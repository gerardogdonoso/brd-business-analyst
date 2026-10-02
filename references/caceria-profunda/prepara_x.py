# -*- coding: utf-8 -*-
"""prepara_x.py — segunda etapa de la caceria (el CRUCE): agrupa por tema las FICHAS que escribieron los cinco
lectores (una linea por elemento) para que dos afirmaciones del mismo tema que cayeron en paquetes distintos
queden en el mismo lote. Salida: paquetes_x.json y elementos_x.json (para leer.py con LEER_SUFIJO=_x)."""
import importlib.util, io, json, math, os, random, re, sys
from collections import Counter, defaultdict

RAIZ = r"C:\Users\User\Projects\agentesIA"
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
spec = importlib.util.spec_from_file_location("buscar_brd", os.path.join(RAIZ, "tools", "buscar-brd.py"))
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)

D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
CITAS, ENT, CAMBIO = D["citas"], D["entrantes"], D["cambio_en"]
EL = D["elementos"]
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
paquete_de = {}
for p in P["paquetes"]:
    for g in p["grupos"]:
        for i in g["ids"]:
            paquete_de[i] = p["lente"]

PREFS = r'AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT'
IDL = re.compile(r'^[\s>*\-`]*(.+?)[`\s]*\|(.*)$')
TOKEN_ID = re.compile(r'^(?:(%s)-)?(\d{3})$' % PREFS)

def ids_de_cabeza(cab):
    """IDs de la cabeza de una ficha. Acepta un ID solo, «(leido)» detras, y grupos como CA-281/297/360 o RN-1, CB-2:
    un numero suelto hereda el prefijo del ultimo ID completo."""
    out = []; pref = None
    for t in re.split(r'[\s,/;+&]+', re.sub(r'\([^)]*\)', ' ', cab)):
        m = TOKEN_ID.match(t.strip("`*"))
        if not m:
            continue
        if m.group(1):
            pref = m.group(1)
        if pref:
            out.append("%s-%s" % (pref, m.group(2)))
    return out

items = {}
sin_id = 0
agrupadas = 0
for k in range(1, 6):
    ruta = os.path.join(SP, "fichas_L%d.md" % k)
    for ln in io.open(ruta, encoding="utf-8"):
        m = IDL.match(ln.rstrip("\n"))
        ids_l = ids_de_cabeza(m.group(1)) if (m and len(m.group(1)) <= 90) else []
        ids_l = [x for x in ids_l if x in EL]
        if not ids_l:
            if ln.strip() and not ln.startswith("#"):
                sin_id += 1
            continue
        resto = m.group(2).strip()
        if len(ids_l) > 1:
            agrupadas += 1
        for i in ids_l:
            texto = "[paquete %s] %s | %s" % (paquete_de.get(i, "?"), i, resto if len(ids_l) == 1 else "(ficha de grupo %s) %s" % ("/".join(ids_l), resto))
            if i in items:
                items[i] += "  //  " + resto
            else:
                items[i] = texto
print("fichas validas:", len(items), "elementos distintos; lineas sin ID reconocible:", sin_id)

docs = {k: bb.palabras(v) for k, v in items.items()}
N = len(docs)
df = Counter()
for toks in docs.values():
    df.update(set(toks))
idf = {t: math.log((N + 1) / (n + 1)) + 1.0 for t, n in df.items()}
vec = {}
for k, toks in docs.items():
    tf = Counter(toks)
    w = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items() if df[t] >= 2}
    norm = math.sqrt(sum(x * x for x in w.values())) or 1.0
    vec[k] = {t: x / norm for t, x in w.items()}

def coseno(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())

def centroide(ids):
    c = defaultdict(float)
    for i in ids:
        for t, x in vec[i].items():
            c[t] += x
    norm = math.sqrt(sum(x * x for x in c.values())) or 1.0
    return {t: x / norm for t, x in c.items()}

def kmeans(ids, k, it=10, semilla=5):
    rnd = random.Random(semilla)
    ids = list(ids)
    if k >= len(ids):
        return [[i] for i in ids]
    cents = [vec[rnd.choice(ids)]]
    dmin = {i: 1 - coseno(vec[i], cents[0]) for i in ids}
    while len(cents) < k:
        tot = sum(dmin.values())
        r = rnd.random() * tot
        acc = 0.0; elegido = ids[-1]
        for i in ids:
            acc += dmin[i]
            if acc >= r:
                elegido = i; break
        cents.append(vec[elegido])
        for i in ids:
            d = 1 - coseno(vec[i], cents[-1])
            if d < dmin[i]:
                dmin[i] = d
    grupos = {}
    for _ in range(it):
        grupos = defaultdict(list)
        for i in ids:
            mejor, mc = 0, -1.0
            for j, c in enumerate(cents):
                s = coseno(vec[i], c)
                if s > mc:
                    mejor, mc = j, s
            grupos[mejor].append(i)
        cents = [centroide(grupos[j]) if grupos[j] else cents[j] for j in range(k)]
    return [g for g in grupos.values() if g]

ids = list(items)
K = 45
grupos = kmeans(ids, K)
final = []
cola = list(grupos)
TOPE = 35
while cola:
    g = cola.pop()
    if len(g) > TOPE:
        sub = kmeans(g, math.ceil(len(g) / 25.0), it=8, semilla=9)
        if len(sub) == 1:
            g2 = sorted(g)
            for j in range(0, len(g2), TOPE):
                final.append(g2[j:j + TOPE])
        else:
            cola.extend(sub)
    else:
        final.append(g)
for g in final:
    g.sort()
cents = [centroide(g) for g in final]
vol = [sum(len(items[i]) for i in g) for g in final]
n = len(final)
visit = [False] * n
inicio = max(range(n), key=lambda j: vol[j])
cadena = [inicio]; visit[inicio] = True
while len(cadena) < n:
    ult = cadena[-1]
    mejor, ms = None, -1.0
    for j in range(n):
        if not visit[j]:
            s = coseno(cents[ult], cents[j])
            if s > ms:
                mejor, ms = j, s
    cadena.append(mejor); visit[mejor] = True
NPAQ = 2
total = sum(vol); objetivo = total / NPAQ
paqs = [[]]; acum = 0
for j in cadena:
    if acum >= objetivo * len(paqs) and len(paqs) < NPAQ:
        paqs.append([])
    paqs[-1].append(j); acum += vol[j]

def nombre(g):
    c = Counter()
    for i in g:
        for t in set(docs[i]):
            c[t] += idf[t]
    return " ".join(t for t, _ in c.most_common(5))

salida = {"paquetes": []}
for p, lista in enumerate(paqs, 1):
    gs = [{"id_grupo": j, "nombre": nombre(final[j]), "ids": final[j]} for j in lista]
    nid = sum(len(g["ids"]) for g in gs)
    chars = sum(vol[j] for j in lista)
    salida["paquetes"].append({"lente": "X%d" % p, "grupos": gs, "n": nid, "chars": chars, "n_cambiados": sum(1 for g in gs for i in g["ids"] if i in CAMBIO)})
    print("X%d: %d fichas, %d KB, %d grupos" % (p, nid, chars // 1024, len(gs)))
json.dump(salida, io.open(os.path.join(SP, "paquetes_x.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"elementos": items, "citas": CITAS, "entrantes": ENT, "cambio_en": CAMBIO, "orden": list(items)},
          io.open(os.path.join(SP, "elementos_x.json"), "w", encoding="utf-8"), ensure_ascii=False)
# mezcla de paquetes dentro de los grupos: cuantos grupos tienen fichas de 2 o mas paquetes de origen
mix = 0
for g in final:
    ps = {paquete_de.get(i) for i in g}
    if len(ps) >= 2:
        mix += 1
print("grupos con fichas de 2 o mas paquetes de origen: %d de %d" % (mix, len(final)))

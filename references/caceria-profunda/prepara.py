# -*- coding: utf-8 -*-
"""Prepara la caceria profunda: agrupa los elementos vivos del BRD por tema (TF-IDF + k-means,
semilla fija) y reparte los grupos en cinco paquetes de lectura de volumen parecido.
Salida (en el scratchpad): grupos.json, paquetes.json, elementos.json.
NO lee con modelo: es mecanico y reproducible. Cada paso declara que cuenta."""
import importlib.util, io, json, math, os, random, re, sys
from collections import Counter, defaultdict

RAIZ = r"C:\Users\User\Projects\agentesIA"
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

spec = importlib.util.spec_from_file_location("buscar_brd", os.path.join(RAIZ, "tools", "buscar-brd.py"))
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)

PREF = (r'AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|'
        r'OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT')
FILA = re.compile(r'^\|\s*((?:%s)-\d{3})\s*\|(.*)$' % PREF)
TOKEN = re.compile(r'\b(?:%s|INV)-\d{3}\b' % PREF)

# 1) elementos vivos: primera fila por ID, solo §1 a §15 (antes de «## 16»)
elementos = {}
orden = []
import comun  # la lista de familias y el reconocimiento de elementos son UNO (tools/comun.py): incluye las notas NT en cita en bloque
with io.open(os.path.join(RAIZ, "docs", "BRD.md"), encoding="utf-8") as f:
    for ln in f:
        if ln.startswith("## 16."):
            break
        d = comun.definicion(ln.rstrip("\r\n"))
        if d and d[0] not in elementos and d[0].rsplit("-", 1)[0] != "INV":
            fila = d[1].rstrip()
            if fila.endswith("|"):
                fila = fila[:-1].rstrip()
            elementos[d[0]] = fila.strip()
            orden.append(d[0])
print("elementos vivos §1-§15:", len(elementos))

# 2) citas dentro del BRD
citas = {}
entrantes = defaultdict(set)
for k, v in elementos.items():
    cs = {c for c in TOKEN.findall(v) if c != k and c in elementos}
    citas[k] = sorted(cs)
    for c in cs:
        entrantes[c].add(k)

# 3) cambios desde la ultima lectura entera
cambios = json.load(io.open(os.path.join(SP, "lista_cambiados.json"), encoding="utf-8"))
cambio_en = defaultdict(list)
for ver, d in cambios["por_version"].items():
    for i in set(d["nuevos"]) | set(d["modificados"]):
        cambio_en[i].append(ver)
print("cambiados vivos:", sum(1 for i in cambio_en if i in elementos), "de", len(cambio_en), "(el resto son INV o derogados)")

# 4) TF-IDF
docs = {k: bb.palabras(v) for k, v in elementos.items()}
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

def kmeans(ids, k, iteraciones=10, semilla=7):
    rnd = random.Random(semilla)
    ids = list(ids)
    if k >= len(ids):
        return [[i] for i in ids]
    # k-means++ con distancia 1-coseno
    cents = [vec[rnd.choice(ids)]]
    dmin = {i: 1 - coseno(vec[i], cents[0]) for i in ids}
    while len(cents) < k:
        tot = sum(dmin.values())
        if tot <= 0:
            cents.append(vec[rnd.choice(ids)])
        else:
            r = rnd.random() * tot
            acc = 0.0
            elegido = ids[-1]
            for i in ids:
                acc += dmin[i]
                if acc >= r:
                    elegido = i
                    break
            cents.append(vec[elegido])
        for i in ids:
            d = 1 - coseno(vec[i], cents[-1])
            if d < dmin[i]:
                dmin[i] = d
    asign = {}
    for _ in range(iteraciones):
        grupos = defaultdict(list)
        for i in ids:
            mejor, mc = 0, -1.0
            for j, c in enumerate(cents):
                s = coseno(vec[i], c)
                if s > mc:
                    mejor, mc = j, s
            grupos[mejor].append(i)
        nuevos = []
        for j in range(k):
            if grupos[j]:
                nuevos.append(centroide(grupos[j]))
            else:
                nuevos.append(cents[j])
        cents = nuevos
    return [g for g in grupos.values() if g]

ids = list(elementos)
K = 75
print("agrupando %d elementos en %d grupos..." % (len(ids), K))
grupos = kmeans(ids, K)
# partir los grupos de mas de 40 elementos
TOPE = 40
final = []
cola = list(grupos)
while cola:
    g = cola.pop()
    if len(g) > TOPE:
        sub = kmeans(g, math.ceil(len(g) / 28.0), iteraciones=8, semilla=11)
        if len(sub) == 1:  # no se pudo partir: por orden de ID
            g2 = sorted(g)
            for j in range(0, len(g2), TOPE):
                final.append(g2[j:j + TOPE])
        else:
            cola.extend(sub)
    else:
        final.append(g)
print("grupos finales:", len(final), "tamanos:", sorted([len(g) for g in final], reverse=True)[:12], "...", sorted([len(g) for g in final])[:5])

def nombre_grupo(g):
    c = Counter()
    for i in g:
        for t in set(docs[i]):
            c[t] += idf[t]
    return " ".join(t for t, _ in c.most_common(5))

for g in final:
    g.sort()
cents = [centroide(g) for g in final]
vol = [sum(len(elementos[i]) + len(i) for i in g) for g in final]

# 5) cadena de vecinos mas cercanos entre grupos, y corte en cinco paquetes por volumen
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
total = sum(vol)
NPAQ = 5
objetivo = total / NPAQ
paquetes = [[]]
acum = 0
for j in cadena:
    if acum >= objetivo * len(paquetes) and len(paquetes) < NPAQ:
        paquetes.append([])
    paquetes[-1].append(j)
    acum += vol[j]

salida = {"paquetes": []}
for p, lista in enumerate(paquetes, 1):
    gs = [{"id_grupo": j, "nombre": nombre_grupo(final[j]), "ids": final[j]} for j in lista]
    nid = sum(len(g["ids"]) for g in gs)
    chars = sum(vol[j] for j in lista)
    nch = sum(1 for g in gs for i in g["ids"] if i in cambio_en)
    salida["paquetes"].append({"lente": "L%d" % p, "grupos": gs, "n": nid, "chars": chars, "n_cambiados": nch})
    print("L%d: %d elementos, %d KB, %d cambiados desde la ultima lectura entera, %d grupos" % (p, nid, chars // 1024, nch, len(gs)))
    print("    temas:", " | ".join(g["nombre"] for g in gs[:6]), "...")

json.dump(salida, io.open(os.path.join(SP, "paquetes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"elementos": elementos, "citas": citas, "entrantes": {k: sorted(v) for k, v in entrantes.items()},
           "cambio_en": cambio_en, "orden": orden}, io.open(os.path.join(SP, "elementos.json"), "w", encoding="utf-8"), ensure_ascii=False)
asignados = [i for p in salida["paquetes"] for g in p["grupos"] for i in g["ids"]]
print("cobertura del reparto: %d asignados, %d unicos, %d vivos -> faltan %d" % (len(asignados), len(set(asignados)), len(elementos), len(set(elementos) - set(asignados))))

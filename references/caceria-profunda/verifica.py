# -*- coding: utf-8 -*-
"""verifica.py — comprueba POR SCRIPT lo que los lectores reportaron, antes de que nadie lo lea como cierto.
Mide: (1) que los dos IDs sean elementos vivos; (2) que cada cita textual este en el elemento (comun.contiene);
(3) si los dos elementos de verdad se citan (grafo del BRD) contra lo que dijo el lector; (4) si el par ya tenia fila
en el enrutador y en que estado; (5) cuanto de cada paquete se imprimio (registro de leer.py).
No juzga si la contradiccion es real: eso lo hace una lectura con el vecindario abierto.
Uso: python verifica.py [L1 L2 ...]   (por defecto, todas las que tengan hallazgos_*.jsonl)"""
import glob, io, json, os, re, sys
from collections import Counter, defaultdict

SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun

BRD = comun.leer(os.path.join(RAIZ, "docs", "BRD.md"))
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CITAS, CAMBIO = D["elementos"], D["citas"], D["cambio_en"]
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))

# enrutador: una linea por fila; que IDs del BRD nombra y en que estado esta
TOK = re.compile(r'\b(?:AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT)-\d{3}\b')
ROW = re.compile(r'^\|\s*\*{0,2}([A-Z]{1,3}-\d+)\*{0,2}\s*\|')
filas_enr = []
for ruta_enr, etiqueta in (("correcciones-brd-pendientes.md", None), (os.path.join("archivo", "correcciones-aplicadas.md"), "archivada")):
    for ln in io.open(os.path.join(RAIZ, "docs", ruta_enr), encoding="utf-8"):
        m = ROW.match(ln)
        if not m:
            continue
        estado = etiqueta or ("aplicada" if "✅ APLICADA" in ln or "APLICADA" in ln[:600] else ("en parte" if "EN PARTE" in ln else "abierta"))
        filas_enr.append((m.group(1), set(TOK.findall(ln)), estado))
print("enrutador + archivo: %d filas leidas" % len(filas_enr))


def reparar(x):
    """Un lector escribio el JSONL con la codificacion de Windows (cp1252) y quedo UTF-8 doblemente codificado
    («Â«», «Ã¡»). Se deshace solo cuando la cadena trae esas marcas y la inversa decodifica limpia."""
    if isinstance(x, str):
        if any(m in x for m in ("Ã", "Â", "â€")):
            try:
                return x.encode("cp1252").decode("utf-8")
            except Exception:
                try:
                    return x.encode("latin-1").decode("utf-8")
                except Exception:
                    return x
        return x
    if isinstance(x, list):
        return [reparar(i) for i in x]
    if isinstance(x, dict):
        return {k: reparar(v) for k, v in x.items()}
    return x

def conocidos(a, b):
    return [(r, est) for r, ids, est in filas_enr if a in ids and b in ids]

lentes = [a for a in sys.argv[1:] if not a.startswith("-")] or sorted(
    os.path.basename(f)[len("hallazgos_"):-len(".jsonl")] for f in glob.glob(os.path.join(SP, "hallazgos_*.jsonl")))

todo = []
for L in lentes:
    ruta = os.path.join(SP, "hallazgos_%s.jsonl" % L)
    if not os.path.exists(ruta):
        print("%s: sin archivo de hallazgos" % L); continue
    malas = 0
    for n, ln in enumerate(io.open(ruta, encoding="utf-8"), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            h = json.loads(ln)
        except Exception:
            malas += 1; continue
        h = reparar(h)
        h["_lente"] = L
        todo.append(h)
    if malas:
        print("%s: %d linea(s) que no son JSON valido" % (L, malas))

res = []
for h in todo:
    par = h.get("par") or []
    out = {"id": h.get("id"), "lente": h["_lente"], "par": par, "clase": h.get("clase"), "confianza": h.get("confianza")}
    if len(par) != 2:
        out["problema"] = "el par no son dos IDs"; res.append(out); continue
    a, b = par
    out["existen"] = (a in E or bool(comun.elemento(BRD, a))) and (b in E or bool(comun.elemento(BRD, b)))
    ta = comun.elemento(BRD, a); tb = comun.elemento(BRD, b)
    qa, qb = h.get("cita_a") or "", h.get("cita_b") or ""
    out["cita_a_en_A"] = bool(qa) and comun.contiene(ta, qa)
    out["cita_b_en_B"] = bool(qb) and comun.contiene(tb, qb)
    out["cita_a_en_B"] = bool(qa) and comun.contiene(tb, qa)
    out["cita_b_en_A"] = bool(qb) and comun.contiene(ta, qb)
    out["citas_ok"] = out["cita_a_en_A"] and out["cita_b_en_B"]
    out["citas_cruzadas"] = (not out["citas_ok"]) and out["cita_a_en_B"] and out["cita_b_en_A"]
    out["se_citan_real"] = (b in CITAS.get(a, [])) or (a in CITAS.get(b, []))
    out["se_citan_dijo"] = bool(h.get("se_citan"))
    out["conocido"] = conocidos(a, b)
    out["cambio"] = {a: CAMBIO.get(a), b: CAMBIO.get(b)}
    res.append(out)

json.dump(res, io.open(os.path.join(SP, "verificado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("=== COBERTURA DE LECTURA (lo que leer.py imprimio; NO prueba que se leyo con atencion) ===")
for p in P["paquetes"]:
    L = p["lente"]
    f = os.path.join(SP, "leido_%s.log" % L)
    if not os.path.exists(f):
        print("%s: sin lotes impresos (0 de %d elementos)" % (L, p["n"])); continue
    ids = set()
    lotes = 0
    for ln in io.open(f, encoding="utf-8"):
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 4:
            lotes += 1; ids.update(c[3].split())
    ch = sum(1 for g in p["grupos"] for i in g["ids"] if i in CAMBIO)
    chl = sum(1 for g in p["grupos"] for i in g["ids"] if i in CAMBIO and i in ids)
    print("%s: %d lotes impresos, %d de %d elementos (%d%%); cambiados desde v5.58: %d de %d" % (L, lotes, len(ids), p["n"], 100 * len(ids) // p["n"], chl, ch))

print("\n=== HALLAZGOS: %d reportados ===" % len(res))
c = Counter()
for r in res:
    c["total"] += 1
    if r.get("problema"):
        c["par mal formado"] += 1; continue
    if not r["existen"]:
        c["algun ID no es elemento vivo"] += 1
    if r["citas_ok"]:
        c["citas OK (las dos estan en su elemento)"] += 1
    elif r["citas_cruzadas"]:
        c["citas cruzadas (estan, en el otro elemento)"] += 1
    else:
        c["alguna cita NO esta en su elemento"] += 1
    if r["se_citan_real"]:
        c["se citan de verdad"] += 1
    if r["se_citan_real"] != r["se_citan_dijo"]:
        c["el lector se equivoco en «se citan»"] += 1
    if r["conocido"]:
        c["par que ya tenia fila en el enrutador"] += 1
    c["clase:%s" % r["clase"]] += 1
    c["confianza:%s" % r["confianza"]] += 1
for k, v in sorted(c.items()):
    print("  %-48s %d" % (k, v))

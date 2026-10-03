# -*- coding: utf-8 -*-
"""stats.py - cifras del resultado para la cabecera del bloque, con lo que cuenta cada una."""
import glob, io, json, os, re, sys
from collections import Counter
SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun
BRD = comun.leer(os.path.join(RAIZ, "docs", "BRD.md"))
cons = json.load(io.open(os.path.join(SP, "consolidado.json"), encoding="utf-8"))
ver = {}
for f in sorted(glob.glob(os.path.join(SP, "veredictos_V*.jsonl"))):
    for ln in io.open(f, encoding="utf-8"):
        if ln.strip():
            v = json.loads(ln); ver[int(v["n"])] = v
print("veredictos:", len(ver), Counter(v["veredicto"] for v in ver.values()))
nc = [v for v in ver.values() if v["veredicto"] != "compatible"]
print("no compatibles:", len(nc))
print("resuelve:", dict(Counter(v.get("resuelve") for v in nc)))
print("cede:", dict(Counter(v.get("cede") for v in nc)))
print("cambia_lo_que_se_programa:", dict(Counter(v.get("cambia_lo_que_se_programa") for v in nc)))
malas = 0
for v in ver.values():
    a, b = v["par"]
    ok = comun.contiene(comun.elemento(BRD, a), v.get("cita_clave_a", "")) and comun.contiene(comun.elemento(BRD, b), v.get("cita_clave_b", ""))
    if not ok:
        malas += 1
print("citas clave de verificadores que no pasan comun.contiene:", malas, "de", len(ver))
# por lector de origen
por_l = Counter(); ver_l = Counter()
for c in cons:
    for l in c["lentes"]:
        por_l[l] += 1
print("pares por lector de origen:", dict(sorted(por_l.items())))
print("pares que se citan:", sum(1 for c in cons if c["se_citan_real"]), "de", len(cons), "; con una nota NT:", sum(1 for c in cons if any(i.startswith("NT-") for i in c["par"])))
print("pares con fila previa en el enrutador:", sum(1 for c in cons if c["conocido"]), "; de esos no compatibles:", sum(1 for c in cons if c["conocido"] and ver[c["n"]]["veredicto"] != "compatible"))
print("pares que tocan un elemento cambiado desde la v5.95:", sum(1 for c in cons if any(c["cambio"].values())), "; no compatibles:", sum(1 for c in cons if any(c["cambio"].values()) and ver[c["n"]]["veredicto"] != "compatible"))
elems = {i for c in cons for i in c["par"]}
print("elementos distintos en los pares:", len(elems))
print()
for n in sorted(ver):
    v = ver[n]
    if v["veredicto"] == "contradice":
        print("CONTRADICE N=%d %s | cede=%s resuelve=%s | %s" % (n, v["par"], v.get("cede"), v.get("resuelve"), re.sub(r"\s+", " ", v.get("razon", ""))[:330]))

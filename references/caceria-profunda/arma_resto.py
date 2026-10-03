# -*- coding: utf-8 -*-
"""arma_resto.py — paquetes de verificacion A CIEGAS con TODOS los pares validos que todavia no tienen veredicto:
los que quedaron sin verificar al corte del 03-10-2026 (limite de 5 horas en 85%) y los del cruce que llegaron despues.
Mismo formato que arma_verif.py (sin el razonamiento del primer lector). Arreglo frente a `arma_verif.py --nuevos`:
aquel filtra por los pares ASIGNADOS a un paquete, no por los que tienen veredicto, y dejaria fuera los cortados.
Uso: python arma_resto.py [NPAQ] [PRIMER_NUMERO_DE_PAQUETE]   (por defecto 2 paquetes, V4 y V5)
Antes: python consolida.py (suma los pares del cruce y conserva la numeracion de los 72 primeros)."""
import glob, io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NPAQ = int(sys.argv[1]) if len(sys.argv) > 1 else 2
PRIMERO = int(sys.argv[2]) if len(sys.argv) > 2 else 4

cons = json.load(io.open(os.path.join(SP, "consolidado.json"), encoding="utf-8"))
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
CITAS, ENT, CAMBIO = D["citas"], D["entrantes"], D["cambio_en"]
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
orden = {}
k = 0
for p in P["paquetes"]:
    for g in p["grupos"]:
        for i in g["ids"]:
            orden[i] = k; k += 1

def vk(v):
    return tuple(int(x) for x in v.split("."))

def lista(ids, tope=14):
    ids = list(ids)
    if not ids:
        return "ninguno"
    return ", ".join(ids[:tope]) + (" (+%d)" % (len(ids) - tope) if len(ids) > tope else "")

hechos = set()
for f in glob.glob(os.path.join(SP, "veredictos_V*.jsonl")):
    for ln in io.open(f, encoding="utf-8"):
        try:
            hechos.add(int(json.loads(ln)["n"]))
        except Exception:
            pass
validos = [c for c in cons if c["existen"] and all(c["citas_ok"])]
descartados = [c for c in cons if not (c["existen"] and all(c["citas_ok"]))]
resto = [c for c in validos if c["n"] not in hechos]
print("pares: %d; validos: %d; con veredicto: %d; SIN veredicto: %d; descartados por el script de citas: %d" % (
    len(cons), len(validos), len(hechos), len(resto), len(descartados)))
resto.sort(key=lambda c: (orden.get(c["par"][0], 99999), c["par"][1]))
por_paq = [[] for _ in range(NPAQ)]
objetivo = max(1, len(resto)) / NPAQ
for j, c in enumerate(resto):
    por_paq[min(NPAQ - 1, int(j / objetivo))].append(c)

f_idx = os.path.join(SP, "verif_indice.json")
prev = json.load(io.open(f_idx, encoding="utf-8")) if os.path.exists(f_idx) else {"indice": {}, "descartados": []}
for n, grupo in enumerate(por_paq, PRIMERO):
    out = ["# VERIFICACION V%d — %d pares\n" % (n, len(grupo))]
    for c in grupo:
        a, b = c["par"]
        prev["indice"][str(c["n"])] = [a, b]
        out.append("## PAR %d: %s  <->  %s" % (c["n"], a, b))
        out.append("clase(s) que dijo el primer lector: %s" % ", ".join(c["clases"]))
        out.append("%s cambio en: %s | %s cambio en: %s" % (
            a, ", ".join("v" + v for v in sorted(CAMBIO.get(a, []), key=vk)) or "no cambio desde la ultima lectura entera",
            b, ", ".join("v" + v for v in sorted(CAMBIO.get(b, []), key=vk)) or "no cambio desde la ultima lectura entera"))
        out.append("¿se citan? %s" % ("SI (uno cita al otro)" if c["se_citan_real"] else "NO"))
        for h in c["hallazgos"][:2]:
            x, y = h["par"]
            out.append("cita de %s: «%s»" % (x, re.sub(r"\s+", " ", h.get("cita_a", ""))))
            out.append("cita de %s: «%s»" % (y, re.sub(r"\s+", " ", h.get("cita_b", ""))))
        out.append("%s cita a: %s | lo citan: %s" % (a, lista(CITAS.get(a, [])), lista(ENT.get(a, []))))
        out.append("%s cita a: %s | lo citan: %s" % (b, lista(CITAS.get(b, [])), lista(ENT.get(b, []))))
        out.append("")
    io.open(os.path.join(SP, "verif_V%d.md" % n), "w", encoding="utf-8").write("\n".join(out))
    print("V%d: %d pares, %d KB" % (n, len(grupo), len("\n".join(out)) // 1024))
prev["descartados"] = [c["par"] for c in descartados]
json.dump(prev, io.open(f_idx, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

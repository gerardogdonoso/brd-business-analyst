# -*- coding: utf-8 -*-
"""arma_verif.py — arma los paquetes de la VERIFICACION a ciegas: por cada par distinto, solo los IDs, la clase que dijo el
primer lector, las citas literales y los datos que pone el instrumento (versiones en que cambio cada elemento, si se citan,
IDs vecinos). NO lleva el razonamiento del primer lector: el verificador juzga por su cuenta.
Salida: verif_V1.md ... verif_Vk.md y verif_indice.json (n -> par)."""
import io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NPAQ = int(sys.argv[1]) if len(sys.argv) > 1 else 4

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

def lista(ids, tope=14):
    ids = list(ids)
    return (", ".join(ids[:tope]) + (" (+%d)" % (len(ids) - tope if len(ids) > tope else 0) if len(ids) > tope else "")) if ids else "ninguno"

validos = [c for c in cons if c["existen"] and all(c["citas_ok"])]
descartados = [c for c in cons if not (c["existen"] and all(c["citas_ok"]))]
print("pares: %d; pasan el script de citas: %d; descartados por el script: %d" % (len(cons), len(validos), len(descartados)))
validos.sort(key=lambda c: (orden.get(c["par"][0], 99999), c["par"][1]))
if "--nuevos" in sys.argv:
    # solo los pares que NINGUN verificador atendio todavia: un paquete V5 aparte, sin tocar V1..V4
    import glob
    ya = set()
    for f in glob.glob(os.path.join(SP, "veredictos_V*.jsonl")):
        for ln in io.open(f, encoding="utf-8"):
            try:
                ya.add(int(json.loads(ln)["n"]))
            except Exception:
                pass
    f_idx = os.path.join(SP, "verif_indice.json")
    asignados = set()
    if os.path.exists(f_idx):
        asignados = {int(k) for k in json.load(io.open(f_idx, encoding="utf-8"))["indice"]}
    validos = [c for c in validos if c["n"] not in asignados]
    NPAQ = 1
    print("pares nuevos sin verificador: %d" % len(validos))
por_paq = [[] for _ in range(NPAQ)]
tam = [0] * NPAQ
for c in validos:   # reparto en tandas contiguas de tamano parecido (queda cada tema junto)
    pass
objetivo = len(validos) / NPAQ
for j, c in enumerate(validos):
    por_paq[min(NPAQ - 1, int(j / objetivo))].append(c)

indice = {}
for n, grupo in enumerate(por_paq, 1):
    out = ["# VERIFICACION V%d — %d pares\n" % (n, len(grupo))]
    for c in grupo:
        a, b = c["par"]
        indice[str(c["n"])] = [a, b]
        out.append("## PAR %d: %s  <->  %s" % (c["n"], a, b))
        out.append("clase(s) que dijo el primer lector: %s" % ", ".join(c["clases"]))
        out.append("%s cambio en: %s | %s cambio en: %s" % (a, ", ".join("v" + v for v in sorted(CAMBIO.get(a, []), key=float)) or "no cambio desde la ultima lectura entera",
                                                           b, ", ".join("v" + v for v in sorted(CAMBIO.get(b, []), key=float)) or "no cambio desde la ultima lectura entera"))
        out.append("¿se citan? %s" % ("SI (uno cita al otro)" if c["se_citan_real"] else "NO"))
        for h in c["hallazgos"][:2]:
            x, y = h["par"]
            out.append("cita de %s: «%s»" % (x, re.sub(r"\s+", " ", h.get("cita_a", ""))))
            out.append("cita de %s: «%s»" % (y, re.sub(r"\s+", " ", h.get("cita_b", ""))))
        out.append("%s cita a: %s | lo citan: %s" % (a, lista(CITAS.get(a, [])), lista(ENT.get(a, []))))
        out.append("%s cita a: %s | lo citan: %s" % (b, lista(CITAS.get(b, [])), lista(ENT.get(b, []))))
        out.append("")
    io.open(os.path.join(SP, "verif_V%d.md" % (5 if "--nuevos" in sys.argv else n)), "w", encoding="utf-8").write("\n".join(out))
    print("V%d: %d pares, %d KB" % (5 if "--nuevos" in sys.argv else n, len(grupo), len("\n".join(out)) // 1024))
if "--nuevos" in sys.argv:
    prev = json.load(io.open(os.path.join(SP, "verif_indice.json"), encoding="utf-8"))
    prev["indice"].update(indice)
    json.dump(prev, io.open(os.path.join(SP, "verif_indice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
else:
    json.dump({"indice": indice, "descartados": [c["par"] for c in descartados]}, io.open(os.path.join(SP, "verif_indice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

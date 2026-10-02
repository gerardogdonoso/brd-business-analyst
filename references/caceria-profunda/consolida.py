# -*- coding: utf-8 -*-
"""consolida.py — junta los hallazgos de todos los lectores, repara la codificacion, quita duplicados por par
(sin importar el orden de los IDs) y agrega lo que el script comprobo (citas, se citan, ya enrutado, cambio).
Salida: consolidado.json y un listado compacto por pantalla (--lista) o el texto completo de uno (--ver N)."""
import glob, io, json, os, re, sys
from collections import defaultdict, Counter

SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun

def reparar(x):
    if isinstance(x, str):
        if any(m in x for m in ("Ã", "Â", "â€")):
            for cod in ("cp1252", "latin-1"):
                try:
                    return x.encode(cod).decode("utf-8")
                except Exception:
                    pass
        return x
    if isinstance(x, list):
        return [reparar(i) for i in x]
    if isinstance(x, dict):
        return {k: reparar(v) for k, v in x.items()}
    return x

BRD = comun.leer(os.path.join(RAIZ, "docs", "BRD.md"))
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CITAS, CAMBIO = D["elementos"], D["citas"], D["cambio_en"]

TOK = re.compile(r'\b(?:AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT)-\d{3}\b')
ROW = re.compile(r'^\|\s*\*{0,2}([A-Z]{1,3}-\d+)\*{0,2}\s*\|')
filas_enr = []
for ruta_enr, etiqueta in (("correcciones-brd-pendientes.md", None), (os.path.join("archivo", "correcciones-aplicadas.md"), "archivada")):
    for ln in io.open(os.path.join(RAIZ, "docs", ruta_enr), encoding="utf-8"):
        m = ROW.match(ln)
        if m:
            est = etiqueta or ("aplicada" if "APLICADA" in ln[:700] else ("en parte" if "EN PARTE" in ln else "abierta"))
            filas_enr.append((m.group(1), set(TOK.findall(ln)), est))

def conocidos(a, b):
    return [(r, est) for r, ids, est in filas_enr if a in ids and b in ids]

crudo = []
for f in sorted(glob.glob(os.path.join(SP, "hallazgos_*.jsonl"))):
    L = os.path.basename(f)[len("hallazgos_"):-len(".jsonl")]
    if L in ("TEST",):
        continue
    for ln in io.open(f, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            h = reparar(json.loads(ln))
        except Exception:
            print("linea no valida en", f); continue
        h["_lente"] = L
        crudo.append(h)

por_par = defaultdict(list)
for h in crudo:
    par = h.get("par") or []
    if len(par) != 2:
        continue
    por_par[tuple(sorted(par))].append(h)

cons = []
for (a, b), hs in sorted(por_par.items()):
    ta, tb = comun.elemento(BRD, a), comun.elemento(BRD, b)
    ok = []
    for h in hs:
        qa, qb = h.get("cita_a", ""), h.get("cita_b", "")
        x, y = h["par"]
        tx, ty = comun.elemento(BRD, x), comun.elemento(BRD, y)
        ok.append(bool(qa) and bool(qb) and comun.contiene(tx, qa) and comun.contiene(ty, qb))
    prim = hs[0]
    cons.append({
        "par": [a, b],
        "ids": [h.get("id") for h in hs],
        "lentes": sorted({h["_lente"] for h in hs}),
        "clases": sorted({h.get("clase") for h in hs}),
        "confianza": [h.get("confianza") for h in hs],
        "citas_ok": ok,
        "existen": bool(ta) and bool(tb),
        "se_citan_real": (b in CITAS.get(a, [])) or (a in CITAS.get(b, [])),
        "conocido": conocidos(a, b),
        "cambio": {a: CAMBIO.get(a), b: CAMBIO.get(b)},
        "hallazgos": hs,
    })
# numeracion estable: un par conserva su numero aunque lleguen hallazgos nuevos
num_f = os.path.join(SP, "numeracion.json")
numeracion = json.load(io.open(num_f, encoding="utf-8")) if os.path.exists(num_f) else {}
for c in cons:
    k = "%s|%s" % tuple(c["par"])
    if k not in numeracion:
        numeracion[k] = max(numeracion.values(), default=0) + 1
    c["n"] = numeracion[k]
json.dump(numeracion, io.open(num_f, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
cons.sort(key=lambda c: c["n"])
json.dump(cons, io.open(os.path.join(SP, "consolidado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if "--ver" in sys.argv:
    k = int(sys.argv[sys.argv.index("--ver") + 1])
    c = next(x for x in cons if x["n"] == k)
    print("N=%d par=%s lentes=%s clases=%s conf=%s citas_ok=%s existen=%s se_citan=%s conocido=%s" % (
        c["n"], c["par"], c["lentes"], c["clases"], c["confianza"], c["citas_ok"], c["existen"], c["se_citan_real"], c["conocido"]))
    for h in c["hallazgos"]:
        print("---", h.get("id"))
        for k2 in ("por_que", "cita_a", "cita_b", "supuesto", "tocaria_ceder"):
            print(" ", k2 + ":", re.sub(r"\s+", " ", str(h.get(k2, ""))))
    sys.exit(0)

cuenta = Counter()
print("hallazgos crudos: %d; pares distintos: %d" % (len(crudo), len(cons)))
for c in cons:
    cuenta["citas_ok_todas" if all(c["citas_ok"]) else "alguna_cita_mala"] += 1
    cuenta["se_citan" if c["se_citan_real"] else "no_se_citan"] += 1
    cuenta["conocido" if c["conocido"] else "nuevo_para_el_enrutador"] += 1
    cuenta["tocan_cambiados" if any(c["cambio"].values()) else "ninguno_cambio_desde_la_ultima_lectura"] += 1
    cuenta["en_2_o_mas_lentes"] += 1 if len(c["lentes"]) > 1 else 0
print(dict(cuenta))
if "--lista" in sys.argv:
    for c in cons:
        kn = ",".join("%s:%s" % (r, e[:4]) for r, e in c["conocido"][:3])
        ch = "".join("*" if v else "." for v in c["cambio"].values())
        print("%3d %-9s %-9s %-22s %s %s ci=%s %s %s" % (
            c["n"], c["par"][0], c["par"][1], "/".join(c["clases"])[:22], "/".join((x or "?")[0] for x in c["confianza"]),
            ch, "S" if c["se_citan_real"] else "n", "OK" if all(c["citas_ok"]) else "CITA-MALA", kn))

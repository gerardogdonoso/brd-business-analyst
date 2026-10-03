# -*- coding: utf-8 -*-
"""escribe_dx.py — junta primer lector + verificador a ciegas y emite las filas del bloque EA del enrutador.
Salida: dx_filas.md (las filas de pares que NO son compatibles), dx_descartadas.md (los compatibles, con la razon),
dx_resumen.json (conteos). No inventa nada: cada frase sale de un campo de un lector o del instrumento.
Uso: python escribe_dx.py [--matriz]"""
import glob, io, json, os, re, sys
from collections import Counter, defaultdict

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
cons = json.load(io.open(os.path.join(SP, "consolidado.json"), encoding="utf-8"))
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
CAMBIO = D["cambio_en"]

ver = {}
malos = 0
for f in sorted(glob.glob(os.path.join(SP, "veredictos_V*.jsonl"))):
    for ln in io.open(f, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            v = reparar(json.loads(ln))
            ver[int(v["n"])] = v
        except Exception:
            malos += 1

def limpia(s, tope=None):
    s = re.sub(r"\s+", " ", str(s or "")).strip().replace("|", "/")
    if tope and len(s) > tope:
        corte = s[:tope]
        k = max(corte.rfind(". "), corte.rfind("; "))
        s = (corte[:k + 1] if k > tope * 0.5 else corte.rsplit(" ", 1)[0] + "…")
    return s

def sin_comillas(s):
    """Las frases de un lector que parecen citas pero no lo son (parafrasis, puntos suspensivos) no se dejan entre comillas de cita:
    el control citas-verificadas las leeria como literales."""
    return str(s or "").replace("«", "‘").replace("»", "’").replace("“", "‘").replace("”", "’").replace('"', "’")

FAMILIAS_QUE_ABRE_EL_CONTROL = {"RN", "PR", "AL", "AL-F", "RE", "CB", "CA", "CE", "OB", "PZ", "RG", "SA", "PE", "DA-IN", "DA-OUT", "DA-EST", "PR-ALT", "PR-EXC", "INV"}

def delim(q, eid):
    """Cita literal entre « » si el control sabe abrir la familia del elemento de donde sale; entre ‹ › si no (AC, NT, AC-ECO, DA-CON, BN)."""
    pref = re.sub(r"-\d{3}$", "", eid)
    return ("«%s»" % q) if pref in FAMILIAS_QUE_ABRE_EL_CONTROL else ("‹%s›" % q)

def citas_ok_verificador(v, a, b):
    ta, tb = comun.elemento(BRD, a), comun.elemento(BRD, b)
    qa, qb = v.get("cita_clave_a", ""), v.get("cita_clave_b", "")
    return bool(qa) and bool(qb) and comun.contiene(ta, qa) and comun.contiene(tb, qb)

LETRA = {"derivado": ("a", "Claude, derivándolo de lo ya escrito"), "investigar": ("b", "Claude, investigando antes de proponer"),
         "cuenta": ("c", "la cuenta lo declara y el producto pone el default"), "dueno": ("d", "el dueño, con la escena y la recomendación"),
         "sistema": ("e", "nadie todavía: necesita el sistema construido"), "trd": ("f", "el TRD")}
CEDE = {"A": 0, "B": 1}

# pares «compatibles» que igual se enrutan: {n: "texto del estado"}, en promover.json (se llena a mano en cada corrida)
_pf = os.path.join(SP, "promover.json")
PROMOVER = {int(k): v for k, v in json.load(io.open(_pf, encoding="utf-8")).items()} if os.path.exists(_pf) else {}
filas = []; descartadas = []; sin_ver = []
cuenta = Counter(); matriz = Counter()
for c in cons:
    n = c["n"]; a, b = c["par"]
    v = ver.get(n)
    if v is None:
        sin_ver.append(n); continue
    h = c["hallazgos"][0]
    veredicto = v.get("veredicto")
    cuenta[veredicto] += 1
    matriz[(c["clases"][0], veredicto)] += 1
    ok_v = citas_ok_verificador(v, a, b)
    if not ok_v:
        cuenta["citas_del_verificador_no_pasan"] += 1
    if veredicto == "compatible" and n in PROMOVER:
        veredicto = "promovido"
    if veredicto == "compatible":
        descartadas.append((n, a, b, limpia(sin_comillas(v.get("razon")), 330), c["conocido"]))
        continue
    letra, quien = LETRA.get(v.get("resuelve"), ("?", "sin clasificar"))
    fuente = limpia(sin_comillas(v.get("fuente")), 160)
    if letra in ("a", "b") and fuente:
        quien += " (%s)" % fuente
    ced = v.get("cede")
    if ced in CEDE:
        elem = c["par"][CEDE[ced]] if h["par"][0] == c["par"][0] else c["par"][1 - CEDE[ced]]
        # el verificador habla de A y B segun el orden de verif_V*.md, que sigue c["par"]
        elem = c["par"][CEDE[ced]]
        hacer = "Corregir `%s`: %s" % (elem, limpia(sin_comillas(v.get("por_que_cede")), 420))
    elif ced == "ambos":
        hacer = "Corregir los dos para que digan lo mismo: %s" % limpia(sin_comillas(v.get("por_que_cede")), 420)
    elif ced == "ninguno":
        hacer = "Ninguno cambia por ahora: %s" % limpia(sin_comillas(v.get("por_que_cede") or v.get("razon")), 300)
    else:
        hacer = "Decidir cuál rige: %s" % limpia(sin_comillas(v.get("por_que_cede")), 420)
    if v.get("cambia_lo_que_se_programa") in ("si", "sí"):
        hacer += " (cambia lo que se programa)"
    prom = PROMOVER.get(n) if veredicto == "promovido" else None
    if isinstance(prom, dict) and prom.get("hacer"):
        hacer = prom["hacer"]
    conoc = ""
    if c["conocido"]:
        conoc = " Los dos IDs ya comparten fila con %s." % ", ".join("`%s` (%s)" % (r, e) for r, e in c["conocido"][:4])
    cam = []
    for e in (a, b):
        cv = CAMBIO.get(e)
        if cv:
            cam.append("`%s` cambió en %s" % (e, ", ".join("v" + x for x in sorted(cv, key=lambda v: tuple(int(x) for x in v.split("."))))))
    cam = ("; ".join(cam) + ".") if cam else "Ninguno cambió desde la v5.95."
    citan = "Se citan entre sí." if c["se_citan_real"] else "No se citan."
    primer = "lector %s: %s, confianza %s" % ("/".join(c["lentes"]), "/".join(c["clases"]), "/".join(sorted(set(str(x) for x in c["confianza"]))))
    if a == b:
        sujeto = "dentro de `%s`" % a
    else:
        sujeto = "`%s` frente a `%s`" % (a, b)
    qa = limpia(h.get("cita_a"), 230); qb = limpia(h.get("cita_b"), 230)
    x, y = h["par"]
    partes = "*%s* (`%s`) frente a *%s* (`%s`)" % (delim(qa, x), x, delim(qb, y), y)
    _p = PROMOVER.get(n, "")
    estado = {"contradice": "contradice", "en-parte": "contradice en parte", "no-decidible": "no se puede decidir",
              "promovido": _p.get("estado", "") if isinstance(_p, dict) else _p}.get(veredicto, veredicto)
    quien_txt = "**(%s)** %s" % (letra, quien)
    if letra == "d":
        quien_txt += ": %s" % limpia(sin_comillas(v.get("razon")), 200)
    vec = [i for i in (v.get("vecinos_abiertos") or []) if i not in (a, b)]
    base = ", ".join("`%s`" % i for i in ([a] if a == b else [a, b]) + vec[:4])
    # 03-10-2026: decia siempre «las citas de los dos lectores pasaron el script» aunque las del segundo no pasaran
    txt_citas = ("las citas de los dos lectores pasaron el script" if ok_v
                 else "las citas del primer lector pasaron el script; las citas clave del segundo NO")
    fila = "| **EA-%d** | ○ **SIN VERIFICAR POR LA SESIÓN PRINCIPAL** (%s; segundo lector a ciegas: **%s**; %s) | **%s.** %s *Segundo lector:* %s %s %s%s | %s | %s | %s |" % (
        n, primer, estado, txt_citas, sujeto, partes, limpia(sin_comillas(v.get("razon")), 1000), citan, cam, conoc, base, hacer, quien_txt)
    filas.append((n, fila))

io.open(os.path.join(SP, "dx_filas.md"), "w", encoding="utf-8").write("\n".join(f for _, f in sorted(filas)) + "\n")
d = ["| # | Par | Razón del segundo lector | Filas con los dos IDs |", "|---|---|---|---|"]
for n, a, b, r, k in sorted(descartadas):
    d.append("| EA-%d | `%s` · `%s` | %s | %s |" % (n, a, b, r, ", ".join("%s (%s)" % (x, e) for x, e in k[:3]) or "—"))
io.open(os.path.join(SP, "dx_descartadas.md"), "w", encoding="utf-8").write("\n".join(d) + "\n")
res = {"pares": len(cons), "sin_veredicto": sin_ver, "veredictos": dict(cuenta), "filas": len(filas), "descartadas": len(descartadas),
       "lineas_de_veredicto_mal_formadas": malos}
json.dump(res, io.open(os.path.join(SP, "dx_resumen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
if "--matriz" in sys.argv:
    print("clase del primer lector -> veredicto del segundo:")
    for (cl, ve), k in sorted(matriz.items()):
        print("  %-22s %-14s %d" % (cl, ve, k))

"""plan_con_anclas.py -- arma el plan de una version del BRD SIN retipear los tramos a reemplazar (v5.107, 03-10-2026).

Por que existe: el plan de `aplica_version.py` exige que cada `viejo` aparezca UNA vez en todo el BRD y caiga dentro de la
fila de su elemento. Copiarlos a mano falla (apostrofes, comillas angulares, espacios finos) y en la v5.107 eran 80.
Aqui `E(fila, id, ancla_inicial, ancla_final, nuevo)` extrae el tramo exacto de la fila entre las dos anclas, comprueba
unicidad en el BRD y que no se pisa con otra edicion, y lo agrega a EDS. Uso: un `plan_*.py` hace
`exec(open(<este archivo>).read())`, llama a E(...) y al final vuelca `json.dumps(PLAN)` con EDS, NUEVOS y NOTAS.
Trae rutas absolutas de esa maquina (BRDP): se adaptan. Se escribe el plan con la herramienta Write, no con un heredoc.
"""
# ayudante del plan de la v5.107: extrae el `viejo` exacto del BRD por anclas y comprueba unicidad y solapes
import io, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
BRDP = r"C:\Users\User\Projects\agentesIA\docs\BRD.md"
BRD = io.open(BRDP, encoding="utf-8", newline="").read()
LINES = BRD.split("\n")
EDS, NUEVOS, NOTAS, EVID, SPANS = [], [], [], [], []


def fila_de(idv, linea=None):
    if linea:
        return LINES[linea - 1]
    for l in LINES:
        if l.startswith("| %s |" % idv) or l.startswith("> [%s]" % idv):
            return l
    raise SystemExit("elemento no hallado: %s" % idv)


def E(fila, idv, a, b, nuevo, linea=None, historial=True):
    """viejo = subcadena de la fila de idv desde la ancla a hasta la ancla b (incluidas); b=None -> solo a."""
    r = fila_de(idv, linea)
    if r.count(a) != 1:
        raise SystemExit("ancla inicial NO UNICA (%d) en %s: %r" % (r.count(a), idv, a[:90]))
    i = r.index(a)
    if b is None:
        j = i + len(a)
    else:
        k = r.find(b, i)
        if k < 0:
            raise SystemExit("ancla final NO HALLADA en %s: %r" % (idv, b[:90]))
        j = k + len(b)
    viejo = r[i:j]
    if BRD.count(viejo) != 1:
        raise SystemExit("viejo NO UNICO en el BRD (%d) en %s: %r" % (BRD.count(viejo), idv, viejo[:100]))
    for (x, p, q) in SPANS:
        if x == (idv, linea) and not (j <= p or i >= q):
            raise SystemExit("SOLAPE en %s entre %r y una edicion previa" % (idv, a[:60]))
    SPANS.append(((idv, linea), i, j))
    d = {"fila": fila, "id": idv, "viejo": viejo, "nuevo": nuevo}
    if not historial:
        d["historial"] = False
    EDS.append(d)

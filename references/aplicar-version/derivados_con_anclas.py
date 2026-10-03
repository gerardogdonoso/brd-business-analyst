"""derivados_con_anclas.py -- lo mismo que plan_con_anclas.py, para los documentos derivados del BRD (v5.107).

`D(doc, ancla_inicial, ancla_final, nuevo)` reemplaza un tramo UNICO del documento; `DD(..., veces)` uno identico que vive
en `veces` lineas (una fila copiada en dos lugares); `aplicar(escribir=True)` escribe. Ensayo primero, sin escribir.
Trae RAIZ absoluta de esa maquina: se adapta. Respeta el fin de linea del archivo (lee y escribe con newline="").
"""
# ayudante de los derivados: reemplazos por anclas dentro de UN documento, con unicidad y sin solapes
import io, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = r"C:\Users\User\Projects\agentesIA"
CAMBIOS = {}   # ruta relativa -> lista de (i, j, nuevo)
TEXTOS = {}


def _txt(doc):
    if doc not in TEXTOS:
        TEXTOS[doc] = io.open(os.path.join(RAIZ, doc), encoding="utf-8", newline="").read()
    return TEXTOS[doc]


def D(doc, a, b, nuevo):
    """Reemplaza, dentro de `doc`, el tramo desde la ancla a hasta la ancla b (incluidas) por `nuevo`.
    El tramo debe aparecer UNA sola vez en el documento; b=None -> solo `a`."""
    t = _txt(doc)
    if t.count(a) != 1:
        raise SystemExit("ancla inicial NO UNICA (%d) en %s: %r" % (t.count(a), doc, a[:90]))
    i = t.index(a)
    if b is None:
        j = i + len(a)
    else:
        k = t.find(b, i)
        if k < 0:
            raise SystemExit("ancla final NO HALLADA en %s: %r" % (doc, b[:90]))
        j = k + len(b)
    viejo = t[i:j]
    if t.count(viejo) != 1:
        raise SystemExit("tramo NO UNICO en %s: %r" % (doc, viejo[:90]))
    for (p, q, _) in CAMBIOS.get(doc, []):
        if not (j <= p or i >= q):
            raise SystemExit("SOLAPE en %s: %r" % (doc, a[:70]))
    CAMBIOS.setdefault(doc, []).append((i, j, nuevo))


def DD(doc, a, b, nuevo, veces):
    """Como D, pero el mismo tramo aparece exactamente `veces` veces (p. ej. una fila copiada en dos lugares)
    y se reemplazan todas."""
    t = _txt(doc)
    if t.count(a) != veces:
        raise SystemExit("ancla inicial: %d apariciones y se esperaban %d en %s: %r" % (t.count(a), veces, doc, a[:90]))
    pos = [m.start() for m in re.finditer(re.escape(a), t)]
    viejos = set()
    spans = []
    for i in pos:
        k = t.find(b, i) if b else i
        if k < 0:
            raise SystemExit("ancla final NO HALLADA en %s: %r" % (doc, b[:90]))
        j = (k + len(b)) if b else (i + len(a))
        viejos.add(t[i:j])
        spans.append((i, j))
    if len(viejos) != 1:
        raise SystemExit("los %d tramos de %s no son identicos" % (veces, doc))
    for (i, j) in spans:
        for (p, q, _) in CAMBIOS.get(doc, []):
            if not (j <= p or i >= q):
                raise SystemExit("SOLAPE en %s: %r" % (doc, a[:70]))
        CAMBIOS.setdefault(doc, []).append((i, j, nuevo))


def aplicar(escribir=False):
    for doc, cs in CAMBIOS.items():
        t = _txt(doc)
        for (i, j, n) in sorted(cs, key=lambda x: -x[0]):
            t = t[:i] + n + t[j:]
        print("%-52s %2d cambios  (%+d caracteres)" % (doc, len(cs), len(t) - len(_txt(doc))))
        if escribir:
            io.open(os.path.join(RAIZ, doc), "w", encoding="utf-8", newline="").write(t)

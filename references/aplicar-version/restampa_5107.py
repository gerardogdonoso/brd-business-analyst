# -*- coding: utf-8 -*-
"""Sube la estampa `Al día con BRD` de los derivados que docs-fresh marca (ERROR de herencia fina) a la v5.107,
tras el barrido de frases de la unidad de cobro y de reagendar. Uso: python restampa_5107.py [--escribir]"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
R = r"C:\Users\User\Projects\agentesIA"
NUEVA = "5.107"
escribe = "--escribir" in sys.argv

fresh = io.open(os.path.join(SP, "fresh2.txt"), encoding="utf-8").read()
docs = []
for m in re.finditer(r"ERROR\s+Herencia fina: (\S+) se estampa", fresh):
    docs.append(m.group(1))
docs = [d for d in dict.fromkeys(docs)]

cuenta = {}
doc = None
for ln in fresh.split("\n"):
    m = re.match(r"\[lineas que releer\] (\S+):", ln)
    if m:
        doc = m.group(1)
        cuenta[doc] = 0
        continue
    if doc and re.match(r"\s+L\d+ \[", ln):
        cuenta[doc] += 1

# tramos que se corrigieron en cada documento (cuenta de reemplazos aplicados el 03-10-2026)
CORREGIDOS = {
    "docs/PRD.md": 7, "docs/app-flow.md": 8, "docs/backend-schema.md": 5, "docs/ui-ux-brief.md": 3,
    "docs/huecos-para-implementar.md": 4, "docs/implementation-plan.md": 3, "docs/input-inventory.md": 3,
    "docs/reglas-imponibles.md": 1, "docs/tech-risks.md": 2, "docs/specs/001-primer-camino/spec.md": 4,
    "docs/specs/001-primer-camino/tareas.md": 2, "docs/contraste-owasp-asi.md": 1,
    "docs/mercados-adyacentes.md": 1, "docs/PROJECT-PROFILE.md": 1,
}
RELATOS = {"docs/SUITE-STATE.md", "docs/DECISION-LEDGER.md"}
SIN_NOTA = {"docs/BRD-evidencia.md", "docs/BRD-historial.md", "docs/correcciones-brd-pendientes.md",
            "docs/specs/001-primer-camino/requisitos.md"}
EST = re.compile(r"Al d[ií]a con BRD: v([\d.]+)\*\*")

BASE = ("*(re-estampado el 03-10-2026 contra la v5.107: se barrieron en el documento entero, con dos juegos de palabras, "
        "las frases del cobro que la v5.107 cambió —que `Pedidos` mide pedidos y que la consulta que no pide no suma; "
        "reagendar, la segunda hora con la primera pendiente y el reclamo que vuelve por lo mismo— %s; "
        "el control nombró %d líneas y no se releyeron una por una: las que no repiten esas frases citan elementos "
        "cuyo texto cambió en lo que ninguna de ellas afirma)*")


def nota(d, n):
    if d in CORREGIDOS:
        k = CORREGIDOS[d]
        return BASE % ("y se corrigieron %d tramos que las repetían" % k, n)
    if d in RELATOS:
        return BASE % ("y no se halló ningún tramo vigente que las repita; las menciones que quedan relatan lo que hizo cada versión", n)
    return BASE % ("y no se halló ningún tramo que las repita", n)


for d in docs:
    ruta = os.path.join(R, *d.split("/"))
    t = io.open(ruta, encoding="utf-8", newline="").read()
    m = EST.search(t)
    if not m:
        print("SIN ESTAMPA", d)
        continue
    j = t.find("\n", m.end())
    fin = j if j >= 0 else len(t)
    cr = "\r" if t[fin - 1:fin] == "\r" else ""
    fin_texto = fin - 1 if cr else fin
    resto = t[m.end():fin_texto]
    tenia_nota = resto.lstrip().startswith("*(")
    if d in SIN_NOTA or not tenia_nota:
        t2 = t[:m.start()] + "Al día con BRD: v%s**" % NUEVA + t[m.end():]
        tipo = "sin nota"
    else:
        t2 = t[:m.start()] + "Al día con BRD: v%s** %s" % (NUEVA, nota(d, cuenta.get(d, 0))) + t[fin_texto:]
        tipo = "nota %d lineas" % cuenta.get(d, 0)
    print("%s %-58s v%s -> v%s  (%s)" % ("ESCRIBE " if escribe else "ensayo  ", d, m.group(1), NUEVA, tipo))
    if escribe:
        io.open(ruta, "w", encoding="utf-8", newline="").write(t2)

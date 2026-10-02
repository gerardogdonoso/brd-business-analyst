# -*- coding: utf-8 -*-
"""Sube la estampa `Al día con BRD: vX.YY` de los derivados que docs-fresh marca (ERROR de herencia fina y AVISO
«ningun ID que cita cambio») a la v5.98, tras el barrido de frases del bloque DZ.
Documento con nota en la estampa: la nota se REEMPLAZA por la de este script. Sin nota: solo cambia la version.
Uso: python restampa3.py [--escribir]"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
R = r"C:\Users\User\Projects\agentesIA"
NUEVA = "5.99"
escribe = "--escribir" in sys.argv

fresh = io.open(os.path.join(SP, "fresh-lineas.txt"), encoding="utf-8").read()
docs = []
for m in re.finditer(r"ERROR\s+Herencia fina: (\S+) se estampa", fresh):
    docs.append(m.group(1))
for m in re.finditer(r"AVISO\s+Herencia: (\S+) dice 'Al dia con BRD: v5\.98'", fresh):
    docs.append(m.group(1))
docs = [d for d in dict.fromkeys(docs)]

# lineas que nombro el control, por documento
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
CORREGIDOS = {}
SIN_NOTA = {"docs/BRD-evidencia.md", "docs/BRD-historial.md", "docs/correcciones-brd-pendientes.md", "docs/specs/001-primer-camino/requisitos.md"}
EST = re.compile(r"Al d[ií]a con BRD: v([\d.]+)\*\*")


def nota(n, c):
    if n == 0:
        return "*(re-estampado el 02-10-2026 contra la v5.99: el control no halló ningún elemento citado por el documento que haya cambiado desde la v5.98)*"
    return ("*(re-estampado el 02-10-2026 contra la v5.99: se barrieron en el documento entero, con dos juegos de palabras, las frases que corrigen los once criterios de la v5.99 "
            "—escenario de la cuenta, fusión entre activos de una misma cuenta, oferta de reagendar, consentimiento por número, campaña de Fidelización sin playbook, cierre tras las dos respuestas de ayuda, "
            "campos vacíos de la ficha, entrada de `Ármalo` sin medidor y listas de objeciones de Fidelización— y no se halló ningún tramo que las repita; el control nombró %d líneas y no se releyeron "
            "una por una: las que no repiten esas frases citan criterios cuyo texto cambió en lo que ninguna de ellas afirma; el detalle está en el commit de la v5.99)*" % n)


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
        t2 = t[:m.start()] + "Al día con BRD: v%s** %s" % (NUEVA, nota(cuenta.get(d, 0), 0)) + t[fin_texto:]
        tipo = "nota %d" % cuenta.get(d, 0)
    print("%s %-58s v%s -> v%s  (%s)" % ("ESCRIBE " if escribe else "ensayo  ", d, m.group(1), NUEVA, tipo))
    if escribe:
        io.open(ruta, "w", encoding="utf-8", newline="").write(t2)

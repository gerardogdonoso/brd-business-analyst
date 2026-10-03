"""cuadro_cierre.py -- las cifras del cuadro de cierre de SKILL.md §12, contadas por ELEMENTO y no por etiqueta (03-10-2026).

Una fila de §1 a §15 = un elemento, con el estado de su celda; los criterios (CA), que no traen celda de estado, toman el
del §16 con sus rangos expandidos. Dos analizadores independientes que se comparan: si no coinciden, no se publica la
cifra. Medido en la v5.107: 1.737 elementos, los dos coinciden. Trae la ruta del BRD de esa maquina: se adapta.
"""
import io, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
# Cuadro de cierre: ELEMENTOS de §1 a §15 contados por fila unica, estado = el de su celda; los criterios (CA), que no
# tienen celda de estado, toman el del §16 (rangos expandidos). Dos analizadores independientes que se comparan.
R = r"C:\Users\User\Projects\agentesIA\docs\BRD.md"
t = io.open(R, encoding="utf-8").read()
cuerpo = re.split(r"(?m)^## .*Historial de cambios.*$", t, maxsplit=1)[0]
ID = r"(?:OB|AL(?:-F)?|AC(?:-ECO|-REG)?|PR(?:-ALT|-EXC)?|RN|DA(?:-IN|-OUT|-CON|-EST)?|CB|CE|RE|SA|RG|PE|BN|CA|INV|PZ)-\d{2,4}"
ESTADOS = ["CONFIRMADO", "SUPUESTO", "INVESTIGADO", "DERIVADO", "DUDA", "PENDIENTE-INVESTIGACION", "PENDIENTE",
           "BLOQUEO-DE-NEGOCIO", "RIESGO-CONTROLADO", "RIESGO", "A CALIBRAR"]

# ---- el mapa del §16 (expandiendo rangos y listas)
i16 = cuerpo.index("\n## 16.")
i17 = cuerpo.index("\n## 17.")
m16 = {}
for l in cuerpo[i16:i17].split("\n"):
    p = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(p) != 3 or not p[1].startswith("§"):
        continue
    mt = re.search(r"\[([A-ZÁÉÍÓÚÑ\- ]+?)(?::[^\]]*)?\]", p[2])
    tag = mt.group(1) if mt else None
    if not tag:
        continue
    ids = []
    for trozo in re.split(r",\s*", p[0]):
        mr = re.match(r"^([A-Z]+(?:-[A-Z]+)*)-(\d+) a (?:[A-Z]+(?:-[A-Z]+)*-)?(\d+)$", trozo)
        if mr:
            a, b = int(mr.group(2)), int(mr.group(3))
            ids += ["%s-%03d" % (mr.group(1), n) if len(mr.group(2)) == 3 else "%s-%d" % (mr.group(1), n) for n in range(a, b + 1)]
        else:
            ids.append(trozo)
    for x in ids:
        m16.setdefault(x, tag)

# ---- analizador A: celdas de la fila, de derecha a izquierda
A = {}
for linea in cuerpo.split("\n"):
    m = re.match(r"^\|\s*(%s)\s*\|\s*([^|]*)" % ID, linea)
    if not m or m.group(2).strip().startswith("§"):
        continue
    eid = m.group(1)
    if eid in A:
        continue
    est = None
    for celda in reversed([c.strip().strip("`").strip() for c in linea.split("|")]):
        mc = re.fullmatch(r"\[([A-Z \-]+?)(?::[^\]]*)?\]", celda)
        if mc and mc.group(1) in ESTADOS:
            est = mc.group(1)
            break
    A[eid] = est

# ---- analizador B: expresion regular sobre el final de la fila
B = {}
rx = re.compile(r"\|\s*`?\[(%s)(?::[^\]]*)?\]`?\s*(?=\|)" % "|".join(sorted(ESTADOS, key=len, reverse=True)))
for linea in cuerpo.split("\n"):
    m = re.match(r"^\|\s*(%s)\s*\|\s*([^|]*)" % ID, linea)
    if not m or m.group(2).strip().startswith("§"):
        continue
    eid = m.group(1)
    if eid in B:
        continue
    ms = rx.findall(linea)
    B[eid] = ms[-1] if ms else None


def cuenta(M):
    c = Counter()
    de16 = 0
    sin = 0
    for eid, est in M.items():
        if est is None:
            est = m16.get(eid)
            if est:
                de16 += 1
        if est is None:
            sin += 1
            est = "(sin estado)"
        c[est] += 1
    return c, de16, sin


cA, dA, sA = cuenta(A)
cB, dB, sB = cuenta(B)
print("A: %d elementos (%d con el estado tomado del 16, %d sin estado)" % (len(A), dA, sA))
print("   ", dict(cA.most_common()))
print("B: %d elementos (%d con el estado tomado del 16, %d sin estado)" % (len(B), dB, sB))
print("   ", dict(cB.most_common()))
print("coinciden los dos:", cA == cB)
dif = [e for e in A if A[e] != B.get(e)]
print("elementos en que difieren:", len(dif), dif[:10])
print("PE abiertos (13):", sum(1 for l in cuerpo.split("\n") if re.match(r"^\| PE-\d+ \|", l) and "✅" not in l[:40]),
      " de ", sum(1 for l in cuerpo.split("\n") if re.match(r"^\| PE-\d+ \|", l)))
print("marcas [A CALIBRAR] y [NO EXIGIBLE] abiertas en §1-§15:", len(re.findall(r"\[(?:A CALIBRAR|NO EXIGIBLE)", cuerpo[:cuerpo.index("\n## 16.")])))

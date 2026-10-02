# -*- coding: utf-8 -*-
"""Saca de las filas de §19 (BRD + historial) los IDs que cada version v5.59..v5.83 toco.
Salida: lista_cambiados.json con {version: {nuevos, modificados, revisados}} y la union.
Cuenta: lo que la columna «IDs afectados» nombra como Nuevos / Modificados / Criterios revisados sin cambio;
expande los rangos «CA-X a CA-Y» y «CA-X, ..., CA-Y». NO cuenta los IDs que aparecen solo en la columna Motivo."""
import io, json, re, sys, os
sys.path.insert(0, r"C:\Users\User\Projects\agentesIA\tools")

RAIZ = r"C:\Users\User\Projects\agentesIA"
PREF = (r'AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|'
        r'OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|INV|NT|DE')
TOK = re.compile(r'\b((?:%s))-(\d{3})\b' % PREF)
RANGO = re.compile(r'\b((?:%s))-(\d{3})\s+a\s+((?:%s))-(\d{3})\b' % (PREF, PREF))

def ids_de(texto):
    out = []
    # rangos primero
    def expande(m):
        p1, a, p2, b = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
        if p1 == p2 and b >= a and b - a < 400:
            for n in range(a, b + 1):
                out.append("%s-%03d" % (p1, n))
        return " "
    resto = RANGO.sub(expande, texto)
    for m in TOK.finditer(resto):
        out.append("%s-%s" % (m.group(1), m.group(2)))
    return out

def parte(celda, clave_ini, claves_todas):
    # devuelve el texto de la celda desde «**clave:**» hasta la siguiente clave
    pat = re.compile(r'\*\*(%s):\*\*' % "|".join(re.escape(c) for c in claves_todas))
    marcas = [(m.start(), m.end(), m.group(1)) for m in pat.finditer(celda)]
    out = ""
    for i, (s, e, nombre) in enumerate(marcas):
        fin = marcas[i + 1][0] if i + 1 < len(marcas) else len(celda)
        if nombre == clave_ini:
            out += celda[e:fin] + " "
    return out

LO = float(os.environ.get('LO','5.59')); HI = float(os.environ.get('HI','5.83'))
SALIDA = os.environ.get('SALIDA','lista_cambiados.json')
CLAVES = ["Nuevos", "Modificados", "Criterios revisados sin cambio", "Derogados", "Derogado", "Revisados sin cambio"]

filas = {}
for ruta in ("docs/BRD.md", "docs/BRD-historial.md"):
    with io.open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
        for ln in f:
            if not ln.startswith("| 2026-"):
                continue
            celdas = ln.split("|")
            if len(celdas) < 6:
                continue
            ver = celdas[2].strip()
            if not re.match(r'^5\.\d\d$', ver):
                continue
            filas.setdefault(ver, {"fecha": celdas[1].strip(), "fuente": ruta, "celda": celdas[3]})

res = {}
for ver in sorted(filas, key=lambda v: float(v)):
    n = float(ver)
    if not (LO <= n <= HI):
        continue
    c = filas[ver]["celda"]
    res[ver] = {
        "fecha": filas[ver]["fecha"],
        "fuente": filas[ver]["fuente"],
        "nuevos": sorted(set(ids_de(parte(c, "Nuevos", CLAVES)))),
        "modificados": sorted(set(ids_de(parte(c, "Modificados", CLAVES)))),
        "revisados": sorted(set(ids_de(parte(c, "Criterios revisados sin cambio", CLAVES) + parte(c, "Revisados sin cambio", CLAVES)))),
        "derogados": sorted(set(ids_de(parte(c, "Derogados", CLAVES) + parte(c, "Derogado", CLAVES)))),
        "largo_celda": len(c),
    }

print("versiones halladas:", len(res), "rango", LO, HI)
faltan = [("5.%d" % k) for k in range(59, 84) if ("5.%d" % k) not in res]
print("faltan:", faltan)
for v, d in res.items():
    print(v, d["fecha"], d["fuente"].split("/")[-1], "nuevos=%d modificados=%d revisados=%d derogados=%d celda=%d" % (
        len(d["nuevos"]), len(d["modificados"]), len(d["revisados"]), len(d["derogados"]), d["largo_celda"]))

union_n = sorted(set(i for d in res.values() for i in d["nuevos"]))
union_m = sorted(set(i for d in res.values() for i in d["modificados"]))
union = sorted(set(union_n) | set(union_m))
print("union nuevos+modificados:", len(union), "(nuevos %d, modificados %d)" % (len(union_n), len(union_m)))
destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), SALIDA)
with io.open(destino, "w", encoding="utf-8") as f:
    json.dump({"por_version": res, "union": union, "nuevos": union_n, "modificados": union_m}, f, ensure_ascii=False, indent=1)
print("guardado en", destino)

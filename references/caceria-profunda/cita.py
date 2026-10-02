# -*- coding: utf-8 -*-
"""cita.py A B — dice si el elemento A cita a B, si B cita a A, y que criterios (CA) prueban a los dos.
Es la unica comprobacion de «se citan o no se citan»: la hace el instrumento, no el lector.
Uso: python cita.py RN-123 CA-456 [RN-789 ...]   (todos los pares entre los IDs dados)"""
import io, json, os, sys, itertools
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CITAS, ENT = D["elementos"], D["citas"], D["entrantes"]
ids = [a for a in sys.argv[1:] if not a.startswith("-")]
if len(ids) < 2:
    print(__doc__); sys.exit(1)
for a in ids:
    if a not in E:
        print("%s: NO es un elemento vivo del BRD (puede estar derogado: python tools/historia.py %s)" % (a, a))
for a, b in itertools.combinations([i for i in ids if i in E], 2):
    ab = b in CITAS.get(a, []); ba = a in CITAS.get(b, [])
    comunes = sorted(set(ENT.get(a, [])) & set(ENT.get(b, [])))
    print("%s <-> %s: %s cita a %s: %s; %s cita a %s: %s; comparten %d elemento(s) que los citan a los dos%s" % (
        a, b, a, b, "SI" if ab else "no", b, a, "SI" if ba else "no", len(comunes),
        (": " + ", ".join(comunes[:8])) if comunes else ""))

# -*- coding: utf-8 -*-
"""mide_relectura.py - tamano de la relectura bidireccional (§11 (4-bis)) de los 114 cambiados: cuantos vecinos y cuantos caracteres."""
import io, json, os
SP = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CITAS, ENT, CAMBIO = D["elementos"], D["citas"], D["entrantes"], D["cambio_en"]
cam = sorted(i for i in CAMBIO if i in E)
pares = set(); vec = set()
for t in cam:
    for v in set(CITAS.get(t, [])) | set(ENT.get(t, [])):
        pares.add(tuple(sorted((t, v)))); vec.add(v)
solo_vec = vec - set(cam)
print("cambiados vivos:", len(cam), "; chars de los cambiados:", sum(len(E[i]) for i in cam) // 1024, "KB")
print("pares cambiado-vecino (sin orden):", len(pares))
print("vecinos unicos:", len(vec), "; de ellos NO cambiados:", len(solo_vec), "; chars de esos vecinos:", sum(len(E[i]) for i in solo_vec) // 1024, "KB")
grandes = sorted(cam, key=lambda t: -(len(CITAS.get(t, [])) + len(ENT.get(t, []))))[:12]
print("cambiados con mas vecinos:", ", ".join("%s(%d)" % (t, len(set(CITAS.get(t, [])) | set(ENT.get(t, [])))) for t in grandes))

# pares cuyo cambiado y vecino cayeron en paquetes DISTINTOS: nunca estuvieron en la cabeza de un mismo lector
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
paq = {i: p["lente"] for p in P["paquetes"] for g in p["grupos"] for i in g["ids"]}
cruz = [(a, b) for a, b in pares if paq[a] != paq[b]]
print("pares en paquetes distintos:", len(cruz), "de", len(pares))
import re
def cabeza(t, n=350):
    return t[:n]
vec_cruz = set()
for a, b in cruz:
    t, v = (a, b) if a in CAMBIO else (b, a)
    vec_cruz.add(v)
print("vecinos de pares cruzados:", len(vec_cruz), "; chars enteros:", sum(len(E[i]) for i in vec_cruz) // 1024, "KB; cabezas de 350:", sum(min(350, len(E[i])) for i in vec_cruz) // 1024, "KB")
# sin contar los criterios CA que citan al cambiado (esos los cubre la regla 'la correccion baja a la prueba' y prueba-rezagada)
sin_ca = [(a, b) for a, b in cruz if not ((a in CAMBIO and b.startswith("CA-")) or (b in CAMBIO and a.startswith("CA-")))]
print("pares cruzados sin contar CA vecinos:", len(sin_ca))

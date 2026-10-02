# -*- coding: utf-8 -*-
"""leer.py — entrega a un lector el siguiente lote de elementos del BRD de su paquete, en TEXTO (sin vecindario),
y anota en un registro que se imprimio. Uso:
    python leer.py L1              # el siguiente lote (lleva la cuenta solo)
    python leer.py L1 --estado     # cuantos lotes y elementos van
    python leer.py L1 --lote 4     # vuelve a imprimir el lote 4 (no suma al registro)
Cada elemento sale con: ID, en que versiones cambio (si cambio desde la ultima lectura entera), a quien cita y quien lo cita.
Lo impreso NO prueba lo leido: el lector declara aparte lo que leyo con atencion."""
import io, json, os, sys, time

SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TOPE = 22000  # caracteres por lote: bajo el corte de ~30.000 de la herramienta de shell

SUF = os.environ.get("LEER_SUFIJO", "")
P = json.load(io.open(os.path.join(SP, "paquetes%s.json" % SUF), encoding="utf-8"))
D = json.load(io.open(os.path.join(SP, "elementos%s.json" % SUF), encoding="utf-8"))
E, CITAS, ENT, CAMBIO = D["elementos"], D["citas"], D["entrantes"], D["cambio_en"]

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)
lente = sys.argv[1]
paq = next((p for p in P["paquetes"] if p["lente"] == lente), None)
if paq is None:
    print("lente desconocida:", lente); sys.exit(1)

def lista(ids, tope=10):
    ids = list(ids)
    if not ids:
        return "ninguno"
    if len(ids) <= tope:
        return ", ".join(ids)
    return ", ".join(ids[:tope]) + " (+%d mas)" % (len(ids) - tope)

# lotes: se llenan por grupos completos hasta el tope; un grupo mas grande que el tope se parte por elementos
lotes = []; actual = []; chars = 0
for g in paq["grupos"]:
    bloque = []
    for i in g["ids"]:
        bloque.append(i)
    for i in bloque:
        n = len(E[i]) + 200
        if actual and chars + n > TOPE:
            lotes.append(actual); actual = []; chars = 0
        actual.append(i); chars += n
    # al terminar un grupo, si el lote ya pasa de la mitad se cierra para no mezclar temas lejanos
    if chars > TOPE * 0.6:
        lotes.append(actual); actual = []; chars = 0
if actual:
    lotes.append(actual)

estado_f = os.path.join(SP, "estado_%s.json" % lente)
log_f = os.path.join(SP, "leido_%s.log" % lente)
estado = json.load(io.open(estado_f, encoding="utf-8")) if os.path.exists(estado_f) else {"siguiente": 0}

def imprime(k):
    ids = lotes[k]
    print("=== %s · LOTE %d de %d · %d elementos ===" % (lente, k + 1, len(lotes), len(ids)))
    print("(cada elemento: ID · versiones en que cambio desde la ultima lectura entera · CITA A · LO CITAN)\n")
    for i in ids:
        cam = CAMBIO.get(i)
        marca = " · CAMBIO en v" + ", v".join(sorted(cam, key=float)) if cam else ""
        print("### %s%s" % (i, marca))
        print("cita a: %s | lo citan: %s" % (lista(CITAS.get(i, [])), lista(ENT.get(i, []), 8)))
        print(E[i])
        print()

if "--marco" in sys.argv:
    # el marco que MANDA: las nueve notas de vocabulario (NT-) y las tres relaciones del dueño
    import re
    n = sys.argv[sys.argv.index("--marco") + 1]
    if n == "1":
        print("=== MARCO 1 de 2 · LAS NUEVE NOTAS DE VOCABULARIO (NT-001 a NT-009), texto integro de docs/BRD.md ===\n")
        for k, ln in enumerate(io.open(r"C:\Users\User\Projects\agentesIA\docs\BRD.md", encoding="utf-8"), 1):
            if ln.startswith("## 16."):
                break
            if re.match(r"^>\s*\[NT-\d{3}\]", ln):
                print(ln.rstrip("\n")); print()
    else:
        print("=== MARCO 2 de 2 · LAS TRES RELACIONES QUE MANDAN: RN-380 (mapa de entidades), RN-362 (Propietario y Asignado), RN-311 (niveles) ===\n")
        for i in ("RN-380", "RN-362", "RN-311"):
            print("### %s\n%s\n" % (i, E[i]))
    sys.exit(0)

if "--estado" in sys.argv:
    leidos =sum(len(lotes[k]) for k in range(estado["siguiente"]))
    print("%s: lote siguiente %d de %d; impresos %d de %d elementos" % (lente, estado["siguiente"] + 1, len(lotes), leidos, paq["n"]))
    sys.exit(0)

if "--lote" in sys.argv:
    k = int(sys.argv[sys.argv.index("--lote") + 1]) - 1
    imprime(k)
    sys.exit(0)

k = estado["siguiente"]
if k >= len(lotes):
    print("FIN: ya se imprimieron los %d lotes de %s (%d elementos). Escribe tu informe final." % (len(lotes), lente, paq["n"]))
    sys.exit(0)
imprime(k)
with io.open(log_f, "a", encoding="utf-8") as f:
    f.write("%s\tlote %d\t%s\t%s\n" % (time.strftime("%H:%M:%S"), k + 1, len(lotes[k]), " ".join(lotes[k])))
estado["siguiente"] = k + 1
json.dump(estado, io.open(estado_f, "w", encoding="utf-8"))
print("--- fin del lote %d de %d. %s ---" % (k + 1, len(lotes), "Pide el siguiente con: python leer.py %s" % lente if k + 1 < len(lotes) else "ULTIMO lote: despues escribe tu informe final."))

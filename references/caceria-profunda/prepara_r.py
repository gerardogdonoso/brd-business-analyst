# -*- coding: utf-8 -*-
"""prepara_r.py — la RELECTURA BIDIRECCIONAL (§11 (4-bis) de la skill del BRD) de lo que tocaron las v5.96 a v5.108,
como etapa aparte de la caceria (las corridas del 01-10 y del 02-10 declararon que no la hicieron).
Por cada elemento vivo que cambio desde la v5.95: (1) LO QUE CAMBIO, como diferencia de palabras contra el BRD del commit
c7f8ef4 (la v5.95); (2) su texto entero de hoy; (3) la CABEZA (primeros CAB caracteres) de cada vecino —a quien cita y quien
lo cita— que cayo en OTRO paquete de lectura: esos pares nunca estuvieron en la cabeza de un mismo lector.
Cuenta: pares por citas dentro de §1-§15 (las que trae elementos.json). Deja fuera: los pares del mismo paquete (los ve el
lector de ese paquete) y lo que no se cita (lo ve el cruce). Una entrada que pasaria de MAXE caracteres se parte en
«ID·2», «ID·3»… que repiten la diferencia y la cabeza del cambiado, no el texto entero.
Salida: paquetes_r.json y elementos_r.json, para leer_r.py (leer.py con LEER_SUFIJO=_r)."""
import difflib, io, json, os, re, subprocess, sys
SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun

BASE = "c7f8ef4"
CAB = 300
MAXE = 19000
NPAQ = int(sys.argv[1]) if len(sys.argv) > 1 else 2

D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CITAS, ENT, CAMBIO = D["elementos"], D["citas"], D["entrantes"], D["cambio_en"]
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
paq, orden, grupo_de = {}, {}, {}
k = 0
for p in P["paquetes"]:
    for g in p["grupos"]:
        for i in g["ids"]:
            paq[i] = p["lente"]; orden[i] = k; grupo_de[i] = (p["lente"], g["id_grupo"]); k += 1

def filas(texto):
    out = {}
    for ln in texto.split("\n"):
        if ln.startswith("## 16."):
            break
        d = comun.definicion(ln.rstrip("\r"))
        if d and d[0] not in out:
            f = d[1].rstrip()
            out[d[0]] = (f[:-1].rstrip() if f.endswith("|") else f).strip()
    return out

viejo = filas(subprocess.run(["git", "-C", RAIZ, "show", "%s:docs/BRD.md" % BASE], capture_output=True).stdout.decode("utf-8"))

def diferencia(a, b, ctx=8):
    """[-quitado-] y {+agregado+} con ctx palabras de contexto; los tramos iguales largos se resumen con «(…)»."""
    wa, wb = a.split(), b.split()
    sm = difflib.SequenceMatcher(a=wa, b=wb, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            seg = wa[i1:i2]
            if len(seg) > 2 * ctx:
                out.append(" ".join(seg[:ctx]) + " (…) " + " ".join(seg[-ctx:]))
            else:
                out.append(" ".join(seg))
        else:
            if i2 > i1:
                out.append("[-" + " ".join(wa[i1:i2]) + "-]")
            if j2 > j1:
                out.append("{+" + " ".join(wb[j1:j2]) + "+}")
    return " ".join(out)

cam = sorted((i for i in CAMBIO if i in E), key=lambda i: orden[i])
items, citas_r, ent_r, cambio_r, grupos = {}, {}, {}, {}, {}
n_pares = 0
for t in cam:
    if t in viejo:
        dif = diferencia(viejo[t], E[t])
        dif_txt = "LO QUE CAMBIÓ desde la v5.95 ([-quitado-] {+agregado+}; «(…)» resume texto igual):\n" + dif
    else:
        dif_txt = "LO QUE CAMBIÓ desde la v5.95: el elemento es NUEVO (no existía en la v5.95)."
    vec = []
    for v in CITAS.get(t, []):
        if paq.get(v) != paq[t]:
            vec.append(("cita a", v))
    for v in ENT.get(t, []):
        if paq.get(v) != paq[t] and v not in CITAS.get(t, []):
            vec.append(("lo cita", v))
    vec.sort(key=lambda x: (x[0] != "cita a", orden.get(x[1], 99999)))
    n_pares += len(vec)
    lineas = ["- [%s] %s (paquete %s%s): %s%s" % (r, v, paq.get(v, "?"), ", CAMBIÓ también" if v in CAMBIO else "",
              E[v][:CAB].replace("\n", " "), "…" if len(E[v]) > CAB else "") for r, v in vec]
    cab_vec = "VECINOS EN OTROS PAQUETES (%d; cabeza de %d caracteres de cada uno; el texto entero con python tools/elemento.py <ID> --solo-texto):" % (len(vec), CAB)
    cuerpo = dif_txt + "\n\nTEXTO DE HOY:\n" + E[t] + "\n\n" + cab_vec
    partes, actual, largo = [], [], len(cuerpo)
    for ln in lineas:
        if actual and largo + len(ln) + 1 > MAXE:
            partes.append(actual); actual = []
            largo = len(dif_txt) + 1600
        actual.append(ln); largo += len(ln) + 1
    partes.append(actual)
    lg = grupo_de[t]
    for j, pl in enumerate(partes, 1):
        clave = t if j == 1 else "%s·%d" % (t, j)
        if j == 1:
            txt = cuerpo + "\n" + ("\n".join(pl) if pl else "(ninguno: todos sus vecinos están en su mismo paquete)")
        else:
            txt = (dif_txt + "\n\nCABEZA DE HOY (el texto entero salió en la parte 1; o python tools/elemento.py %s --solo-texto):\n%s…\n\n" % (t, E[t][:1500])
                   + cab_vec.replace("VECINOS EN OTROS PAQUETES", "VECINOS EN OTROS PAQUETES, parte %d de %d" % (j, len(partes))) + "\n" + "\n".join(pl))
        items[clave] = txt
        citas_r[clave] = CITAS.get(t, []); ent_r[clave] = ENT.get(t, []); cambio_r[clave] = CAMBIO[t]
        grupos.setdefault(lg, []).append(clave)

vol = {g: sum(len(items[i]) + 200 for i in ids) for g, ids in grupos.items()}
total = sum(vol.values()); objetivo = total / NPAQ
paqs, acum = [[]], 0
for g in grupos:  # en el orden de los paquetes de la primera etapa: el tema queda junto
    if acum >= objetivo * len(paqs) and len(paqs) < NPAQ:
        paqs.append([])
    paqs[-1].append(g); acum += vol[g]
salida = {"paquetes": []}
for n, lista in enumerate(paqs, 1):
    gs = [{"id_grupo": "%s-%s" % g, "nombre": "cambiados del paquete %s, grupo %s" % g, "ids": grupos[g]} for g in lista]
    nid = sum(len(x["ids"]) for x in gs)
    salida["paquetes"].append({"lente": "R%d" % n, "grupos": gs, "n": nid, "chars": sum(vol[g] for g in lista),
                               "n_cambiados": len({i.split("·")[0] for x in gs for i in x["ids"]})})
    print("R%d: %d entradas (%d cambiados), %d KB" % (n, nid, salida["paquetes"][-1]["n_cambiados"], salida["paquetes"][-1]["chars"] // 1024))
json.dump(salida, io.open(os.path.join(SP, "paquetes_r.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"elementos": items, "citas": citas_r, "entrantes": ent_r, "cambio_en": cambio_r, "orden": list(items)},
          io.open(os.path.join(SP, "elementos_r.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("cambiados vivos: %d; nuevos (sin texto en la v5.95): %d; pares cambiado-vecino en paquetes distintos: %d; entradas: %d (partidas: %d); entrada mas larga: %d caracteres" % (
    len(cam), sum(1 for t in cam if t not in viejo), n_pares, len(items), sum(1 for i in items if "·" in i), max(len(x) for x in items.values())))

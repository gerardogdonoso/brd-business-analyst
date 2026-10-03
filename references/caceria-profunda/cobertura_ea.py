# -*- coding: utf-8 -*-
"""cobertura_ea.py - cobertura de la corrida del 03-10-2026 (bloque EA), declarada y medida.
IMPRESO: lo mide el registro de leer.py / leer_r.py / leer_x.py (leido_*.log: por lote, los IDs que imprimio).
LEIDO RAPIDO / A MEDIA ATENCION: lo declara cada lector en su informe (informes.json, numeros de lote).
FICHADO: elementos con una linea de ficha en fichas_L*.md.
Las entradas de la relectura R se nombran ID, ID·2, ID·3... cuando un cambiado tenia tantos vecinos que no cabian
en un lote: aqui se cuentan por el ID base."""
import io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CAMBIO = D["elementos"], D["cambio_en"]
INF = json.load(io.open(os.path.join(SP, "informes.json"), encoding="utf-8"))
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
tam = {p["lente"]: p["n"] for p in P["paquetes"]}
LC = json.load(io.open(os.path.join(SP, "lista_cambiados.json"), encoding="utf-8"))

IDL = re.compile(r'^[\s>*\-`]*((?:AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT)-\d{3})[`\s]*\|')

def lotes_de(L):
    lotes = {}
    for ln in io.open(os.path.join(SP, "leido_%s.log" % L), encoding="utf-8"):
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 4:
            lotes[int(c[1].split()[1])] = [re.sub(r"\W\d+$", "", i) if "·" in i else i for i in c[3].split()]
    return lotes

def base(i):
    return i.split("·")[0]

out = {}
print("== ETAPA 1: cinco lectores por tema ==")
vistos = set(); rap_t = set(); med_t = set(); fich_t = set()
for L in ("L1", "L2", "L3", "L4", "L5"):
    lotes = lotes_de(L)
    imp = {i for v in lotes.values() for i in v}
    rap = {i for k in INF[L].get("rapido", []) for i in lotes.get(k, [])}
    med = {i for k in INF[L].get("media", []) for i in lotes.get(k, [])} - rap
    fich = set()
    for ln in io.open(os.path.join(SP, "fichas_%s.md" % L), encoding="utf-8"):
        m = IDL.match(ln)
        if m and m.group(1) in E:
            fich.add(m.group(1))
    print("%s: %d de %d impresos en %d lotes; rapido %d (lotes %s); media %d (lotes %s); fichados %d; cambiados impresos %d, en lotes rapidos %d" % (
        L, len(imp), tam[L], len(lotes), len(rap), INF[L].get("rapido", []), len(med), INF[L].get("media", []), len(fich),
        sum(1 for i in imp if i in CAMBIO), sum(1 for i in rap if i in CAMBIO)))
    vistos |= imp; rap_t |= rap; med_t |= med; fich_t |= fich
med_t -= rap_t
n = len(E)
print("TOTAL L: %d impresos de %d vivos (%.1f%%); %d en lotes leidos rapido (%.1f%%); %d a media atencion (%.1f%%); %d fichados (%.1f%%)" % (
    len(vistos), n, 100.0 * len(vistos) / n, len(rap_t), 100.0 * len(rap_t) / n, len(med_t), 100.0 * len(med_t) / n, len(fich_t), 100.0 * len(fich_t) / n))
camb = [i for i in E if i in CAMBIO]
print("cambiados vivos en elementos.json: %d; impresos %d; en lotes rapidos %d; a media %d" % (
    len(camb), sum(1 for i in camb if i in vistos), sum(1 for i in camb if i in rap_t), sum(1 for i in camb if i in med_t)))
faltan = sorted(set(E) - vistos)
print("vivos NO impresos por ningun L: %d %s" % (len(faltan), faltan[:20]))
out["L"] = {"impresos": len(vistos), "vivos": n, "rapido": len(rap_t), "media": len(med_t), "fichados": len(fich_t),
            "cambiados": len(camb), "cambiados_rapido": sum(1 for i in camb if i in rap_t),
            "cambiados_media": sum(1 for i in camb if i in med_t), "no_impresos": faltan}

print("\n== ETAPA 2: relectura bidireccional (cambiado + vecinos de otro paquete) ==")
r_imp = set(); r_rap = set(); r_med = set()
for L in ("R1", "R2", "R3"):
    lotes = lotes_de(L)
    imp = {base(i) for v in lotes.values() for i in v}
    rap = {base(i) for k in INF[L].get("rapido", []) for i in lotes.get(k, [])}
    med = {base(i) for k in INF[L].get("media", []) for i in lotes.get(k, [])} - rap
    print("%s: %d cambiados impresos en %d lotes; en lotes rapidos %d (lotes %s); a media %d (lotes %s)" % (
        L, len(imp), len(lotes), len(rap), INF[L].get("rapido", []), len(med), INF[L].get("media", [])))
    r_imp |= imp; r_rap |= rap; r_med |= med
r_med -= r_rap
print("TOTAL R: %d cambiados impresos; %d en lotes rapidos; %d a media" % (len(r_imp), len(r_rap), len(r_med)))
out["R"] = {"impresos": len(r_imp), "rapido": len(r_rap), "media": len(r_med)}

print("\n== ETAPA 3: cruce de fichas ==")
for L in ("X1", "X2"):
    lotes = lotes_de(L)
    imp = {i for v in lotes.values() for i in v}
    rap = {i for k in INF[L].get("rapido", []) for i in lotes.get(k, [])}
    den = {i for k in INF[L].get("densos_misma_pasada", []) for i in lotes.get(k, [])}
    print("%s: %d entradas impresas en %d lotes; en lotes rapidos %d (lotes %s); en lotes densos declarados %d" % (
        L, len(imp), len(lotes), len(rap), INF[L].get("rapido", []), len(den)))
json.dump(out, io.open(os.path.join(SP, "cobertura_ea.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

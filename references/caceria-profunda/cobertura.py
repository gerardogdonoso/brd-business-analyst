# -*- coding: utf-8 -*-
"""cobertura.py - cobertura de la etapa 1, declarada y medida.
IMPRESO: lo mide leer.py (leido_L*.log guarda, por lote, los IDs que imprimio).
LEIDO RAPIDO: lo declara cada lector en su informe (numeros de lote); aqui se transforma en elementos.
FICHADO: elementos con una linea de ficha en fichas_L*.md."""
import io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = json.load(io.open(os.path.join(SP, "elementos.json"), encoding="utf-8"))
E, CAMBIO = D["elementos"], D["cambio_en"]
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
tam = {p["lente"]: p["n"] for p in P["paquetes"]}

# lo que cada lector declaro en su informe final (numeros de lote)
RAPIDO = {"L1": [17, 18, 19], "L2": [3, 5, 7, 10, 12], "L3": [7, 14, 15, 16, 18, 20],
          "L4": [12, 14, 15, 16, 17, 18], "L5": [4, 5, 8, 10, 12, 15, 19, 21, 22, 23, 24, 25]}
MEDIA = {"L1": [11, 12, 20], "L2": [20, 21], "L3": [], "L4": [], "L5": []}

IDL = re.compile(r'^[\s>*\-`]*((?:AL-F|DA-IN|DA-OUT|DA-CON|DA-EST|AC-ECO|AC-REG|PR-ALT|PR-EXC|OB|AL|AC|PR|RN|CB|CE|PZ|RE|SA|RG|PE|BN|CA|NT)-\d{3})[`\s]*\|')
tot_imp = tot_rap = tot_fich = 0
rap_cambiados = 0; vistos = set(); fichados = set(); rapidos = set()
for L in sorted(RAPIDO):
    lotes = {}
    for ln in io.open(os.path.join(SP, "leido_%s.log" % L), encoding="utf-8"):
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 4:
            lotes[int(c[1].split()[1])] = c[3].split()
    imp = {i for v in lotes.values() for i in v}
    rap = {i for k in RAPIDO[L] for i in lotes.get(k, [])}
    fich = set()
    for ln in io.open(os.path.join(SP, "fichas_%s.md" % L), encoding="utf-8"):
        m = IDL.match(ln)
        if m and m.group(1) in E:
            fich.add(m.group(1))
    print("%s: %d de %d impresos en %d lotes; %d elementos en lotes que el lector leyo RAPIDO (%d%%); %d fichados (%d%%); cambiados desde v5.83: %d, de ellos en lotes rapidos: %d" % (
        L, len(imp), tam[L], len(lotes), len(rap), 100 * len(rap) // max(1, len(imp)), len(fich), 100 * len(fich) // max(1, len(imp)),
        sum(1 for i in imp if i in CAMBIO), sum(1 for i in rap if i in CAMBIO)))
    vistos |= imp; fichados |= fich; rapidos |= rap
print("TOTAL: %d impresos de %d vivos; %d en lotes leidos rapido (%d%%); %d fichados (%d%%); cambiados %d de los cuales rapido %d" % (
    len(vistos), len(E), len(rapidos), 100 * len(rapidos) // len(E), len(fichados), 100 * len(fichados) // len(E),
    sum(1 for i in vistos if i in CAMBIO), sum(1 for i in rapidos if i in CAMBIO)))
json.dump({"rapidos": sorted(rapidos), "fichados": sorted(fichados)}, io.open(os.path.join(SP, "cobertura.json"), "w", encoding="utf-8"))

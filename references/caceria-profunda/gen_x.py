# -*- coding: utf-8 -*-
"""gen_x.py - escribe encargo_X1..Xk.md desde encargo_X.md con {L} y el numero real de fichas de cada paquete del cruce."""
import io, json, os
SP = os.path.dirname(os.path.abspath(__file__))
base = io.open(os.path.join(SP, "encargo_X.md"), encoding="utf-8").read()
P = json.load(io.open(os.path.join(SP, "paquetes_x.json"), encoding="utf-8"))
for p in P["paquetes"]:
    t = base.replace("{L}", p["lente"]).replace("unas 540 fichas", "unas %d fichas" % p["n"])
    io.open(os.path.join(SP, "encargo_%s.md" % p["lente"]), "w", encoding="utf-8").write(t)
    print(p["lente"], p["n"], "fichas ->", "encargo_%s.md" % p["lente"], "; llaves sin llenar:", t.count("{L}"), "; '540' restantes:", t.count("540"))

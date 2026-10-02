# -*- coding: utf-8 -*-
"""gen_encargos.py - escribe encargo_L1..L5.md desde encargo_base.md poniendo {L} y {N} de cada paquete."""
import io, json, os
SP = os.path.dirname(os.path.abspath(__file__))
base = io.open(os.path.join(SP, "encargo_base.md"), encoding="utf-8").read()
P = json.load(io.open(os.path.join(SP, "paquetes.json"), encoding="utf-8"))
for p in P["paquetes"]:
    t = base.replace("{L}", p["lente"]).replace("{N}", str(p["n"]))
    io.open(os.path.join(SP, "encargo_%s.md" % p["lente"]), "w", encoding="utf-8").write(t)
    print(p["lente"], p["n"], "elementos ->", "encargo_%s.md" % p["lente"], len(t), "caracteres; llaves sin llenar:", t.count("{L}") + t.count("{N}"))

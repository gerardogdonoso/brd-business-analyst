# -*- coding: utf-8 -*-
"""gen_v.py - escribe encargo_V1..Vk.md desde encargo_V.md con {V} y el numero real de pares de cada paquete."""
import io, json, os, re, glob
SP = os.path.dirname(os.path.abspath(__file__))
base = io.open(os.path.join(SP, "encargo_V.md"), encoding="utf-8").read()
for f in sorted(glob.glob(os.path.join(SP, "verif_V*.md"))):
    v = os.path.basename(f)[len("verif_"):-len(".md")]
    n = len(re.findall(r"^## PAR ", io.open(f, encoding="utf-8").read(), re.M))
    t = base.replace("{V}", v).replace("unos 26 pares", "%d pares" % n)
    io.open(os.path.join(SP, "encargo_%s.md" % v), "w", encoding="utf-8").write(t)
    print(v, n, "pares -> encargo_%s.md; llaves sin llenar: %d; '26 pares' restantes: %d" % (v, t.count("{V}"), t.count("26 pares")))

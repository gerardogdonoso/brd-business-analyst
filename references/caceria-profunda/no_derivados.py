# -*- coding: utf-8 -*-
import glob, io, json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in sorted(glob.glob(os.path.join(SP, "veredictos_V*.jsonl"))):
    for ln in io.open(f, encoding="utf-8"):
        if not ln.strip():
            continue
        v = json.loads(ln)
        if v["veredicto"] != "compatible" and v.get("resuelve") != "derivado":
            print("N=%d %s | %s | resuelve=%s | cede=%s | fuente=%s" % (v["n"], v["par"], v["veredicto"], v.get("resuelve"), v.get("cede"), re.sub(r"\s+", " ", str(v.get("fuente")))[:200]))
            print("   razon:", re.sub(r"\s+", " ", v.get("razon", ""))[:600])
            print("   por_que_cede:", re.sub(r"\s+", " ", v.get("por_que_cede", ""))[:300])

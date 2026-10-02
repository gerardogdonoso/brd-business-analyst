"""El siguiente ID libre por familia, mirando definiciones Y menciones en los tres archivos que definen IDs."""
import io, re, sys
R = r"C:\Users\User\Projects\agentesIA\docs"
t = "".join(io.open(R + "\\" + f, encoding="utf-8").read() for f in ("BRD.md", "BRD-historial.md", "BRD-evidencia.md"))
for fam in (sys.argv[1:] or ["RN", "CA", "INV", "AL", "PR", "CB", "PE", "DA-IN", "DA-OUT", "DA-EST", "RE", "CE", "RG", "PZ", "NT"]):
    ns = [int(x) for x in re.findall(r"(?<![A-Z-])" + re.escape(fam) + r"-(\d{2,3})\b", t)]
    print("%-7s max %s -> siguiente %s-%03d" % (fam, max(ns) if ns else "-", fam, (max(ns) + 1) if ns else 1))

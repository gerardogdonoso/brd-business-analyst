# -*- coding: utf-8 -*-
"""contraste_git.py <commit> - segundo instrumento para la lista de cambiados: compara fila por fila el BRD de la ultima lectura entera
(el commit que se da como argumento) con el de hoy y dice que elementos vivos de §1-§15 difieren, contra lo que dice la columna «IDs afectados» de §19.
Cuenta: filas de tabla de §1 a §15 (primera por ID) y notas NT en cita en bloque. Deja fuera §16 en adelante."""
import io, json, os, re, subprocess, sys
SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun

def filas(texto):
    out = {}
    for ln in texto.split("\n"):
        if ln.startswith("## 16."):
            break
        d = comun.definicion(ln.rstrip("\r"))
        if d and d[0] not in out:
            out[d[0]] = re.sub(r"\s+", " ", d[1]).strip()
    return out

if len(sys.argv) < 2:
    print("uso: python contraste_git.py <commit del BRD en la ultima lectura entera>   (el 02-10-2026: 7f3c5c4, la v5.83)"); sys.exit(1)
BASE = sys.argv[1]
viejo = subprocess.run(["git", "-C", RAIZ, "show", "%s:docs/BRD.md" % BASE], capture_output=True).stdout.decode("utf-8")
nuevo = io.open(os.path.join(RAIZ, "docs", "BRD.md"), encoding="utf-8").read()
V, N = filas(viejo), filas(nuevo)
cambiados = sorted(i for i in N if i in V and V[i] != N[i])
nuevos = sorted(i for i in N if i not in V)
quitados = sorted(i for i in V if i not in N)
print("v5.83: %d elementos; hoy: %d; cambiados %d; nuevos %d; quitados %d" % (len(V), len(N), len(cambiados), len(nuevos), len(quitados)))

L = json.load(io.open(os.path.join(SP, "lista_cambiados.json"), encoding="utf-8"))
u19 = set(L["union"])
git = set(cambiados) | set(nuevos)
vivos19 = {i for i in u19 if i in N}
print("§19 union: %d IDs, de los cuales vivos en §1-§15: %d" % (len(u19), len(vivos19)))
print("git: %d (cambiados+nuevos)" % len(git))
print("en git y NO en §19:", len(git - u19), sorted(git - u19)[:40])
print("en §19 (vivos) y NO en git:", len(vivos19 - git), sorted(vivos19 - git)[:40])
print("quitados (derogados/mudados):", quitados[:30])
json.dump({"git": sorted(git), "u19_vivos": sorted(vivos19)}, io.open(os.path.join(SP, "contraste_git.json"), "w", encoding="utf-8"))

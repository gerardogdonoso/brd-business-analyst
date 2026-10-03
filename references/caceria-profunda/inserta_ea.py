# -*- coding: utf-8 -*-
"""inserta_ea.py - agrega ea_bloque.md al final de docs/correcciones-brd-pendientes.md, que esta en CRLF.
No inserta dos veces: si el titulo del bloque EA ya esta, se detiene. Comprueba despues que el archivo siga entero en CRLF."""
import io, os, sys
SP = os.path.dirname(os.path.abspath(__file__))
RUTA = r"C:\Users\User\Projects\agentesIA\docs\correcciones-brd-pendientes.md"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
bloque = io.open(os.path.join(SP, "ea_bloque.md"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
crudo = io.open(RUTA, "rb").read()
txt = crudo.decode("utf-8")
if "\n## Bloque EA " in txt.replace("\r\n", "\n"):
    sys.exit("el bloque EA ya esta en el enrutador: no se inserta otra vez")
# los saltos LF sueltos que ya traia se conservan (03-10-2026: uno, al final de la fila DZ-69, de otra sesion)
lf_sueltos = txt.replace("\r\n", "").count("\n")
cuerpo = txt.rstrip("\r\n")
nuevo = cuerpo + "\r\n\r\n" + bloque.replace("\n", "\r\n") + "\r\n"
io.open(RUTA, "wb").write(nuevo.encode("utf-8"))
chk = io.open(RUTA, "rb").read().decode("utf-8")
assert chk.replace("\r\n", "").count("\n") == lf_sueltos, "el bloque nuevo agrego saltos LF sueltos"
print("insertado: %d lineas nuevas; el archivo pasa de %d a %d bytes, todo en CRLF" % (
    bloque.count("\n") + 1, len(crudo), len(chk.encode("utf-8"))))

"""Aplica UNA version del BRD desde un plan JSON revisado por la sesion principal.

Uso:  python aplica_version.py plan.json            (ensayo: no escribe)
      python aplica_version.py plan.json --escribir

El plan:
{
 "version": "5.63", "fecha": "2026-09-27", "tema": "tema cobro y precio del bloque DF",
 "resumen": "texto de la cabecera, sin el prefijo vX.YY",
 "motivo": "celda Motivo de la fila del §19", "aprobado": "celda Aprobado por",
 "revisados": ["CA-..."],                      # criterios revisados sin cambio
 "ediciones": [{"fila": "DF-1", "id": "RN-198", "viejo": "...", "nuevo": "...", "historial": true}],
 "nuevos":    [{"fila": "DF-1", "id": "CA-745", "despues_de": "CA-744", "linea": "| CA-745 | ... |", "seccion": "§15", "estado": "`[DERIVADO: ...]`"}],
 "evidencia": [{"fila": "DF-98", "id": "INV-188", "despues_de": "INV-187", "linea": "| INV-188 | ... |"}],
 "mudar": [{"fila": "DY-6", "id": "CA-586", "seccion": "15. Criterios de aceptación", "razon": "..."}]   # 02-10: derogado -> historial §1
}
Cada `viejo` debe aparecer UNA vez en todo el BRD y caer dentro de la fila del elemento que dice `id`
(o de la nota que nombra, si `id` no es un ID). Lo que no cumpla, aborta sin escribir nada.
"""
import io, json, re, sys
from collections import OrderedDict

import os
R = os.environ.get("BRD_ROOT", r"C:\Users\User\Projects\agentesIA")  # 29-09: BRD_ROOT permite ensayar en una copia
B, H, E = R + r"\docs\BRD.md", R + r"\docs\BRD-historial.md", R + r"\docs\BRD-evidencia.md"
ID_RE = re.compile(r"^(?:RN|PR|PR-ALT|PR-EXC|AL|AL-F|RE|CB|CA|CE|OB|PZ|RG|SA|PE|BN|DA-IN|DA-OUT|DA-EST|DA-CON|AC|AC-ECO|AC-REG|INV|NT)-\d+$")


def leer(p):
    return io.open(p, encoding="utf-8", newline="").read()


def escribir(p, t):
    io.open(p, "w", encoding="utf-8", newline="").write(t)


def dueno_de(texto, pos):
    ini = texto.rfind("\n", 0, pos) + 1
    fin = texto.find("\n", pos)
    l = texto[ini:fin if fin >= 0 else len(texto)]
    m = re.match(r"\| ([A-Z]+(?:-[A-Z]+)*-\d+) \|", l) or re.match(r"> \[(NT-\d+)\]", l)
    if m:
        return m.group(1)
    if l.startswith(">"):
        k = ini
        while k > 0:
            k0 = texto.rfind("\n", 0, k - 1) + 1
            lk = texto[k0:k - 1]
            mm = re.match(r"> \[(NT-\d+)\]", lk)
            if mm:
                return mm.group(1)
            mn = re.match(r"> \*{0,2}(Nota de [^—*]+)", lk)
            if mn:
                return mn.group(1).strip()
            if not lk.startswith(">"):
                break
            k = k0
    return "linea %d" % (texto.count("\n", 0, pos) + 1)


def main():
    plan = json.load(io.open(sys.argv[1], encoding="utf-8"))
    escribe = "--escribir" in sys.argv
    v = plan["version"]
    b, h, e = leer(B), leer(H), leer(E)
    errores = []

    # 1. ediciones, en orden; cada una contra el texto ya editado
    tocados = OrderedDict()
    hist = []
    for ed in plan.get("ediciones", []):
        a, n = ed["viejo"], ed["nuevo"]
        en_evid = ed.get("archivo") == "evidencia"   # 29-09: una edicion puede apuntar a BRD-evidencia.md
        txt = e if en_evid else b
        c = txt.count(a)
        if c != 1:
            errores.append("%s %s: %d apariciones de «%s»" % (ed["fila"], ed["id"], c, a[:90]))
            continue
        pos = txt.find(a)
        quien = dueno_de(txt, pos) if ID_RE.match(ed["id"]) else ed["id"]
        if ID_RE.match(ed["id"]) and quien != ed["id"]:
            errores.append("%s: el tramo cae en %s, no en %s: «%s»" % (ed["fila"], quien, ed["id"], a[:90]))
            continue
        if en_evid:
            e = e.replace(a, n, 1)
        else:
            b = b.replace(a, n, 1)
        tocados.setdefault(quien, [])
        if ed["fila"] not in tocados[quien]:
            tocados[quien].append(ed["fila"])
        if ed.get("historial", True) and len(a) >= 25:
            hist.append("| `%s` | v%s | decía: «%s» — %s (%s) |" % (quien, v, a.replace("|", "¦"), ed["fila"], plan["tema"]))

    # 2. elementos nuevos en el BRD y en la evidencia, y su fila del §16
    nuevos16 = []
    for nv in plan.get("nuevos", []):
        if re.search(r"(?m)^\| " + re.escape(nv["id"]) + r" \|", b + h + e):
            errores.append("ID ya ocupado: %s" % nv["id"])
            continue
        if nv.get("antes_de"):
            m = re.search(r"(?m)^\| " + re.escape(nv["antes_de"]) + r" \|.*$", b)
            if not m:
                errores.append("ancla no hallada: %s" % nv["antes_de"])
                continue
            b = b[:m.start()] + nv["linea"] + "\n" + b[m.start():]
        else:
            m = re.search(r"(?m)^\| " + re.escape(nv["despues_de"]) + r" \|.*$", b)
            if not m:
                errores.append("ancla no hallada: %s" % nv["despues_de"])
                continue
            b = b[:m.end()] + "\n" + nv["linea"] + b[m.end():]
        nuevos16.append("| %s | %s | %s |" % (nv["id"], nv["seccion"], nv["estado"]))
    for iv in plan.get("evidencia", []):
        if re.search(r"(?m)^\| " + re.escape(iv["id"]) + r" \|", b + h + e):
            errores.append("ID ya ocupado: %s" % iv["id"])
            continue
        m = re.search(r"(?m)^\| " + re.escape(iv["despues_de"]) + r" \|.*$", e)
        if not m:
            errores.append("ancla de evidencia no hallada: %s" % iv["despues_de"])
            continue
        e = e[:m.end()] + "\n" + iv["linea"] + e[m.end():]
        nuevos16.append("| %s | §18 | `[INVESTIGADO]` |" % iv["id"])
    # 2-bis. notas de vocabulario nuevas: una linea de blockquote tras otra nota; no llevan fila del §16
    notas_ids = []
    for nt in plan.get("notas_nuevas", []):
        mi = re.match(r"> \[(NT-\d+)\]", nt["linea"])
        if not mi:
            errores.append("nota nueva sin su [NT-xxx] al inicio: %s" % nt["linea"][:60])
            continue
        idn = mi.group(1)
        if re.search(r"(?m)^(?:> \[|\| )" + re.escape(idn) + r"(?:\]| \|)", b + h + e):
            errores.append("ID ya ocupado: %s" % idn)
            continue
        m = re.search(r"(?m)^> \[" + re.escape(nt["despues_de"]) + r"\].*$", b)
        if not m:
            errores.append("ancla de nota no hallada: %s" % nt["despues_de"])
            continue
        b = b[:m.end()] + "\n" + nt["linea"] + b[m.end():]
        notas_ids.append(idn)
    # 2-ter. elementos derogados que se mudan del documento vivo al historial (seccion 1 del historial)
    for md in plan.get("mudar", []):
        rid = md["id"]
        mr = re.search(r"(?m)^\| " + re.escape(rid) + r" \| (.*) \| ([^|\n]*) \|\n", b)
        m16 = re.search(r"(?m)^\| " + re.escape(rid) + r" \| §\d+ \| (`[^`\n]*`) \|\n", b)
        if not mr or not m16:
            errores.append("mudar: no hallo la fila o su §16: %s" % rid)
            continue
        texto, cites, est = mr.group(1), mr.group(2).strip(), m16.group(1)
        b = b[:m16.start()] + b[m16.end():]
        mr = re.search(r"(?m)^\| " + re.escape(rid) + r" \| (.*) \| ([^|\n]*) \|\n", b)
        b = b[:mr.start()] + b[mr.end():]
        celda = "%s ¦ *(**Mudado a este archivo en la v%s, fila %s**: %s.)* · Fila tal como vivía: %s ¦ %s ¦ %s" % (
            rid, v, md["fila"], md["razon"], texto.replace("|", "¦"), cites, est)
        nueva = "| %s | %s | %s |" % (rid, md["seccion"], celda)
        enc = "| ID | Vivía en | Fila completa tal como estaba |\n|---|---|---|\n"
        k0 = h.find(enc)
        assert k0 >= 0, "tabla de derogados del historial"
        k0 += len(enc)
        lineas = []
        pos = k0
        while h.startswith("| ", pos):
            fin = h.find("\n", pos)
            lineas.append((pos, h[pos:fin]))
            pos = fin + 1
        fam, num = re.match(r"([A-Z]+(?:-[A-Z]+)*)-(\d+)$", rid).groups()
        num = int(num)
        punto = None
        ult_fam = None
        for (ps, ln) in lineas:
            mm = re.match(r"\| ([A-Z]+(?:-[A-Z]+)*)-(\d+) \|", ln)
            if not mm or mm.group(1) != fam:
                continue
            ult_fam = ps + len(ln) + 1
            if int(mm.group(2)) > num and punto is None:
                punto = ps
        if punto is None:
            punto = ult_fam if ult_fam is not None else pos
        h = h[:punto] + nueva + "\n" + h[punto:]
        tocados.setdefault(rid, [])
        if md["fila"] not in tocados[rid]:
            tocados[rid].append(md["fila"])
    if nuevos16:
        i16 = b.find("\n## 16.")
        i17 = b.find("\n## 17.")
        tramo = b[i16:i17]
        ult = [mm for mm in re.finditer(r"(?m)^\|.*\|$", tramo)][-1]
        pos = i16 + ult.end()
        b = b[:pos] + "\n" + "\n".join(nuevos16) + b[pos:]

    if errores:
        print("NO SE ESCRIBE NADA. Errores:")
        for x in errores:
            print("  -", x)
        sys.exit(1)

    # 3. cabecera
    ant = re.search(r"(?m)^# Versión: (\d+\.\d+) \(APROBADA — ", b)
    assert ant, "cabecera"
    b = b.replace(ant.group(0), "# Versión: %s (APROBADA — **v%s: %s** · " % (v, v, plan["resumen"]), 1)

    # 4. fila del §19, y lo que pasa de diez versiones se muda al historial
    nuevos_ids = [nv["id"] for nv in plan.get("nuevos", [])] + [iv["id"] for iv in plan.get("evidencia", [])] + notas_ids
    por_fila = OrderedDict()
    for quien, filas in tocados.items():
        por_fila.setdefault(", ".join(filas), []).append(quien)
    mod = "; ".join("%s (%s)" % (", ".join(ids), f) for f, ids in por_fila.items())
    col = ""
    if nuevos_ids:
        col += "**Nuevos:** %s. " % ", ".join(nuevos_ids)
    col += "**Modificados:** %s" % mod
    if nuevos16:
        col += "; §16 Trazabilidad"
    col += "."
    motivo = plan["motivo"]
    if plan.get("revisados"):
        # En la columna de IDs quedan solo los criterios de elementos con nota de esta version (los que
        # exige prueba-rezagada); el resto va al Motivo, para que docs-fresh no los cuente como tocados.
        con_nota = set(re.findall(r"(?m)^\| ([A-Z]+(?:-[A-Z]+)*-\d+) \|.*\(v" + re.escape(v) + r"[:;,) ]", b))
        cubre = {}
        for l in b.split("\n"):
            if l.startswith("| CA-"):
                c = l.split("|")
                cubre[c[1].strip()] = set(re.findall(r"[A-Z]+(?:-[A-Z]+)*-\d+", c[3] if len(c) > 3 else ""))
        quedan = [c for c in plan["revisados"] if cubre.get(c, set()) & con_nota]
        van = [c for c in plan["revisados"] if c not in quedan]
        if quedan:
            col += " **Criterios revisados sin cambio:** %s." % ", ".join(quedan)
        if van:
            motivo = "*(Criterios abiertos uno por uno y sin cambio, por eso van aquí y no en la columna de IDs: %s.)* " % ", ".join(van) + motivo
    fila19 = "| %s | %s | %s | %s | %s |" % (plan["fecha"], v, col, motivo, plan["aprobado"])
    filas = [mm for mm in re.finditer(r"(?m)^\| \d{4}-\d\d-\d\d \| 5\.\d+ \|.*$", b)]
    b = b[:filas[0].start()] + fila19 + "\n" + b[filas[0].start():]
    filas = [mm for mm in re.finditer(r"(?m)^\| \d{4}-\d\d-\d\d \| 5\.\d+ \|.*$", b)]
    sobran = filas[10:]
    mudadas = [mm.group(0) for mm in sobran]
    for mm in reversed(sobran):
        b = b[:mm.start()] + b[mm.end() + 1:]
    if mudadas:
        t = re.search(r"(?m)^## §19 del BRD — historial de cambios hasta la v5\.30 \(.*\)$", h)
        assert t, "seccion del §19 en el historial"
        tit = t.group(0)
        h = h.replace(tit, tit[:-1] + " y la v%s)" % v, 1)
        k = h.find("|---", h.find(tit[:40]))
        k = h.find("\n", k) + 1
        h = h[:k] + "\n".join(mudadas) + "\n" + h[k:]

    # 5. notas historicas
    if hist:
        ancla = "| ID | Versión | Nota tal como estaba |\n|---|---|---|\n"
        k = h.find(ancla)
        assert k >= 0, "ancla de notas del historial"
        h = h[:k + len(ancla)] + "\n".join(hist) + "\n" + h[k + len(ancla):]

    print("version %s: %d ediciones sobre %d elementos, %d nuevos, %d filas de historial, %d filas del §19 mudadas"
          % (v, len(plan.get("ediciones", [])), len(tocados), len(nuevos_ids), len(hist), len(mudadas)))
    for quien, fl in tocados.items():
        print("  %-12s %s" % (quien, ", ".join(fl)))
    if escribe:
        escribir(B, b)
        escribir(H, h)
        escribir(E, e)
        print("ESCRITO")
    else:
        print("(ensayo: no se escribio nada)")


if __name__ == "__main__":
    main()

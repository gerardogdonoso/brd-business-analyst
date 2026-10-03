# -*- coding: utf-8 -*-
"""compone_ea.py - arma el bloque EA completo (titulo, cabecera, filas, lo visto de paso, compatibles) en ea_bloque.md.
Las cifras salen de los archivos de los lectores y de los instrumentos; la prosa es la unica parte escrita a mano.
Antes: python escribe_dx.py --matriz ; python cobertura_ea.py ; costo.json con lo que el arnes reporto de V4 y V5."""
import glob, io, json, os, re, sys
from collections import Counter

SP = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\User\Projects\agentesIA"
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import comun

BRD = comun.leer(os.path.join(RAIZ, "docs", "BRD.md"))
res = json.load(io.open(os.path.join(SP, "dx_resumen.json"), encoding="utf-8"))
filas = io.open(os.path.join(SP, "dx_filas.md"), encoding="utf-8").read().rstrip("\n")
desc = io.open(os.path.join(SP, "dx_descartadas.md"), encoding="utf-8").read().rstrip("\n")
cons = json.load(io.open(os.path.join(SP, "consolidado.json"), encoding="utf-8"))
cob = json.load(io.open(os.path.join(SP, "cobertura_ea.json"), encoding="utf-8"))
costo = json.load(io.open(os.path.join(SP, "costo.json"), encoding="utf-8"))
ver = {}
for f in sorted(glob.glob(os.path.join(SP, "veredictos_V*.jsonl"))):
    for ln in io.open(f, encoding="utf-8"):
        if ln.strip():
            v = json.loads(ln); ver[int(v["n"])] = v

def miles(x):
    return "{:,}".format(x).replace(",", ".")

def pct(a, b):
    return ("%.1f" % (100.0 * a / b)).replace(".", ",")

assert "--borrador" in sys.argv or not res["sin_veredicto"], "faltan veredictos: %s" % res["sin_veredicto"]
V = res["veredictos"]
n_pares = res["pares"]; n_filas = res["filas"]; n_desc = res["descartadas"]
n_contr = V.get("contradice", 0); n_parte = V.get("en-parte", 0); n_comp = V.get("compatible", 0); n_nd = V.get("no-decidible", 0)
nc = [v for v in ver.values() if v["veredicto"] != "compatible"]
prog = Counter(v.get("cambia_lo_que_se_programa") for v in nc)
resu = Counter(v.get("resuelve") for v in nc)
malas_v = sum(1 for v in ver.values()
              if not (comun.contiene(comun.elemento(BRD, v["par"][0]), v.get("cita_clave_a", ""))
                      and comun.contiene(comun.elemento(BRD, v["par"][1]), v.get("cita_clave_b", ""))))
n_cita = sum(1 for c in cons if c["se_citan_real"])
n_conoc = sum(1 for c in cons if c["conocido"])
n_conoc_nc = sum(1 for c in cons if c["conocido"] and ver.get(c["n"], {}).get("veredicto", "compatible") != "compatible")
n_cam = sum(1 for c in cons if any(c["cambio"].values()))
n_cam_nc = sum(1 for c in cons if any(c["cambio"].values()) and ver.get(c["n"], {}).get("veredicto", "compatible") != "compatible")
n_elem = len({i for c in cons for i in c["par"]})
n_nt = sum(1 for c in cons if any(i.startswith("NT-") for i in c["par"]))
por_l = Counter(l for c in cons for l in c["lentes"])
crudos = sum(len(c["hallazgos"]) for c in cons)
clases = Counter(x for c in cons for x in c["clases"])
dos_clases = sum(1 for c in cons if len(c["clases"]) > 1)
dobles = [c for c in cons if len(c["hallazgos"]) > 1]
# lo que dijo cada verificador, por paquete
por_v = {}
for f in sorted(glob.glob(os.path.join(SP, "veredictos_V*.jsonl"))):
    k = os.path.basename(f)[len("veredictos_"):-len(".jsonl")]
    por_v[k] = sum(1 for ln in io.open(f, encoding="utf-8") if ln.strip())
# salida (b) y (d) del segundo lector entre los no compatibles
letras = {"derivado": "a", "investigar": "b", "cuenta": "c", "dueno": "d", "sistema": "e", "trd": "f"}
reparto = " · ".join("(%s) %d" % (letras.get(k, "?"), n) for k, n in sorted(resu.items(), key=lambda kv: letras.get(kv[0], "z")))
n_d = [v["n"] for v in nc if v.get("resuelve") == "dueno"]
n_b = [v["n"] for v in nc if v.get("resuelve") == "investigar"]
contradicen = sorted(v["n"] for v in nc if v["veredicto"] == "contradice")

L = cob["L"]; R = cob["R"]
tok_total = sum(costo["tokens"].values())
_pf = os.path.join(SP, "promover.json")
PROM = sorted(int(k) for k in json.load(io.open(_pf, encoding="utf-8"))) if os.path.exists(_pf) else []
PROM = [n for n in PROM if ver.get(n, {}).get("veredicto") == "compatible"]
prom_txt = ", ".join("`EA-%d`" % n for n in PROM)

titulo = ("## Bloque EA — la cacería profunda de la v5.108: %d hallazgos de cinco lectores por tema, tres de relectura y dos de cruce "
          "(%d pares), %d filas tras una segunda lectura a ciegas (%d contradicen, %d en parte%s%s), %d pares que el segundo lector dio "
          "por compatibles, tres filas de lo visto de paso y una de control (03-10)"
          % (crudos, n_pares, n_filas, n_contr, n_parte, (", %d sin decidir" % n_nd) if n_nd else "",
             (" y %d compatible que se enruta igual" % len(PROM)) if PROM else "", n_desc))

cab = []
cab.append("**De dónde sale:** `cazador-obsoletos.py` avisaba que iban 13 versiones desde la última cacería profunda (v5.95 → v5.108; su umbral es 8) "
           "y el dueño la pidió el 03-10-2026 al lanzar la skill del BRD con las palabras *«Revisión profunda del BRD»*. La corrida se cortó a las 13:45 "
           "con el límite de 5 horas en 85% (sesión `645e33c8`) y la terminó la sesión `d766b70b` después del reinicio, cuando el dueño volvió a lanzar "
           "la skill sin argumentos. **Sin cambio del BRD (v5.108): son filas para aplicar después.**")
cab.append("**Cómo se hizo —el método de los bloques DX y DZ, con una etapa nueva y otro modelo en dos etapas—:** (1) el BRD vivo entero, "
           "**%s elementos** (los 1.738 de §1 a §15 y las 10 notas de vocabulario), se agrupó por tema con un script (TF-IDF y k-means con semilla fija) "
           "y se repartió en cinco paquetes (L1: 159 elementos y 365 KB · L2: 210 y 342 KB · L3: 465 y 318 KB · L4: 338 y 336 KB · L5: 576 y 329 KB); "
           "cada lector (Opus 5.5) leyó primero las diez notas de vocabulario (`NT-001` a `NT-010`) y las tres relaciones del dueño (`RN-380`, `RN-362`, "
           "`RN-311`) y después su paquete en 21, 20, 21, 21 y 23 lotes de unos 20.000 caracteres, con, por elemento, las versiones en que cambió desde la "
           "v5.95, a quién cita y quién lo cita, y escribió una ficha por elemento que afirma algo contradecible. (2) **Etapa nueva, la relectura "
           "bidireccional de §11 (4-bis) de la skill del BRD**, que las corridas del 01-10 y del 02-10 declararon no haber hecho: por cada uno de los "
           "114 elementos que cambiaron entre la v5.96 y la v5.108, tres lectores (R1, R2 y R3) recibieron lo que cambió (la diferencia de palabras "
           "contra la v5.95), su texto de hoy y la cabeza de 300 caracteres de cada vecino —a quién cita y quién lo cita— que cayó en OTRO paquete: "
           "**1.699 pares cambiado-vecino** de los 2.237 que dan las citas (el 67%%), que ningún lector de la etapa (1) tenía juntos. (3) **Cruce:** "
           "las 1.687 fichas se reagruparon por tema sin mirar el paquete de origen (X1: 834 en 18 lotes · X2: 853 en 19) y dos lectores más las "
           "leyeron abriendo el elemento original de cada tensión. (4) **Segunda lectura a ciegas:** cinco verificadores (Opus 5.5) recibieron de cada "
           "par solo los IDs, la clase, las citas literales y los datos del instrumento —sin el razonamiento del primer lector—, abrieron los dos "
           "elementos enteros y a lo más dos vecinos, y dieron su veredicto con quién resuelve el hueco según los seis montones; V2 y V3 se detuvieron "
           "en el corte con 13 y 11 de sus 24 pares, y V4 y V5 verificaron después del reinicio los 24 pares cortados y los 15 que trajo el cruce "
           "(V1 %d · V2 %d · V3 %d · V4 %d · V5 %d veredictos). **Por qué Sonnet en la relectura y el cruce:** según la medición de la sesión `645e33c8`, "
           "Opus 5.5 gastó en la etapa (1) más límite por token que la corrida del 02-10 (unos 63.000 tokens por punto del límite de 5 horas, contra "
           "unos 125.000), y las etapas (2) y (3) se pasaron a Sonnet para que la corrida cupiera. **Los lectores por tema y los verificadores son del "
           "mismo modelo: su acuerdo no es evidencia independiente;** los hallazgos de la relectura y del cruce los verificó un modelo distinto del que "
           "los encontró."
           % (miles(L["vivos"]), por_v.get("V1", 0), por_v.get("V2", 0), por_v.get("V3", 0), por_v.get("V4", 0), por_v.get("V5", 0)))
dob_txt = "; ".join("`%s`/`%s` (%s)" % (c["par"][0], c["par"][1], " y ".join(c["lentes"])) for c in dobles)
cab.append("**Cifras del resultado, con cómo se midió cada una:** (a) *Hallazgos:* %d reportados (L1 %d · L2 %d · L3 %d · L4 %d · L5 %d · relectura "
           "R1 %d, R2 %d y R3 %d · cruce X1 %d y X2 %d) = **%d pares distintos** —%d pares los reportaron dos lectores sin saberlo: %s— que "
           "involucran %d elementos; el recuento sale de leer los diez archivos con un script y juntar por par sin importar el orden. Clase del primer "
           "lector: %s (%d pares traen dos clases). (b) **Citas:** las parejas de citas literales de los primeros lectores están dentro de su elemento "
           "(`comun.contiene` sobre el BRD vivo: %d de %d), y de las citas clave de los verificadores %d de %d pasan; eso prueba que la cita existe, "
           "no que el choque sea real. (c) **Veredicto del segundo lector:** %d contradicen, %d contradicen en parte (chocan solo en una parte del "
           "alcance o bajo un supuesto que el texto no da por escrito), %d compatibles y %d sin decidir; los compatibles quedan en la tabla del final "
           "con su razón, para que la próxima cacería no los vuelva a reportar%s. De los %d no compatibles el segundo lector dice que %d cambian lo que "
           "se programa, %d no y %d no sabe. (d) **Se citan o no:** de los %d pares, **%d SÍ se citan** y %d no (el grafo es el del BRD vivo y trae "
           "las notas `NT`; %d pares tienen una nota). (e) **Pares que ya tenían fila:** %d de %d nombran los dos IDs en una misma fila de este "
           "enrutador o de `docs/archivo/correcciones-aplicadas.md` (criterio laxo: no se comparó que la fila trate la misma contradicción; %d de "
           "esos %d no son compatibles); casi siempre la fila es la aplicada que produjo el choque. **No se midió el recall** —no se sabe cuántas "
           "contradicciones hay—. (f) **Tocan un elemento cambiado desde la v5.95:** %d de los %d pares (%d de los %d no compatibles)."
           % (crudos, por_l["L1"], por_l["L2"], por_l["L3"], por_l["L4"], por_l["L5"], por_l["R1"], por_l["R2"], por_l["R3"], por_l["X1"], por_l["X2"],
              n_pares, len(dobles), dob_txt, n_elem,
              " · ".join("%s %d" % (k, n) for k, n in clases.most_common()), dos_clases,
              sum(1 for c in cons if all(c["citas_ok"])), n_pares, len(ver) - malas_v, len(ver),
              n_contr, n_parte, n_comp, n_nd,
              ("; %s se enruta igual, porque el propio segundo lector dice que su frase sobra (ver su fila)" % prom_txt) if PROM else "",
              len(nc), prog.get("si", 0) + prog.get("sí", 0), prog.get("no", 0), prog.get("no se", 0) + prog.get("no sé", 0),
              n_pares, n_cita, n_pares - n_cita, n_nt, n_conoc, n_pares, n_conoc_nc, n_conoc, n_cam, n_pares, n_cam_nc, len(nc)))
cab.append("**Cobertura, declarada y medida:** **impreso no es leído con atención.** Medido por el registro de `leer.py`: %s de %s elementos impresos, "
           "y los %d elementos vivos que cambiaron entre la v5.96 y la v5.108 también; la relectura imprimió los %d cambiados con sus vecinos de otro "
           "paquete. Declarado por los propios lectores: **%d de los %s elementos (%s%%) estaban en lotes que leyeron más rápido** y %d (%s%%) en "
           "lotes leídos con atención media (L1: rápido 11, 13 y 14, media 9 y 10 · L2: rápido 17, 18 y 19, y del 4 dos filas cerradas, media 7, 9, "
           "10, 11, 14 y 20 · L3: rápido 17 a 21, media 1, 4, 5, 6, 7, 9 y 16 · L4: rápido 8 y 12, media 7, 9, 11 y 13 · L5: rápido 14, 19, 20 y 23, "
           "media 11, 12, 13, 15 y 22); **%d de los %d cambiados están en lotes rápidos y %d en lotes de atención media**. En la relectura, %d de los "
           "114 cambiados cayeron en lotes que su lector declaró rápidos (R1: 15, 20 y 21 · R2: 2, 13, 18 y 20 · R3: 13 y 15) y %d en lotes de "
           "atención media. En el cruce, X2 declaró rápidos sus lotes 3, 12, 14 y 16 (219 de sus 853 fichas) y X1 no declaró lotes rápidos pero "
           "avisó que en los más densos (3, 6, 8, 15, 16 y 17: 337 de sus 834 fichas) pudo escaparse algo. Para comparar, con la misma pregunta a "
           "los lectores: el 02-10 fueron 605 de 1.732 (34,9%%) en lotes rápidos y el 01-10, 689 de 1.727 (40%%). **Lo que L4 declaró NO leído:** "
           "`PE-014` puntos (k) a (o); los otros cuatro lectores por tema y los tres de relectura declararon 0 elementos sin leer. Las fichas cubren "
           "%s de los %s elementos (%s%%): lo no fichado solo se comparó en la cabeza del lector. X1 anotó 69 tensiones (8 hallazgos, 9 duplicados y "
           "52 descartes) y X2 unas 100 (74 descartadas, 10 ya reportadas por otros lectores y 8 hallazgos)."
           % (miles(L["impresos"]), miles(L["vivos"]), L["cambiados"], R["impresos"], L["rapido"], miles(L["vivos"]), pct(L["rapido"], L["vivos"]),
              L["media"], pct(L["media"], L["vivos"]), L["cambiados_rapido"], L["cambiados"], L["cambiados_media"], R["rapido"], R["media"],
              miles(L["fichados"]), miles(L["vivos"]), pct(L["fichados"], L["vivos"])))
cab.append("**La lista de elementos cambiados:** 122 IDs en las 13 versiones v5.96 a v5.108, de ellos 114 vivos en §1 a §15; el resto son "
           "derogados o evidencia `INV`. **Contraste con un segundo instrumento:** se comparó fila por fila el `docs/BRD.md` del commit `c7f8ef4` "
           "(v5.95) con el de hoy: 107 elementos con texto distinto y 7 nuevos, y **los dos instrumentos dan los mismos 114 IDs, con 0 de diferencia "
           "en los dos sentidos.**")
cab.append("**Costo, medido:** unos %s millones de tokens de subagentes (suma de lo que el arnés reportó por agente: cinco lectores por tema "
           "2,73 millones —de 507.000 a 594.000 cada uno, 34 a 40 minutos—, tres de relectura 2,12 millones —Sonnet, de 672.000 a 767.000—, dos de "
           "cruce 1,86 millones —Sonnet, 916.000 y 949.000, 61 y 57 minutos—, V1 0,33 millones, V4 %s y V5 %s; V2 y V3 se detuvieron en el corte y "
           "el arnés no reporta lo que gastaron). El límite de 5 horas pasó de 4%% a 85%% en la primera parte (12:20 a 13:45) y de 5%% a %s en la "
           "segunda; el semanal de 54%% a 65%% en la primera y de 67%% a %s en la segunda, contando también los turnos de las dos sesiones. Para "
           "comparar: la corrida del 02-10 gastó unos 4,4 millones y llevó el límite de 5 horas de 8%% a 45%%; la del 01-10, unos 7 millones y de "
           "0%% a 77%%. Esta fue la más cara de las tres en límite de uso, con la etapa nueva de relectura (2,12 millones) incluida."
           % (("%.1f" % (tok_total / 1e6)).replace(".", ","), costo["v4_txt"], costo["v5_txt"], costo["limite5_fin"], costo["semanal_fin"]))
cab.append("**Lo que esta corrida NO hizo:** (1) **medir el recall**: no se sabe cuántas contradicciones hay; (2) **abrir el vecindario completo "
           "de cada fila**: lectores y verificadores abrieron los vecinos por ID y a lo más dos vecinos por par; (3) **la sesión principal no reabrió "
           "los pares**: leyó los informes, las cifras y lo visto de paso, y ninguna fila queda como comprobada contra su vecindario; (4) «quién "
           "resuelve» es la lectura del verificador: entre los %d no compatibles el reparto es %s; las corridas del 01-10 y del 02-10 marcaron casi "
           "todo «derivado» (84 de 90 y 42 de 48), lo que invita a desconfiar del reparto: **quien aplique una fila (a) abre el par y confirma que "
           "solo una lectura es consistente con lo escrito**%s; (5) el agrupamiento por tema lo hizo un script: lo que separó en paquetes distintos "
           "solo lo juntaron el cruce y la relectura; (6) la relectura dio %d hallazgos de 1.699 pares cambiado-vecino, y no se midió cuántos de "
           "esos pares leyó con atención cada lector más allá de lo que declararon por lote."
           % (len(nc), reparto,
              ("; las marcadas (d) (%s) y (b) (%s) no llegan al dueño todavía: antes se corre la pregunta cero (¿quién mira ese dato?) y se busca en la industria"
               % (", ".join("`EA-%d`" % n for n in sorted(n_d)) or "ninguna", ", ".join("`EA-%d`" % n for n in sorted(n_b)) or "ninguna")),
              por_l["R1"] + por_l["R2"] + por_l["R3"]))

# Lo visto de paso: cada cita se comprueba aqui mismo contra el BRD vivo
def chk(eid, q):
    t = comun.elemento(BRD, eid)
    assert t and comun.contiene(t, q), "cita que no pasa: %s «%s»" % (eid, q)
    return q
q88a = chk("NT-005", "la palabra designa CINCO cosas en este documento")
q88b = chk("NT-005", "Los cuatro usos, con su nombre canónico")
q89a = chk("RN-334", "$950 por atención ≈ 3% de ese ticket si cada atención es un pedido")
q89b = chk("RN-334", "del orden de $25.000 por pedido")
derog = []
for i in ("PR-039", "CA-182", "CA-283", "CA-461", "CA-530", "CA-573"):
    t = comun.elemento(BRD, i)
    assert t and "DEROGAD" in t[:200], "no abre con DEROGAD: %s" % i
    derog.append(i)

cab.append("**Lo que los lectores vieron de paso, fuera de su encargo, y la sesión principal abrió:** (a) `NT-005` cuenta CINCO cosas y titula "
           "su lista con cuatro: se sostiene → fila `EA-88`; `cazador-obsoletos.py` no lo ve porque su control O1 cuenta solo marcadores numéricos "
           "(1)..(N) y se abstiene a propósito cuando el mismo elemento trae un numeral que coincide con la enumeración, y aquí trae los dos (no se "
           "propone cambiar el control: no está medido); (b) `RN-334` dice que $950 son ≈ 3% de un ticket de $25.000, y la cuenta da 3,8%: se "
           "sostiene → fila `EA-89`; (c) el lector L3 nombró cuatro criterios derogados dentro del BRD vivo y la sesión principal contó con un script "
           "**seis** filas de §1 a §15 que abren con *DEROGADO*: se sostiene → fila `EA-90`, y como la regla de mudarlas ya estaba escrita y "
           "ningún control la verifica, la fila `EA-C1` propone el control, medido; (d) el verificador V1 vio que la regla de las "
           "capacidades de ofrecer contradice su propio pendiente: es la misma corrección de la fila `EA-70` y va dentro de ella; (e) un lector leyó "
           "en `AL-072` *los otros cuatro canales* con Mercado Libre como sexto canal (`AL-084`): **no se sostiene**, porque `AL-052` declara que "
           "«los cinco canales» nombra siempre los cinco del alcance de `PZ-001`, `AL-084` dice que Mercado Libre no está entre ellos, y la sesión "
           "principal leyó el tramo de cada una de las 15 apariciones de «cinco canales» del BRD vivo sin hallar una que contradiga esa regla de "
           "lectura; (f) `DA-EST-001` cierra su lista de lo que no es con *Tres objetos con tres relojes distintos* (la conversación, la atención y "
           "el caso) y un lector lo leyó como texto anterior al corte del caso a los 30 días: la sesión principal abrió `DA-EST-001` y no lo pudo "
           "decidir sin abrir `RN-274` y `RN-337`; queda ○ sin verificar y sin fila.")
cab.append("**Cómo leer estas filas:** todas nacen ○ SIN VERIFICAR (las citas de cada fila pasaron el script; el veredicto es lectura de un "
           "modelo). **Antes de actuar sobre una se abren los dos elementos del par con `tools/elemento.py` (trae el vecindario) y se buscan sus "
           "citas.** «Qué cede» y «quién resuelve» son lecturas, no decisiones del dueño. **Las citas entre « » son literales y `citas-verificadas.py` "
           "las comprueba; las frases del segundo lector que no son citas literales van sin comillas de cita, y las citas literales de las familias "
           "que ese control no abre (`AC`, `NT`) van entre ‹ ›.** La numeración `EA-n` es la del par (1 a %d) y no cambia: los pares compatibles "
           "conservan su número en la tabla del final; las filas `EA-88` a `EA-90` son lo visto de paso y `EA-C1` es la de un control." % n_pares)

extra = []
extra.append("| **EA-88** | ○ **SIN VERIFICAR** (visto de paso por el lector L2, fuera de su encargo; la sesión principal abrió `NT-005` y contó su "
             "enumeración) | **Dentro de `NT-005`.** La nota dice *‹%s›* y titula *‹%s›* antes de enumerar cinco, de (a) el chat web a (e) el chat "
             "de Dudas, que lleva la marca de la v5.51; la cabeza cuenta cinco y el titular de la lista quedó en cuatro. Quien lea solo el titular "
             "programa cuatro usos. | `NT-005` | Corregir el titular a *Los cinco usos*: la propia nota cuenta cinco y enumera cinco (se deriva de "
             "`NT-005`). No cambia lo que se programa si la nota se lee entera. | **(a)** Claude, derivándolo de lo ya escrito (`NT-005`) |" % (q88a, q88b))
extra.append("| **EA-89** | ○ **SIN VERIFICAR** (visto de paso por el lector R1, fuera de su encargo; la sesión principal abrió `RN-334` e hizo la "
             "cuenta) | **Dentro de `RN-334`.** La regla pide un ticket *«%s»* y explica *«%s»*; $950 / $25.000 = 3,8%%, no 3%%. La cifra viene de "
             "antes: la v5.107 reescribió la frase, que decía $950 por pedido ≈ 3%% (`tools/historia.py RN-334`), y conservó el porcentaje. | "
             "`RN-334`, `PZ-016` | Corregir a ≈ 4%% o 3,8%%: es la aritmética de las dos cifras que la regla ya trae (se deriva de `RN-334`). Cambia "
             "la explicación del ticket, no el precio. | **(a)** Claude, derivándolo de lo ya escrito (`RN-334`) |" % (q89b, q89a))
extra.append("| **EA-90** | ○ **SIN VERIFICAR** (visto de paso por el lector L3, que nombró cuatro; la sesión principal contó con un script las "
             "filas de §1 a §15 que abren con *DEROGADO* y consultó el historial de cada una con `tools/historia.py`) | **Seis elementos derogados "
             "siguen dentro de §1 a §15 del BRD vivo**, con el texto viejo tachado y su nota de derogación: `PR-039` (v5.69), `CA-182` (v5.41), "
             "`CA-461` (v5.49), y `CA-283`, `CA-530` y `CA-573` (v4.34). `tools/historia.py` no encuentra nada de `CA-283`, `CA-461`, `CA-530` ni "
             "`CA-573` en `docs/BRD-historial.md`, y de `PR-039` y `CA-182` solo notas de lo que decían. La skill del BRD manda que lo que dejó de "
             "regir salga del documento vivo y conserve su fila en el historial (cambios posteriores, punto 6); quien lee §4 o §15 de corrido lee "
             "seis filas que no rigen. **Y el §16 les da dos estados:** `PR-039` está en el rango `PR-001 a PR-076` como `[CONFIRMADO]` y en su "
             "fila como `[DEROGADO]`; `CA-283`, `CA-530` y `CA-573` están en su fila como `[DEROGADA]` y en un rango como vigentes (`CA-001 a "
             "CA-300` y `CA-527 a CA-533` como `[CONFIRMADO]`, `CA-570 a CA-576` como `[INVESTIGADO]`); y `CA-182` solo aparece como vigente, en "
             "`CA-001 a CA-300`, cuya lista de exceptuados no lo nombra. Por eso el cuadro de cierre de la skill (`cuadro_cierre.py`, que se queda "
             "con el primer estado que el §16 da a cada ID) contó en la v5.108 3 derogadas y no 6, y cuenta `PR-039`, `CA-182` y `CA-283` como "
             "confirmados. | %s | Mudar las seis filas a `docs/BRD-historial.md` con su versión de derogación y dejar en el §16 del BRD un solo "
             "estado por ID: la fila de derogada, y las seis fuera de los rangos que las dan por vigentes (o en su lista de exceptuados); antes, "
             "correr `tools/vecinos-brd.py` sobre las seis para que ninguna cita quede apuntando a una fila sin definición (se deriva de la regla de "
             "la historia fuera del documento vivo). No cambia lo que se programa si quien lee respeta el tachado. | "
             "**(a)** Claude, derivándolo de lo ya escrito |" % ", ".join("`%s`" % i for i in derog))
extra.append("| **EA-C1** | ○ **SIN VERIFICAR** (hallada por la sesión principal al revisar lo visto de paso, 03-10-2026, sesión `d766b70b`) | "
             "**La regla de mudar lo que dejó de regir no tiene control.** La skill del BRD manda que un elemento derogado salga del documento vivo "
             "y conserve su fila en `docs/BRD-historial.md` (cambios posteriores, punto 6), y seis seguían en §1 a §15 (`EA-90`), algunos desde la "
             "v4.34: el defecto ya tenía su regla escrita y ocurrió igual. `mapa-brd.py` no los nombra y ningún diagnóstico del arranque los cuenta. "
             "*Qué se contó:* filas de §1 a §15 de `docs/BRD.md` cuyo texto abre con *DEROGADO* en sus primeros 160 caracteres: 6; *segundo "
             "instrumento:* filas con un tramo tachado (`~~…~~`) en sus primeros 600 caracteres: 6, **los mismos seis IDs, 0 de diferencia en los dos "
             "sentidos**. *Qué quedó fuera:* las notas `NT`, que no son filas de tabla, y los derogados escritos de otra forma, que no se buscaron. | "
             "`tools/mapa-brd.py`, %s | Agregar a `mapa-brd.py` (o como diagnóstico del arranque) un foco que cuente las filas vivas de §1 a §15 que "
             "abren con *DEROGADO* o con texto tachado. *Antes:* 6. *Después* de aplicar `EA-90`: 0. *Qué se rompería:* como diagnóstico, nada; si "
             "entrara a la puerta, la pondría en rojo hasta que se aplique `EA-90`. Va por `regresion-controles.py` y su copia a la skill `crea-suite`. | "
             "**(f)** mecanismo de un control, sesión normal sin la skill |" % ", ".join("`%s`" % i for i in derog))

txt = titulo + "\n\n" + "\n\n".join(cab) + "\n\n" + "| # | Origen | Qué pasa | Base | Qué hacer | Quién resuelve |\n|---|---|---|---|---|---|\n" \
      + filas + "\n" + "\n".join(extra) + "\n\n" \
      + "### Los %d pares que el segundo lector dio por compatibles (no son filas)\n\n" % n_desc \
      + ("**Se listan para que la próxima cacería no los reporte otra vez**; cada razón es la del segundo lector, que abrió los dos elementos y a lo "
         "más dos vecinos. Si alguna razón no convence, el par se reabre con `tools/elemento.py` y se escribe como fila nueva.\n\n") \
      + desc + "\n"
io.open(os.path.join(SP, "ea_bloque.md"), "w", encoding="utf-8").write(txt)
print("titulo:", titulo)
print("filas de pares: %d + 3 de lo visto de paso; compatibles: %d; %d KB" % (n_filas, n_desc, len(txt.encode("utf-8")) // 1024))
print("contradicen:", contradicen)
print("resuelve (no compatibles):", dict(resu), "| d:", n_d, "| b:", n_b)
print("cambia lo que se programa:", dict(prog), "| citas de verificadores que no pasan:", malas_v)

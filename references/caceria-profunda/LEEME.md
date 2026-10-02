# La cacería profunda por paquetes — herramientas de la corrida del 01-10-2026

> **Cómo usar este documento.** Es la memoria de CÓMO se corrió la cacería semántica de §11 (5) en `agentesIA` el 01-10-2026, con las herramientas y los encargos que se usaron. Lo que rige sigue siendo `SKILL.md`; el relato de los resultados vive en el bloque `DX` de `docs/correcciones-brd-pendientes.md` del repositorio `agentesIA` (commit `7f3c5c4`). Los scripts traen rutas absolutas de esa máquina (`RAIZ`, `SP`) y los textos de cabecera de `compone_dx.py` son de esa corrida: **se adaptan antes de correrlos, no se usan a ciegas**.

**Por qué existe.** El BRD de `agentesIA` pesa ~1,8 MB (unos 450.000 tokens): un solo agente no lo lee entero, y las cacerías DF y DJ (cinco lentes con búsqueda libre, cada elemento abierto con su vecindario) se cortaron por el límite de uso en una de ellas y dejaron la cobertura sin medir. Esta corrida leyó **todo** el texto vivo una vez, por paquetes por tema, con la cobertura medida por un registro.

## Las piezas, en el orden en que se corren

1. `lista_cambiados.py` — IDs que cada versión de §19 (BRD e historial) tocó; variables `LO`, `HI`, `SALIDA`. Se contrastó contra el lector de historial de `cazador-obsoletos.py` en las diez últimas versiones.
2. `prepara.py` — agrupa los elementos vivos de §1 a §15 por tema (TF-IDF y k-means, semilla fija) y los reparte en cinco paquetes de volumen parecido; escribe `paquetes.json` y `elementos.json`.
3. `leer.py <L>` — entrega el siguiente lote (~20.000 caracteres) de un paquete y lo anota en `leido_<L>.log`; `--marco 1` imprime las notas `NT-`, `--marco 2` las tres relaciones que mandan, `--estado` cuenta, `--lote K` repite sin sumar. `cita.py A B` dice si A y B se citan.
4. `encargo_base.md` — el encargo del lector (placeholders `{L}`, `{N}` y `SP/`); cada lector escribe `fichas_<L>.md` (una línea por elemento que afirma algo contradecible) y `hallazgos_<L>.jsonl` con **cita literal de cada elemento**.
5. **Cruce:** `prepara_x.py` reagrupa las fichas por tema ignorando el paquete de origen; `leer_x.py` y `encargo_X.md` son el lector de esa etapa (un par cuyos dos elementos cayeron en paquetes distintos nunca estuvo en la cabeza de un mismo lector).
6. `consolida.py` — junta los hallazgos por par (sin importar el orden), repara la codificación, comprueba citas con `comun.contiene`, mira si se citan y si el par ya tiene fila en el enrutador o su archivo; la numeración del par queda fija en `numeracion.json`. `verifica.py` es la versión por lente.
7. `arma_verif.py` + `encargo_V.md` — paquetes de **verificación a ciegas**: de cada par solo los IDs, la clase, las citas y los datos del instrumento, sin el razonamiento del primer lector. `--nuevos` arma un paquete aparte con los pares que llegaron tarde.
8. `escribe_dx.py` + `compone_dx.py` — generan las filas del enrutador y el bloque entero. Las filas nacen ○ SIN VERIFICAR.

## Segunda corrida (02-10-2026, v5.83 → v5.95) y lo que cambió en las herramientas

Se corrió igual, con las herramientas de arriba copiadas a la carpeta de la sesión y adaptadas con `adapta*.py` (reemplazos literales que cuentan cuántas veces cambiaron; se escriben de nuevo cada corrida). El resultado vive en el bloque `DZ` del enrutador. **Piezas nuevas, ya en esta carpeta:** `contraste_git.py <commit>` (segundo instrumento de la lista de cambiados: compara el BRD del commit de la última lectura entera con el de hoy; el 02-10 dio los mismos 156 IDs que la columna «IDs afectados» de §19, 0 de diferencia) · `gen_encargos.py` (escribe `encargo_L1..L5.md` desde `encargo_base.md`) · `cobertura.py` (impreso por el registro de `leer.py`, leído rápido por lo que declara cada lector, fichado; los números de lote «rápido» se copian a mano de los informes) · `stats.py` (cifras de la cabecera del bloque y los pares «contradice») · `no_derivados.py` (las filas que el verificador no marcó «derivado», que son las que podrían llegar al dueño). **Arreglos medidos:** (1) `prepara_x.py` descartaba las fichas de grupo (`CA-281/297/360/618`) y las de «(leído)»: 1.294 fichas y 121 líneas perdidas antes, 1.511 y 0 después; (2) `prepara.py` lee con `comun.definicion` y por eso el grafo trae las 9 notas `NT` (1.732 → 1.741 elementos, 0 perdidos, `NT-003` pasa de 0 a 30 que la citan; los cuatro lectores que abrieron una nota declararon que no estaba en el grafo); (3) `leer.py --marco 1` cortaba en la línea 2092 (el BRD ya tiene 2.523): ahora corta en «## 16.». `escribe_dx.py` conserva a mano dos cosas de cada corrida: `PROMOVER` (pares «compatibles» que igual se enrutan) y `LEIDAS` (pares que la sesión principal leyó enteros), y el prefijo `DX-`/`DZ-` de las filas.

## Antes de correrlo

- **Mirar `get_usage` (límite de 5 horas) y correr UN lector de piloto** antes de lanzar el resto. Medido el 01-10-2026: cinco lectores 3,7 millones de tokens, dos de cruce 1,5 millones, cinco verificadores 1,9 millones (≈ 7 millones y unas dos horas); el límite de 5 horas pasó de 0% a 77% y el semanal de 12% a 22%. **Medido el 02-10-2026:** cinco lectores 2,4 millones (de 442.000 a 521.000 cada uno), dos de cruce 1,26 millones, tres verificadores 0,70 millones (≈ 4,4 millones y 67 minutos); el límite pasó de 8% a 45% y el semanal de 38% a 43%, turnos de la sesión incluidos. **La diferencia entre las dos corridas no se explicó.** El piloto (L1 solo) dio 1 punto en 5 minutos y 7 de 21 lotes, y a eso se le puede proyectar el resto.
- Declarar la cobertura **como dato del lector**: «impreso» lo mide `leer.py`; «leído con atención» solo lo declara cada lector (el 01-10, 40% de los elementos estaban en lotes que los propios lectores leyeron más rápido; el 02-10, 34,9%, y 37 de los 154 elementos cambiados). El informe de cada lector pide los números de lote leídos rápido; el encargo base no lo pide, se agrega en el prompt.
- **El encargo se pasa como archivo** (`encargo_L1.md`…): el prompt del agente dice «ábrelo con Read y síguelo» y no lo repite; el guardián de la sesión no frenó ese formato el 02-10.

## Trampas que costaron tiempo

- `leer.py <L>` sin opciones **consume** un lote: para probar usar `--lote K` o `--estado`.
- Un lector que escribe el JSONL con `Add-Content`, `Out-File` o `>>` de PowerShell lo guarda en cp1252 y rompe tildes y «»: el encargo pide Python con `encoding="utf-8"`; `consolida.py` repara lo que quede.
- Las notas `NT-` no son filas de tabla (son citas en bloque): se leen con `--marco 1`. `vecinos-brd.py` y `cazador-obsoletos.py` **no siguen `DA-EST` ni `NT`**; el grafo de `prepara.py` sí incluye `DA-EST`.
- Un verificador que marca todo «derivado» (el cuarto paquete marcó los 26 así): el «quién resuelve» es lectura suya; quien aplica abre el par y lo confirma.
- Las frases de un lector entre «» que no sean literales hacen fallar `citas-verificadas.py`: en las filas van sin comillas de cita; las literales de familias que ese control no abre (`AC-`, `NT-`) van entre ‹ ›.
- `git checkout` del enrutador lo deja en LF aunque el árbol de trabajo tuviera CRLF: se vuelve a escribir con CRLF antes de comprobar.
- El agrupamiento lo hace un script: lo que separa en paquetes distintos solo lo junta el cruce.

## Lo que esta corrida no hizo

Medir el recall (no se sabe cuántas contradicciones hay) · la relectura bidireccional de lo que tocaron las últimas versiones (§11 (4-bis)) · abrir el vecindario completo de cada fila (lectores y verificadores abrieron los vecinos por ID y a lo más dos vecinos por par).

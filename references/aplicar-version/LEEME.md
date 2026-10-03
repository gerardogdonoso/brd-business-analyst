# Aplicar una versión del BRD — la herramienta de las v5.63 a v5.99

> **Cómo usar este documento.** Es la memoria de CÓMO se aplica a `docs/BRD.md` una versión nueva desde un plan revisado, con las herramientas que se usaron en `agentesIA` entre el 27-09 y el 02-10-2026 (v5.63 a v5.99). Lo que rige sigue siendo `SKILL.md` (§11, «Cambios posteriores a la aprobación»). Antes vivían en las carpetas temporales de cada sesión (diez copias) y se buscaban a mano; desde el 02-10-2026 viven aquí. **Traen rutas absolutas de esa máquina** (`R` en `aplica_version.py` y `siguiente_id.py`; `restampa_ejemplo.py` es de la v5.99): se adaptan antes de correrlos.

## Las piezas

- `aplica_version.py` — aplica UNA versión desde un plan JSON. El formato está en su cabecera y en `ejemplo-plan.json` (el de la v5.95). Escribe el BRD, el historial (con el «decía» de cada edición de 25 o más caracteres), la cabecera, la fila del §19 (las filas que pasan de diez versiones se mudan al historial) y la evidencia. **Cada `viejo` debe aparecer UNA vez en todo el BRD y caer dentro de la fila del elemento que dice `id`; si no, no escribe nada.** Opciones del plan: `ediciones`, `nuevos`, `evidencia`, `notas_nuevas`, `mudar` (derogado que sale al historial), `revisados` (criterios abiertos y sin cambio) y `"archivo": "evidencia"` en una edición que cae en `BRD-evidencia.md`.
- `siguiente_id.py` — el siguiente ID libre por familia (mira definiciones y menciones en los tres archivos que definen IDs). Los IDs los asigna quien escribe en el BRD; nunca se reservan desde fuera.
- `restampa_ejemplo.py` — sube la estampa «Al día con BRD» de los derivados que `docs-fresh` marca, con una nota que dice cómo se revisaron. **Es de la v5.99: el texto de la nota y la lista de documentos se adaptan.**
- `restampa_5107.py` — el mismo re-estampado, de la v5.107, con tres notas según el documento: el que se corrigió (dice cuántos tramos), el que solo conserva relatos y el que no tuvo hallazgo; lee la lista de `docs-fresh` de un archivo del scratchpad.
- `plan_con_anclas.py` — ayudante para armar el plan sin retipear: `E(fila, id, ancla_inicial, ancla_final, nuevo)` extrae el `viejo` EXACTO del BRD entre dos anclas y comprueba que aparece una sola vez en todo el BRD y que no se pisa con otra edición (v5.107: 80 ediciones sin un `viejo` mal copiado). El plan se escribe en un `.py` que importa este y termina volcando el JSON.
- `derivados_con_anclas.py` — lo mismo para los documentos derivados: `D` reemplaza un tramo único del documento y `DD` uno idéntico que vive en dos líneas; `aplicar(escribir=True)` escribe.
- `cuadro_cierre.py` — cuenta los elementos de §1 a §15 por estado, una vez cada uno, con dos analizadores que se comparan; es el cuadro de cierre de `SKILL.md` §12 (los criterios, que no traen celda de estado, toman el del §16 con sus rangos expandidos).

## El orden

1. Armar el plan con los pares viejo/nuevo copiados del BRD. Cada fila del enrutador se abre antes con `python tools/elemento.py <ID> <ID>` (trae el vecindario; con 18 a 28 KB por par, se guarda al scratchpad y se lee por tramos).
   **Y antes de armar el plan se barre el propio BRD por las frases que la regla nueva vuelve falsas, con dos juegos de palabras, y cada elemento hallado entra al plan.** Las filas nombran los elementos que su autor vio: las tres de la v5.107 nombraban 12 y el barrido halló 33 más —criterios, estados de datos, reglas de factura, de alertas y de caída—. Se barren también las preguntas contrarias (qué otras frases dicen lo mismo con otras palabras), no solo la que la fila cita.
2. **Ensayo sin escribir:** `python aplica_version.py plan.json`. Para ensayar versiones en cadena, sobre una copia de los tres archivos: `BRD_ROOT=<carpeta con docs/>` (la variable cambia la raíz).
3. Releer sobre la copia los tramos largos que quedaron escritos, antes de tocar el BRD de verdad. Después `--escribir` y `python tools/docs-check.py`. **Si al releer se hallan más elementos, se revierten los dos archivos con `git checkout -- docs/BRD.md docs/BRD-historial.md` (están limpios al empezar) y se reaplica el plan ampliado:** así la fila del §19 y el historial quedan completos en una sola versión, en vez de parchar el BRD a mano después.
4. **Revisar a mano los criterios de lo que se tocó** (la regla que cambió y su criterio se miran juntos) y correr `python tools/cazador-obsoletos.py --relectura <versión>`: nombra, no compara significados.
5. `python tools/docs-fresh.py --lineas > <scratchpad>/fresh-lineas.txt` y **barrer los derivados por las frases corregidas, con dos juegos de palabras**, sin imprimir el resultado entero. Corregir lo que repita lo viejo; regenerar `requisitos.md` con `python tools/spec-requisitos.py docs/specs/<spec>`; re-estampar con la nota que dice cómo se revisó (no se sube una estampa sin decir qué se leyó).
6. Marcar las filas del enrutador como aplicadas (solo su celda «Origen»), `python tools/citas-verificadas.py`, `python tools/docs-gate.py`, commit por ruta y `git push origin main`.

## Trampas medidas (02-10-2026)

- **`prueba-rezagada.py` da verde de más:** su expresión de notas no reconoce «(v5.84, fila …)» —la versión seguida de coma, la forma usada desde la v5.50—. Medido con una copia: última versión 0 → 1 y histórico 40 → 271. Fila `DZ-C1` del enrutador; hasta que se arregle, los criterios se miran a mano.
- **`docs-fresh.py` no ve los `DA-EST` ni las notas `NT`:** para esos elementos se barre por frase en los derivados.
- Una nota de versión no se escribe dentro de un paréntesis en cursiva (`*(…)*`): el asterisco interior cierra la cursiva. Va fuera.
- En una fila del enrutador, una frase entre « » sobre un elemento `INV` no la puede comprobar `citas-verificadas.py` (busca en el §16 del BRD, no en la evidencia): va sin comillas.
- Una salida de más de ~3.000 palabras va al scratchpad, no a la conversación (tres barridos de 17 a 26 KB entraron igual el 02-10).
- El guardián solo deja escribir el BRD a la sesión donde el dueño lanzó la skill.

## Trampas medidas (03-10-2026, v5.107)

- **Bash: un heredoc con apóstrofes o `'''` revienta** con «unexpected EOF» y no escribe nada. Los scripts que llevan texto del BRD se escriben con la herramienta Write y se corren con `python`.
- **Fin de línea:** `docs/correcciones-brd-pendientes.md` está en CRLF; el BRD, el historial y los derivados, en LF. El script que agrega filas al enrutador detecta el fin de línea del archivo y lo respeta.
- **`frases-viejas.py` no marca nada** cuando los «decía» van al historial, que es lo que hace el aplicador: el barrido de los derivados es por frases, a mano, con dos juegos de palabras.
- **`docs-fresh` nombra un documento por CUALQUIER cita a un ID tocado** (28 en la v5.107; repetían lo viejo 14). La estampa sube con la nota que dice cuántos tramos se corrigieron y cuántas líneas nombró el control.
- **`decisiones-abiertas.py` clasifica una marca por sus primeros 200 caracteres:** el «se mide con …» de un `[A CALIBRAR]` va antes de esa marca o la cuenta como sin clasificar. Y dentro de una marca no van backticks (ya está en un code span).
- **La cacería profunda no corre en la aplicación de una versión:** el aviso de las 8 versiones se dice en el mensaje de cierre y se ofrece; no se lanza sola.

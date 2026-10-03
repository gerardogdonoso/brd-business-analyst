ENCARGO — lector de la cacería profunda del BRD, paquete {L}

Eres LECTOR, no autor. Tu trabajo es encontrar CONTRADICCIONES DE SIGNIFICADO entre elementos del BRD que los controles mecánicos no ven, leyendo tu paquete (unos {N} elementos) en lotes. No editas nada de `docs/` ni de `tools/`: solo escribes en la carpeta de trabajo (SP) = C:/Users/User/AppData/Local/Temp/claude/C--Users-User-Projects-agentesIA/645e33c8-b812-41ef-87fa-0fa74699c87b/scratchpad/cp

QUÉ ES EL BRD. `docs/BRD.md` es la fuente de verdad del negocio de agentesIA: agentes de inteligencia artificial que atienden al público de pymes chilenas, en tres productos (Ármalo, Pedidos, Cazador). Cada elemento es una fila con ID: RN regla, CA criterio de aceptación, PR proceso, AL alcance, DA-* dato, CE criterio de éxito, PZ priorización, RE restricción, RG riesgo, PE pendiente, CB caso borde. Quien programe este producto leerá cada elemento SIN poder repreguntar y escribirá el código y la prueba que lo cumplen: por eso dos elementos que se contradicen son un defecto aunque cada uno esté bien escrito solo. Entre la v5.96 y la v5.108 el BRD cambió en trece versiones —sobre todo el cobro: la forma de cobrar quedó UNA para Cazador y Pedidos, y entró la nota de vocabulario NT-010 «caso»— y nadie lo ha leído entero buscando contradicciones desde la v5.95. En tu lote cada elemento dice «CAMBIO en vX» si cambió en ese lapso: LAS CONTRADICCIONES MÁS PROBABLES ESTÁN ENTRE UN ELEMENTO QUE CAMBIÓ Y OTRO QUE NO SE ENTERÓ.

CÓMO LEER (en este orden, todo con Bash o PowerShell):
1. `python "SP/leer.py" {L} --marco 1` y `python "SP/leer.py" {L} --marco 2`: las diez notas de vocabulario (NT-001 a NT-010) y las tres relaciones del dueño (RN-380 mapa de entidades, RN-362 Propietario y Asignado, RN-311 niveles). Léelas ENTERAS primero: mandan sobre cualquier regla que las contradiga.
2. Luego los lotes, uno tras otro: `python "SP/leer.py" {L}` (cada llamada imprime el SIGUIENTE lote; `--lote K` repite el lote K sin sumar al registro; `--estado` dice cuántos van). Cada elemento sale con su ID, las versiones en que cambió, a quién cita y quién lo cita. Los elementos de un lote son parecidos entre sí por tema: léelos como un grupo.
3. Después de CADA lote, antes de pedir el siguiente:
   (a) FICHA: agrega a `SP/fichas_{L}.md` una línea por elemento que afirme algo que otro elemento podría contradecir (actor que hace o decide; número con su unidad; lista cerrada con SUS VALORES; valor por defecto; plazo u orden; alcance —dentro o fuera—, producto o nivel al que aplica). Formato: `ID | quién | qué | números | lista | por defecto | alcance`, máximo 30 palabras, con los valores copiados tal cual;
   (b) COMPARA el lote contra sí mismo y contra tus fichas anteriores (usa grep sobre `SP/fichas_{L}.md`);
   (c) cada contradicción que encuentres entra de inmediato a `SP/hallazgos_{L}.jsonl` (formato abajo), no al final.
4. Cuando `leer.py` diga FIN, haz una última pasada sobre tus fichas completas buscando pares de lotes distintos que se contradigan, y escribe el informe final.

QUÉ ES UNA CONTRADICCIÓN (pon la clase en `clase`):
- `negacion-global`: un elemento niega en general («no hay X fuera de Y», «nunca», «solo») y otro establece X por otra vía.
- `lista-cerrada`: dos listas cerradas del mismo conjunto con valores distintos, o una lista que otro elemento rebasa.
- `numero`: dos valores distintos (plazo, umbral, tope, cantidad, porcentaje, precio) para la misma cosa.
- `actor`: dos elementos asignan la misma conducta o decisión a actores distintos, o contradicen las relaciones del marco (RN-380, RN-362, RN-311) o las notas de vocabulario.
- `orden-o-momento`: orden, ventana o momento distinto para la misma secuencia.
- `alcance`: uno incluye (o excluye) un producto, nivel, canal o tipo de cuenta que el otro excluye (o incluye).
- `promesa-atribuida`: un elemento dice que otro hace o garantiza algo que ese otro no dice.
- `prueba-legisla`: un criterio de aceptación (CA) cuyo «entonces» introduce o contradice una decisión que ninguna regla enuncia, o verifica la versión vieja de la regla.
- `valor-por-defecto`: valores por defecto o excepciones incompatibles.
- `vocabulario`: la misma palabra para dos cosas, o dos palabras para la misma cosa, contra las notas de vocabulario.
NO son hallazgos: una regla general y su excepción declarada; dos reglas que se complementan; diferencias de redacción que no cambian lo que alguien tendría que programar; lo marcado DEROGADO. Si ves una ausencia («el BRD no dice X») no es de este encargo.

REGLAS QUE UN SCRIPT TE COBRA DESPUÉS:
- CITA TEXTUAL O NO HAY HALLAZGO. `cita_a` y `cita_b` se copian LITERALES del texto impreso (hasta 220 caracteres cada una, sin «…», sin paráfrasis, sin comillas inventadas); un script las busca dentro de cada elemento y la fila cuya cita no aparezca queda descartada.
- ANTES DE ESCRIBIR CADA HALLAZGO corre `python "SP/cita.py" A B` (dice si A y B se citan entre sí) y `python tools/vecinos-brd.py A B` desde la raíz del repositorio C:/Users/User/Projects/agentesIA (son listas de IDs, baratas). Si algún vecino puede cambiar la lectura —acota, exceptúa o corrige—, ábrelo con `python tools/elemento.py <ID>` (trae su vecindario: úsalo solo para esto) o con `python tools/elemento.py <ID> --solo-texto` para leer solo su texto, y anótalo en `vecinos_leidos`. Si A y B SE CITAN igual puedes reportarlo, con `se_citan: true`.
- NO INVENTES. Si tu lectura necesita algo que el texto no dice, es `confianza: baja` y lo declaras en `supuesto`. Redacta cada frase con el sujeto escrito: nada de «eso», «lo anterior» ni pronombres con dos dueños posibles.
- UN PAR, UNA VEZ. Dos hallazgos que comparten un elemento son filas distintas solo si la contradicción es distinta.
- COBERTURA HONESTA. Lo que no alcances a leer con atención lo declaras `NO-LEÍDA` por ID en tu informe. No rellenes.
- ECONOMÍA. No vuelques el BRD ni listados enteros; no abras con vecindario completo lo que puedes leer con `--solo-texto`; no escribas fuera de SP.

FORMATO de cada línea de `SP/hallazgos_{L}.jsonl` (una línea JSON). ESCRÍBELA SIEMPRE EN UTF-8 EXPLÍCITO, con Python (`open(ruta, "a", encoding="utf-8")` y `json.dumps(..., ensure_ascii=False)`); NO uses `Add-Content`, `Out-File` ni `>>` de PowerShell: guardan en la codificación de Windows y rompen las tildes y las comillas «». Lo mismo para `SP/fichas_{L}.md`.
{"id": "H-{L}-01", "par": ["RN-123","CA-456"], "clase": "numero", "cita_a": "texto literal de RN-123", "cita_b": "texto literal de CA-456", "por_que": "una o dos frases: qué dice cada uno y en qué choca", "se_citan": false, "vecinos_leidos": ["RN-789"], "confianza": "alta|media|baja", "supuesto": "", "tocaria_ceder": "tu lectura de cuál de los dos parece el desactualizado y por qué (es lectura tuya, no decisión del dueño)", "lote": 7}

INFORME FINAL (máximo 300 palabras, en español): lotes leídos; los NÚMEROS de los lotes que leíste más rápido y los de atención media (un script los transforma en elementos: sin números, la cobertura queda sin medir); número de hallazgos por clase; IDs `NO-LEÍDA`; qué parte del paquete recorriste con atención y cuál rápido; y qué NO puede verificar el script. No pegues los hallazgos: están en el archivo.

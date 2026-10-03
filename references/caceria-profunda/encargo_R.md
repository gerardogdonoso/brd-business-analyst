ENCARGO — lector de la RELECTURA BIDIRECCIONAL de la cacería profunda del BRD, paquete {L}

Eres LECTOR, no autor. Tu trabajo es encontrar CONTRADICCIONES DE SIGNIFICADO entre un elemento del BRD que CAMBIÓ y los elementos que lo citan o que él cita, leyendo tu paquete (unas {N} entradas) en lotes. No editas nada de `docs/` ni de `tools/`: solo escribes en la carpeta de trabajo (SP) = C:/Users/User/AppData/Local/Temp/claude/C--Users-User-Projects-agentesIA/645e33c8-b812-41ef-87fa-0fa74699c87b/scratchpad/cp

QUÉ ES EL BRD. `docs/BRD.md` es la fuente de verdad del negocio de agentesIA: agentes de inteligencia artificial que atienden al público de pymes chilenas, en tres productos (Ármalo, Pedidos, Cazador). Cada elemento es una fila con ID: RN regla, CA criterio de aceptación, PR proceso, AL alcance, DA-* dato, CE criterio de éxito, PZ priorización, RE restricción, RG riesgo, PE pendiente, CB caso borde, NT nota de vocabulario. Quien programe este producto leerá cada elemento SIN poder repreguntar y escribirá el código y la prueba que lo cumplen: por eso dos elementos que se contradicen son un defecto aunque cada uno esté bien escrito solo.

QUÉ ES ESTA ETAPA. Entre la v5.96 y la v5.108 cambiaron 114 elementos vivos del BRD (sobre todo el cobro: la forma de cobrar quedó UNA para Cazador y Pedidos, y entró la nota de vocabulario NT-010 «caso»). El método manda releer cada cambio en las DOS direcciones: **(b) A QUIÉN CITA el elemento que cambió** —suele nombrar a los viejos como respaldo y, al mismo tiempo, cambiar una de sus cláusulas sin decirlo: el citado queda vivo diciendo lo de antes— y **(a) QUIÉN LO CITA** —un elemento, y sobre todo un criterio de aceptación, que todavía dice o prueba lo que el cambiado decía ANTES—. Otros cinco lectores leen el BRD entero por tema y ya ven juntos los pares que cayeron en un mismo paquete; **a ti te tocan solo los pares que cayeron en paquetes DISTINTOS: nunca estuvieron en la cabeza de un mismo lector.**

Cada entrada de tu paquete trae, por un elemento que cambió: (1) **LO QUE CAMBIÓ** desde la v5.95, como diferencia de palabras —`[-quitado-]` y `{+agregado+}`; «(…)» resume texto que no cambió—; (2) su **TEXTO DE HOY** entero; (3) la **CABEZA** (los primeros 300 caracteres) de cada vecino de otro paquete, con la marca `[cita a]` (el cambiado lo cita) o `[lo cita]` (el vecino cita al cambiado) y el aviso «CAMBIÓ también» si el vecino cambió en el mismo lapso. Un elemento con muchos vecinos viene partido en entradas «ID·2», «ID·3»…, que repiten lo que cambió y la cabeza del cambiado.

CÓMO LEER (en este orden, todo con Bash o PowerShell):
1. `python "SP/leer_r.py" {L} --marco 1` y `python "SP/leer_r.py" {L} --marco 2`: las diez notas de vocabulario (NT-001 a NT-010) y las tres relaciones del dueño (RN-380 mapa de entidades, RN-362 Propietario y Asignado, RN-311 niveles). Léelas ENTERAS primero: mandan sobre cualquier regla que las contradiga.
2. Luego los lotes, uno tras otro: `python "SP/leer_r.py" {L}` (cada llamada imprime el SIGUIENTE lote; `--lote K` repite el lote K sin sumar al registro; `--estado` dice cuántos van).
3. Por cada entrada, antes de pasar a la siguiente:
   (i) lee LO QUE CAMBIÓ y el texto de hoy: di para ti, en una frase, qué decía antes y qué dice ahora;
   (ii) recorre las cabezas de los vecinos y pregúntate por cada uno: ¿el vecino `[lo cita]` todavía dice, exige o prueba lo que el cambiado decía ANTES (lo `[-quitado-]`)? ¿el cambiado le atribuye a un vecino `[cita a]` algo que ese vecino no dice, o contradice una cláusula del vecino que nombra como respaldo? ¿un criterio que lo cita verifica la versión vieja?
   (iii) cuando la cabeza no alcance para decidir y el vecino pueda chocar con lo que cambió, ábrelo entero con `python tools/elemento.py <ID> --solo-texto` desde la raíz del repositorio C:/Users/User/Projects/agentesIA. No abras los vecinos cuya cabeza ya muestra que tratan otra cosa.
   (iv) cada contradicción entra de inmediato a `SP/hallazgos_{L}.jsonl`, no al final.
4. PASO OBLIGATORIO antes de escribir CADA hallazgo: corre `python "SP/cita.py" A B` (dice si A y B se citan) y `python tools/vecinos-brd.py A B` desde la raíz del repositorio; abre con `python tools/elemento.py <ID>` (trae su vecindario) todo vecino que pueda acotar, exceptuar o corregir la lectura, y anótalo en `vecinos_leidos`. Si un vecino resuelve la tensión, no hay hallazgo.
5. Cuando `leer_r.py` diga FIN, escribe el informe final.

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
NO son hallazgos: una regla general y su excepción declarada; dos reglas que se complementan; diferencias de redacción que no cambian lo que alguien tendría que programar; un vecino que cita al cambiado por algo que NO cambió; lo marcado DEROGADO. Si ves una ausencia («el BRD no dice X») no es de este encargo.

REGLAS QUE UN SCRIPT TE COBRA DESPUÉS:
- CITA TEXTUAL O NO HAY HALLAZGO. `cita_a` y `cita_b` se copian LITERALES del texto de cada ELEMENTO (hasta 220 caracteres cada una, sin «…», sin paráfrasis, sin comillas inventadas): del TEXTO DE HOY del cambiado, de la cabeza impresa del vecino o del vecino abierto con `--solo-texto`. **NUNCA copies de la línea LO QUE CAMBIÓ**: las marcas `[-…-]` y `{+…+}` y el «(…)» no existen en el BRD, y lo `[-quitado-]` ya no está en él. Un script busca cada cita dentro de su elemento y descarta la fila cuya cita no aparezca.
- En `par` va el ID real, sin «·2»: `["RN-323","CA-462"]`.
- NO INVENTES. Si tu lectura necesita algo que el texto no dice, es `confianza: baja` y lo declaras en `supuesto`. Redacta cada frase con el sujeto escrito: nada de «eso», «lo anterior» ni pronombres con dos dueños posibles.
- UN PAR, UNA VEZ. Dos hallazgos que comparten un elemento son filas distintas solo si la contradicción es distinta.
- COBERTURA HONESTA. Lo que no alcances a leer con atención lo declaras `NO-LEÍDA` por ID en tu informe. No rellenes.
- ECONOMÍA. No vuelques el BRD ni listados enteros; no abras con vecindario completo lo que puedes leer con `--solo-texto`; no escribas fuera de SP.

FORMATO de cada línea de `SP/hallazgos_{L}.jsonl` (una línea JSON). ESCRÍBELA SIEMPRE EN UTF-8 EXPLÍCITO, con Python (`open(ruta, "a", encoding="utf-8")` y `json.dumps(..., ensure_ascii=False)`); NO uses `Add-Content`, `Out-File` ni `>>` de PowerShell: guardan en la codificación de Windows y rompen las tildes y las comillas «».
{"id": "H-{L}-01", "par": ["RN-123","CA-456"], "clase": "prueba-legisla", "direccion": "lo-cita|cita-a", "cita_a": "texto literal de RN-123", "cita_b": "texto literal de CA-456", "por_que": "una o dos frases: qué decía el cambiado antes, qué dice ahora y en qué choca el vecino", "se_citan": true, "vecinos_leidos": ["RN-789"], "confianza": "alta|media|baja", "supuesto": "", "tocaria_ceder": "tu lectura de cuál de los dos parece el desactualizado y por qué (es lectura tuya, no decisión del dueño)", "lote": 7}

INFORME FINAL (máximo 300 palabras, en español): lotes leídos; los NÚMEROS de los lotes que leíste más rápido y los de atención media (un script los transforma en entradas: sin números, la cobertura queda sin medir); número de hallazgos por clase y por dirección; cuántos vecinos abriste enteros; IDs `NO-LEÍDA`; y qué NO puede verificar el script. No pegues los hallazgos: están en el archivo.

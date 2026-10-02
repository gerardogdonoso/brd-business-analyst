ENCARGO — VERIFICADOR {V} de la cacería profunda del BRD (segunda lectura A CIEGAS)

Eres VERIFICADOR, no autor. No editas nada de `docs/` ni de `tools/`: solo escribes en la carpeta de trabajo (SP) = C:/Users/User/AppData/Local/Temp/claude/C--Users-User-Projects-agentesIA/736f4882-2b73-4e27-822e-a4176c4fe640/scratchpad

QUÉ ES ESTO. `docs/BRD.md` es la fuente de verdad del negocio de agentesIA (agentes de inteligencia artificial para pymes chilenas; productos Ármalo, Pedidos y Cazador). Cada elemento es una fila con ID (RN regla, CA criterio de aceptación, PR proceso, AL alcance, DA-* dato, CE criterio de éxito, PZ priorización, RE restricción, RG riesgo, PE pendiente, CB caso borde, NT nota de vocabulario). Quien programe lo leerá SIN poder repreguntar: dos elementos que se contradicen son un defecto aunque cada uno esté bien escrito solo.

Siete lectores recorrieron el BRD buscando pares de elementos que se contradicen. Tu paquete es `SP/verif_{V}.md`: unos 26 pares, cada uno con los IDs, la clase que le puso el primer lector, las citas literales que ese lector sacó de cada elemento, en qué versiones cambió cada elemento y los IDs vecinos. NO tienes el razonamiento del primer lector y no lo busques: tu trabajo es leer tú los dos elementos y decidir si de verdad se contradicen. Lo que la cita muestra puede estar sacado de contexto: lo que decide es el elemento ENTERO y lo que acota su vecindario.

CÓMO TRABAJAR:
1. Lee primero el marco que manda sobre cualquier regla: `python "SP/leer.py" L1 --marco 1` (las nueve notas de vocabulario) y `python tools/elemento.py RN-380 RN-362 RN-311 --solo-texto` (mapa de entidades, Propietario y Asignado, niveles; se corre desde la raíz C:/Users/User/Projects/agentesIA).
2. Lee `SP/verif_{V}.md` con Read. Luego, par por par, en ese orden:
   (a) abre LOS DOS elementos en UNA sola llamada: `python tools/elemento.py <A> <B> --solo-texto` y léelos enteros;
   (b) si lo que cada uno dice depende de otros elementos, mira sus listas de vecinos (en tu archivo y con `python tools/vecinos-brd.py <A> <B>`) y abre como MÁXIMO DOS vecinos por par —los que acoten, exceptúen, corrijan o definan lo que dice cualquiera de los dos— en una sola llamada con `--solo-texto`. Para ver el vecindario completo de un elemento (15 a 25 KB) existe `python tools/elemento.py <ID>` sin `--solo-texto`: úsalo solo si el par depende de lo que ese elemento cita o de quién lo cita;
   (c) escribe el veredicto de ese par en `SP/veredictos_{V}.jsonl` ANTES de pasar al siguiente (Python, UTF-8 explícito: `open(ruta, "a", encoding="utf-8")` y `json.dumps(..., ensure_ascii=False)`; NO uses `Add-Content`, `Out-File` ni `>>` de PowerShell).

VEREDICTOS (campo `veredicto`):
- `contradice`: los dos no pueden regir a la vez para el mismo caso; o uno dice que el otro hace o garantiza algo que ese otro no dice y la atribución falsa llevaría a programar mal; o un criterio de aceptación prueba la versión vieja de la regla; o una lista, número, actor o alcance difiere sin que ninguno declare la diferencia.
- `en-parte`: chocan solo para una parte del alcance o solo bajo un supuesto que el texto no da por escrito; di cuál.
- `compatible`: coexisten (excepción declarada en el propio elemento o en un vecino, objetos distintos, reglas que se complementan, o diferencia de redacción que no cambia lo que se programa).
- `no-decidible`: el BRD no da lo suficiente; di exactamente qué falta.

OTROS CAMPOS: `cede` (A, B, ambos, ninguno o no-se: cuál elemento tendría que cambiar) y `por_que_cede` (una frase apoyada en lo escrito: versión posterior, nota o relación del marco que manda, jerarquía de definición); `resuelve` = quién resuelve el hueco, una de seis: `derivado` (solo una lectura es consistente con lo ya escrito: dices de dónde sale), `investigar` (la industria o la ley ya lo resolvieron), `cuenta` (es criterio comercial del negocio cliente), `dueno` (decisión del dueño: hay dos salidas legítimas y nada en el documento ni en la industria decide), `sistema` (necesita el sistema construido) o `trd` (es mecanismo); `fuente`: qué elemento o fuente lo respalda; `cambia_lo_que_se_programa`: sí, no o no sé; `vecinos_abiertos`: los IDs que abriste.

REGLAS QUE UN SCRIPT TE COBRA: `cita_clave_a` y `cita_clave_b` se copian LITERALES del texto de cada elemento (hasta 200 caracteres, sin «…», sin paráfrasis); un script las busca. NO INVENTES: si necesitas suponer algo que el texto no dice, es `en-parte` o `no-decidible` y lo escribes en `razon`. Cada frase con el sujeto escrito: nada de «eso» ni pronombres con dos dueños posibles. Si no alcanzas a verificar un par, no lo rellenes: lo declaras en el informe por su número. ECONOMÍA: no vuelques listados enteros; un par, una llamada para abrir los dos.

FORMATO de cada línea de `SP/veredictos_{V}.jsonl`:
{"n": 12, "par": ["RN-123","CA-456"], "veredicto": "contradice|en-parte|compatible|no-decidible", "razon": "una o dos frases: qué dice cada elemento y por qué chocan o no", "cita_clave_a": "...", "cita_clave_b": "...", "cede": "A|B|ambos|ninguno|no-se", "por_que_cede": "...", "resuelve": "derivado|investigar|cuenta|dueno|sistema|trd", "fuente": "...", "cambia_lo_que_se_programa": "si|no|no se", "vecinos_abiertos": ["RN-789"]}

INFORME FINAL (máximo 200 palabras, en español): cuántos pares por veredicto; los números que no alcanzaste a verificar; y cualquier par donde el primer lector probablemente leyó mal (di por qué en una frase).

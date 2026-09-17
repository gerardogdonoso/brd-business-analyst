# Evidencia y relatos de `brd-business-analyst` — texto original mudado desde `SKILL.md` el 16-09-2026

> **Qué es esto:** el relato que sostenía cada regla —fechas, casos medidos, citas del dueño, cifras— tal como estaba escrito en `SKILL.md` antes de adelgazarla. **La regla vive en `SKILL.md`; aquí vive su porqué.** Se abre cuando alguien pregunta por qué una regla es como es, o antes de proponer quitarla. Nada de esto se implementa ni se relee en cada invocación: por eso salió de la skill. Cada bloque conserva el texto íntegro bajo el título de la regla que sostenía.

## §3 · principio 8

| 8 | **Términos del usuario**: Usar exactamente sus palabras. Sin sinónimos propios. 🔴 **Y REGISTRAR SUS PALABRAS NO ES REGISTRAR SU DECISIÓN: cuando su respuesta cierra una MITAD de la pregunta, se nombra la otra en el mismo turno.** ⚠️ **Caso medido (04-09-2026): a *«¿el producto barato incluye la voz?»* el dueño respondió *«lo que no hace es LLAMAR»*. Eso cerró el saliente y dejó abierto el entrante; nadie nombró la mitad abierta, y el componente más caro del catálogo quedó regalándose SIN TECHO en el plan barato durante versiones.** **Escribir sus palabras con fidelidad y vigilar lo que quedó abierto son DOS trabajos, no uno.** |

---

## §3 · principio 11

| 11 | **Devolver la escena antes de escribir la regla**: antes de redactar una regla sobre **cómo opera el negocio del usuario** —quién entrega el acceso, quién nombra a quién, qué pasa cuando alguien se va—, describirle la escena **en una frase** y esperar su sí. Cuesta diez segundos y evita reescribir. Evidencia: en una sola sesión se escribieron cuatro reglas de operación por inferencia y el dueño corrigió las cuatro; **las cuatro veces su modelo real era MÁS SIMPLE que el inferido**, así que el error no fue faltar a un detalle sino agregar maquinaria que nadie pidió. |

---

## §3 · principio 12

| 12 | **La pregunta llega con su tarea hecha**: antes de pedirle al usuario una decisión o una validación, clasificarla. (a) Si la respuesta **se infiere del propio documento** —solo una opción es consistente con lo ya escrito—, no se pregunta: se aplica con la derivación citada y estado `[SUPUESTO]`, y el usuario veta. (b) Si **la industria ya lo resolvió** (inasistencias, pedidos cancelados, notificaciones, límites de frecuencia), se investiga ANTES de proponer: la propuesta llega con su contraste adjunto — nunca proponer a ciegas para investigar después de que el usuario diga "no sé". (c) Solo la **preferencia genuina de negocio** se pregunta, máximo 3 por turno. Evidencia: en una sesión, dos reglas propuestas sin contraste hicieron decir al dueño "no sé qué puedo decidir, ¿qué es lo recomendado?"; la investigación posterior confirmó ambas — tres turnos de supervisión que el contraste previo habría vuelto uno.
**Y el principio rige la LISTA, ítem por ítem, no solo la pregunta suelta.** Entregar N consecuencias
de una decisión sin marcar cuáles pide el usuario y cuáles se derivan **le transfiere el trabajo de
clasificarlas**, que es precisamente lo que este principio existe para evitar: la lista se ve como
información y funciona como tarea. Caso registrado: de seis consecuencias presentadas juntas, cuatro
eran derivables y ya estaban resueltas, y el usuario tuvo que responder *"no sé para qué me las
mencionas, ¿tengo que decidir?"* antes de poder opinar sobre las dos que sí eran suyas. **Cada ítem
sale etiquetado con quién decide** —del usuario, o derivado y ya aplicado con su derivación citada—,
y los derivados van después, no intercalados. Y de cuatro preguntas de un mismo turno, dos volvieron con "conviene investigar cuál es el estándar": una pregunta sin tarea hecha le transfiere el trabajo al supervisor, que es exactamente la persona cuyo trabajo esta skill existe para reducir. **Y la pregunta de catálogo llega CON SU ESCENA** —qué es la cosa, dónde se ve, qué dispara— **nunca en abstracto**: dos casos en un mismo día (28-08) de lista preguntada sin escena produjeron una respuesta sobre OTRO objeto (se preguntó por los valores que el agente DETECTA y el dueño respondió por el TONO con que responde) y un *«no entiendo el contexto»* — la escena convierte la pregunta en decisión; el abstracto la convierte en adivinanza. **Y ante la duda de QUIÉN decide algo, el default es preguntarse primero *«¿ya lo resolvió la industria o la ley?»* — NUNCA asignárselo al usuario directamente: asignarle lo investigable lo invita a INVENTAR, que es justo lo que esta skill existe para impedir.** Evidencia: dos veces en una misma ventana (28-08) el analista clasificó como «decisión del dueño» algo que la ley y la literatura ya tenían resuelto (una relación entre agentes con patrón publicado; un filtro de tácticas con lista negra regulatoria de la FTC), y las dos veces el dueño lo devolvió: *«el que decide no soy yo — no estamos escribiendo las leyes de la industria desde cero; datos empíricos, no supuestos»*. |

---

## §3 · principio 12-bis

| 12-bis | 🔴 **ANTES DE ESCRIBIR O TOCAR UN ELEMENTO, SE LEE SU VECINDARIO DE CITAS: a quién cita, quién lo cita, y con qué criterios comparte cobertura** (`vecinos-brd.py`). **La skill hermana lo exige en cada encargo desde hace versiones; ésta —la que ESCRIBE— no lo mencionaba ni una vez, y ahí estaba el hueco.** 🔴 **Evidencia medida en una sola jornada (04-09-2026): de once defectos hallados leyendo el documento entero, SEIS eran «dos reglas correctas que nadie leyó juntas», y los seis entre elementos que NO se citaban** — dos listas declaradas cerradas en sentidos opuestos (una exigía salida «otro», la otra negaba por omisión: juntas abrían un agujero de permisos); una regla que prohibía tocar el contexto entre turnos contra otra que obligaba a corregir el precio a mitad de conversación; una regla que atribuía a otra una promesa que la otra no hacía; una cita de ida sin vuelta que dejaba leer «escalamiento» como sinónimo de «inmediato»; la única regla que autoriza el cruce de material entre cuentas competidoras SIN ninguna de sus guardas —vivían en los criterios—; y una regla que exigía «un solo escritor por dominio» sin la lista de dominios. ⚠️ **El defecto NO se ve escribiendo el elemento: cada uno es correcto solo. Se ve leyendo el par, y por eso la lectura del vecindario es un PASO, no una recomendación.** |

---

## §3 · principio 13

| 13 | 🔴 **Toda decisión del dueño se CONTRASTA contra el estándar, y el contraste queda escrito aunque él no cambie de idea.** Esta skill está construida para registrarlo fielmente —*sus palabras exactas*, `[CONFIRMADO]` = *lo dijo*— y **eso, solo, la vuelve taquígrafa**: el dueño decide A, la industria publicó B, y nadie se lo dice. **Cuando exista una respuesta publicada y DISTINTA a lo que él acaba de decidir, se le dice en el momento, en tres partes: (1) qué dice el estándar y con qué fuente, (2) dónde queda su decisión respecto de él —por encima, por debajo, o simplemente en otra rama—, y (3) qué se recomienda y POR QUÉ.** ⚠️ **Contrasta, NO veta:** su decisión se aplica igual, sigue siendo `[CONFIRMADO]` y no se re-litiga después — insistir es desobedecer, no analizar. ✅ **Y el contraste se REGISTRA aunque él mantenga su decisión**, con su razón si la da: *«lo sabíamos y elegimos otra cosa»* y *«no lo sabíamos»* son estados distintos, y solo el primero se puede defender ante un cliente, un inversionista o un tribunal. **Dónde queda escrito, para que no dependa de la memoria de nadie:** el hallazgo va a **§18 como `[INV-XXX]` con su fuente**, y **el elemento decidido conserva su `[CONFIRMADO]`** y suma la nota *«contrastado contra `INV-XXX`: el estándar hace Y; se elige Z porque …»*. Si la decisión es posterior a la aprobación, su fila de **§19** lo dice también. **Cuándo se dispara, para que no sea ruido:** solo cuando la diferencia tiene **costo medible** —dinero, exposición legal, un compromiso que no se va a poder cumplir, o un número que no se va a sostener—. **No se dispara** sobre preferencias, sobre lo que la industria no ha zanjado, ni sobre lo que ya se contrastó una vez. |

---

## §3 · principio 15

| 15 | 🔴 **ANTES DE PREGUNTARLE ALGO AL USUARIO, CLASIFICAR DE QUIÉN ES EL HUECO — y son SEIS montones, no dos.** El principio 12 ya decía que lo investigable se investiga; **le faltaban dos salidas que aparecen todo el tiempo y que, sin nombre, terminan en el usuario.** **(a) SE DERIVA DEL DOCUMENTO** → se aplica con la derivación citada, el usuario veta. **(b) LA INDUSTRIA O LA LEY YA LO RESOLVIERON** → se investiga ANTES de proponer. 🔑 **(c) ES CRITERIO COMERCIAL DEL NEGOCIO DE SU CLIENTE** → **no lo decide ni el usuario ni el producto: LO DECLARA LA CUENTA, y el producto pone el default.** Es la salida que más se olvida: en un caso real, *«cuántos días de gracia antes de dar por roto un compromiso de pago»* se le presentó al dueño como decisión suya y él la devolvió —*«esto no es un tema aparte del framework»*—, porque una panadería y una clínica no tienen por qué coincidir; **el propio documento ya usaba ese patrón tres veces y nadie lo había nombrado.** **(d) DECISIÓN DEL USUARIO** → solo lo que no cae en (a), (b) ni (c), **con la escena y con la constancia de que se buscó**. 🔑 **(e) NECESITA EL SISTEMA CONSTRUIDO** → **no se decide: se deja con su CONDICIÓN DE CIERRE ESCRITA dentro de la marca** —qué se mide, dónde y cuándo—, porque un número inventado hoy se lee mañana como medido. **(f) ES MECANISMO** → se anota para la fase técnica y no se resuelve aquí. ⚠️ **Las tres preguntas que ordenan el reparto, en este orden: ¿lo dice ya otra parte del documento? ¿lo publica la industria o lo fija la ley? ¿es política del negocio de su cliente?** Si alguna responde sí, **no se pregunta**. 🔴 **Evidencia del costo (03-09-2026): de siete «decisiones del dueño» presentadas juntas, CINCO no lo eran** —una estaba investigada y escrita **en el mismo párrafo** donde se le preguntó, dos se derivaban del documento y dos las tenía resueltas la industria—. **El control `decisiones-abiertas.py` de `crea-suite` cuenta las marcas abiertas y las reparte por montón, para que «se lo pregunté sin investigar» deje de ser invisible.** |

---

## §3 · principio 15-ter

| 15-ter | 🔴 **TODA CIFRA QUE VA A DECIDIR ALGO DECLARA CÓMO SE MIDIÓ, Y SE CONTRASTA ANTES DE USARLA.** *(Escrito el 08-09-2026 porque el dueño lo cazó con el síntoma nombrado tres veces y la medicina sin escribir: «si tienes el síntoma y el diagnóstico de lo que te pasa, ¿por qué no le has dado la medicina para que esto viva en la skill y no se pierda?».)* 🔴 **Evidencia: CUATRO mediciones equivocadas en una sola jornada, y las cuatro con la misma forma — el instrumento traía un supuesto NO DECLARADO sobre la forma del dato:** **(1)** *«18 filas abiertas»* eran **12**: el detector daba por abierta toda fila con la marca original, y en este método **una fila resuelta CONSERVA su marca**. **(2)** *«38 citas con la forma vieja»* eran **66**, y la mayoría no estaba donde se dijo: **se contó un archivo y se supuso el resto**. **(3)** *«un elemento de 32.624 caracteres»* eran **5.404**: el medidor le atribuyó texto que vivía ENTRE elementos, no dentro. **(4)** un verificador reportó **seis citas inexistentes que existían las seis**: comparaba fragmentos sin tilde contra un texto con tildes. ✅ **LO QUE RIGE, y se comprueba mirando la propia cifra: (a)** se nombra **QUÉ se contó y qué quedó fuera**; **(b)** antes de decidir, se contrasta contra **un caso conocido o un segundo instrumento**; **(c)** si dos mediciones del mismo objeto **discrepan, NO gana la más nueva: se abre un caso a mano y se mira**. ⚠️ **Y la regla ya existía A MEDIAS, lo que la vuelve más urgente que si no existiera: un control de este método la trae en su cabecera —*«ocho puntos de diferencia por una decisión de medición, así que la definición se declara o el número no significa nada»*— pero vivía en la cabecera de UN script. Una regla escrita donde solo la lee quien abre ese archivo no gobierna a quien cuenta a mano.** |

---

## §3 · principio 15-bis

| 15-bis | 🔴 **LOS SEIS MONTONES DE ARRIBA CLASIFICAN HUECOS DEL NEGOCIO — y por ese hueco las propuestas sobre el PROPIO MÉTODO entraban sin medir.** *(Escrito el 08-09-2026 porque el dueño lo cazó: «propones cosas suponiendo sin medir y haces una recomendación que no sabes si es una mejora o una regresión».)* **Léase el principio 15: nombra la industria, la ley, la cuenta cliente y al dueño. NO dice nada de proponer cambiar un control, una herramienta, un umbral o una skill** — y la asimetría se midió: de las reglas de producto de esa sesión, 6 de 6 llegaron con su investigación y su fuente; de las propuestas sobre el método, 1 de 5. ✅ **Lo que rige: una propuesta sobre el método llega con la cifra de ANTES, la de DESPUÉS y qué se rompería. Sin las tres se dice *«no lo sé, hay que medirlo»*.** ⚠️ **Evidencia: se propuso cambiar el contador de una cacería de versiones a días; al medirlo resultó falso en las dos mitades —el riesgo se acumula por CAMBIO, no por día— y la propuesta la desarmó quien la hizo.** 🔑 **Con su control, porque el texto solo no basta: `regresion-controles.py` avisa cuando un control DEJA DE HABLAR. Es la puerta de `RN-150` aplicada al método, y hasta ese día las herramientas del proyecto tenían CERO casos de prueba.** |

---

## §3 · principio 16

| 16 | 🔴 **LA NOTA DE CORRECCIÓN VA CORTA: EL RELATO DE LO QUE LA REGLA DECÍA ANTES SE MUDA, NO SE ACUMULA.** Esta skill corrige escribiendo *«(vX.YY: decía Z)»* dentro del elemento, **y eso convierte al documento en el almacén de su propia historia — justo en la línea que alguien va a programar.** 🔴 **Medido en un proyecto real el 03-09-2026: 133 notas de versión, 4% de los caracteres vivos, PERO CONCENTRADO — con elementos donde la historia era el 70% del texto.** ⚠️ **Y pesa más de lo que parece cuando quien construye es un modelo de lenguaje** *(vibe coding: el destinatario del documento es una sesión futura sin contexto)*: **cada frase sobre lo que la regla decía ANTES es una lectura que hay que descartar sola, y una lectura descartable mal leída es una regla equivocada en el código.** ✅ **Lo que rige: (1)** la nota se queda pero **en una frase** —qué cambió y por qué—; **(2)** el relato completo, el camino descartado y el contraste largo **se mudan al archivo de historia**, que comparte el espacio de IDs y se consulta; **(3)** lo caza `mapa-brd.py` **por CONCENTRACIÓN y no por promedio** —elemento con 35% o más de su texto en notas de versión—, porque el promedio esconde justo al elemento ilegible. ⚠️ **Lo que NO se muda: el contraste contra el estándar cuando el usuario eligió otra cosa** (principio 13) — pero va en una frase y con su `INV-XXX`, no con el relato entero. |

---

## §3 · principio 14

| 14 | 🔴 **Todo lo que se escribe —BRD o respuesta— se redacta en castellano normativo, y ACORTAR NO AUTORIZA A INTRODUCIR AMBIGÜEDAD.** 🔑 **Y esto NO contradice al principio 8: sus palabras exactas son la fuente del CONTENIDO —el término del negocio, la decisión, el porqué—; la SINTAXIS es responsabilidad del redactor.** Se conserva su vocabulario y se corrige la construcción: calcar su orden de palabras traslada al documento una ambigüedad que él no pidió, y **el lector del BRD es quien no puede repreguntar** — una frase con dos lecturas se resuelve en silencio y queda escrita en el código. **Las tres clases del defecto, con su nombre técnico:** **(a) Anfibología** *(ambigüedad sintáctica)* — la frase admite dos o más interpretaciones por orden confuso de las palabras o uso impreciso de pronombres (*«Juan fue al cine con Pedro en su auto»* → ¿de quién era el auto?). **(b) Referencia anafórica rota** *(deixis rota)* — un pronombre (*él, ella, su, suyo*) sin antecedente explícito, o ubicado entre dos sujetos posibles sin delimitar cuál es. **(c) Sujeto indeterminado o tácito ambiguo** — se omite el sujeto creyendo que el contexto lo aclara, y el verbo en tercera persona permite atribuir la acción a varias entidades ya mencionadas. ✅ **Las tres soluciones que la norma exige:** **especificar el nombre**, **reestructurar el orden de la oración**, o **sustituir el posesivo ambiguo por una construcción aclaratoria** (*«el de este»*, *«el de aquel»*). 🔴 **Y dos fallas de LÓGICA propias del resumen, distintas de la ambigüedad: (1)** afirmar que varios hallazgos *«son el mismo»* y enumerar a continuación problemas de naturaleza distinta —**compartir la causa raíz no los vuelve uno solo**—; **(2)** agrupar bajo una etiqueta común elementos que no la comparten, para que la lista cuadre. **Comprobaciones, verificables en la propia frase: si se afirma que varias cosas SON UNA, debe sostenerse ítem por ítem; y todo pronombre debe poder reemplazarse por su sustantivo sin que cambie el sentido.** ⚠️ **Aplica con más fuerza aquí que en cualquier otro documento: un `[RN]` ambiguo no lo caza ningún verificador de IDs, se aprueba en su puerta y baja a los criterios de aceptación** — que es donde una lectura equivocada se vuelve una prueba equivocada.  ⚠️ **Y las tres construcciones que casi siempre esconden el defecto, para revisarlas ANTES de enviar la frase y no después:** **(i) elipsis con artículo** —*«la del BRD»*, *«el de arriba»*, *«en las dos»*— cuando el sustantivo omitido no es el único posible en ese párrafo; **(ii) el posesivo *su / sus*** con dos antecedentes a la vista; **(iii) las impersonales** —*«hay que»*, *«se debe»*, *«queda por»*, *«corresponde»*— que borran a quien ejecuta la acción. **Las tres se corrigen del mismo modo: nombrando** — el sustantivo, el poseedor y el sujeto. *(Evidencia de que el aviso hace falta: esta misma regla se escribió y se rompió en la frase inmediatamente siguiente, con las tres construcciones a la vez.)* |

---

---

---

## Principios compartidos (sección entera)

## Principios COMPARTIDOS con la skill hermana — y por qué esta lista existe

**Estas dos skills se usan juntas y una escribe lo que la otra audita**, así que un principio sobre **cómo se trabaja** —no sobre qué se escribe— tiene que estar en las dos o no sirve. **Sin esta lista, un principio nuevo entra en una y la otra no se entera**, y nadie lo nota hasta que el defecto reaparece del lado que no lo tiene.

🔴 **Evidencia de que hace falta, del 03-09-2026:** se midieron los conceptos compartidos entre las dos y **cuatro no estaban en ninguna** —vivían solo en el `CLAUDE.md` de un proyecto, o sea que no viajaban al siguiente— y **uno se había escrito en la skill que AUDITA cuando el defecto lo produce la que ESCRIBE**. El dueño lo cazó con una sola pregunta: *«¿entonces las dos skills están perfectamente sincronizadas, porque un cambio afecta a la otra?»*.

**Los que van en las DOS, con su nombre:**

| Principio | Qué exige |
|---|---|
| **Investigar antes de proponer — Y ANTES DE AFIRMAR** | Lo que la industria o la ley ya resolvieron **se investiga ANTES**, nunca se pregunta primero. 🔴 **Y el 10-09-2026 se le agregó el tercer verbo, porque los dos primeros no alcanzaban:** la regla decía *proponer* y *preguntar*, **así que una AFIRMACIÓN de paso sobre el mundo de afuera no obligaba a abrir nada**. El caso: se afirmó que partir el flujo en dos llamadas al modelo *«encarece»* — al mirar los precios publicados resultó **+1% a +5%**, y lo caro era otra cosa. **Un precio, una tarifa, un umbral publicado, lo que una plataforma permite o lo que dice una norma NO se afirman de memoria: se abren.** Tercera vez que esta misma regla se queda corta por el verbo — nació para huecos del negocio, el 08-09 se extendió a las propuestas de método, y hoy a las afirmaciones |
| **Una regla vive donde se lee** | Un principio que gobierna el trabajo diario se copia al `CLAUDE.md` del proyecto: **una skill solo se carga cuando la invocan** |
| **Fuente recomprobable** | Cada hallazgo con dirección, documento, norma o fecha; lo abierto se separa de lo referido; la página de venta se marca |
| **Contraste registrado** | Cuando el dueño elige distinto del estándar, el contraste queda escrito **aunque no cambie de idea** |
| **Castellano normativo** | Acortar no autoriza a introducir ambigüedad: anfibología, referencia rota y sujeto tácito, con sus tres soluciones |
| **La historia sale del documento vivo** | Lo que dejó de regir se **muda** a su archivo y se consulta; no se acumula en la línea que alguien va a programar |
| **La corrección baja a la prueba** | Corregir una regla y dejar sus criterios con la formulación vieja **deja la prueba legitimando lo que la regla prohíbe**. Los criterios del elemento tocado se revisan **en la misma pasada** |
| **La unidad que se entrega al que codifica es la FUNCIONALIDAD, no el documento** | Lo global es la biblioteca; lo que se construye vive en `docs/specs/<NNN-nombre>/`, autocontenido, **con su historia, sus datos y su acuerdo en CUANDO / SI / ENTONCES**. Se inyecta solo lo que aplica a esa historia, nunca el documento entero. **Y el plan técnico se escribe por funcionalidad: el documento técnico global no bloquea** |
| **La cifra que decide declara cómo se midió** | Antes de usar un número para decidir se nombra **qué se contó y qué quedó fuera**, y se contrasta contra un caso conocido o un segundo instrumento. **Si dos mediciones del mismo objeto discrepan, no gana la más nueva: se abre un caso a mano** |
| **El vecindario se lee antes de escribir** | A quién cita, quién lo cita y con qué criterios comparte cobertura (`vecinos-brd.py`). El defecto que más se esconde no es la regla mal escrita: son dos reglas correctas que nadie leyó juntas *(está aquí como principio 12-bis; faltaba en esta tabla, que es el mecanismo de sincronía)* |
| **Texto o control, no los dos** | Si el defecto YA tenía su regla escrita y ocurrió igual, la medicina no es repetirla: es un control que la verifique. Una skill es la MEMORIA del método; un control es lo que OBLIGA *(está aquí como CONTRA-INDICACIÓN; faltaba en esta tabla)* |
| **Una propuesta sobre el MÉTODO llega medida** | Lo que la regla de investigar-antes-de-proponer NO cubría: cambiar un **control, una herramienta, un umbral o una skill** llega con **la cifra de ANTES, la de DESPUÉS y qué se rompería**. Sin las tres no se propone: se dice *«no lo sé, hay que medirlo»* |
| **El enunciado dice lo que rige** | La apertura de un elemento **es** la regla, **incluida su limitación**. Lo que la corrige, la acota o la distingue de otra cosa va **ANTES de la historia, nunca después**. 🔴 Medido el 09-09-2026 sobre un BRD real: **44 elementos abren enunciando y giran pasada la mitad**, hasta el 97% — y una regla de email abría diciendo que servía para reactivación cuando al 81% exige dominio propio. **Quien lee la cabeza codifica la versión equivocada y escribe la prueba que la aprueba**, y una sesión que codifica SIEMPRE lee la cabeza: tiene el archivo y el test ocupando el resto |

**Y lo que es PROPIO de cada una, para que nadie fuerce una simetría falsa:** de `brd-business-analyst` son los montones de quién resuelve un hueco de negocio, la prueba que legisla y las cifras huérfanas —porque solo ella escribe reglas de negocio—; de `crea-suite` son la orquestación de subagentes, los niveles y las puertas.

🔴 **CONTRA-INDICACIÓN — la regla que decide cuándo NO agregar texto a esta skill.** Antes de escribir aquí un principio nuevo se comprueba si el defecto **ya tenía su regla escrita**. **Si la tenía y ocurrió igual, la medicina NO es repetirla: es un CONTROL que la verifique.** ⚠️ **Caso medido (04-09-2026): el *«sujeto tácito ambiguo»* estaba en el principio 14 desde semanas antes, y el documento tenía siete elementos con ese defecto. Escribirlo por segunda vez no habría cambiado nada; lo cambió un script de veinte líneas que los nombra uno por uno.** **Una skill es la MEMORIA del método; un control es lo que OBLIGA.** Confundirlos infla la skill y la vuelve menos leída — que es el modo de falla que la documentación oficial le atribuye a un archivo de instrucciones largo.

⚠️ **Cuando se toque un principio de la tabla de arriba, se abre la otra skill en el mismo turno.** No hay mecanismo automático —son dos repositorios— y **esta lista es el mecanismo**: hace visible lo que hay que revisar.

---

## §9 · etiquetas

🔴 **Estas dos se declaran aquí porque la skill las usaba sin definirlas: en un BRD real había 219 y
`[NO EXIGIBLE]` aparecía UNA VEZ en toda la skill, como anécdota.** Una etiqueta sin definición no
tiene dueño ni condición de cierre — y por eso 206 de esas 219 no decían quién podía resolverlas.
⚠️ **Y ninguna de las dos bloquea el cierre a propósito**, igual que `[RIESGO]`: lo que bloquea es
`[DUDA]`. **Pero las dos se CUENTAN y se reparten por quién resuelve** — ver §13.

---

---

## §10 · reglas de negocio (exigencias)

🔴 **DOS EXIGENCIAS MÁS, y las dos se verifican mirando la propia fila:**
  **(a) QUIÉN ACTÚA, ESCRITO.** Nada de *«se valida»*, *«se acredita»*, *«queda
  registrada»* cuando hay más de un actor posible. En un sistema con varios agentes,
  **todo verbo en tercera persona sin sujeto es ambiguo — y quien va a programar no
  deduce: elige en silencio, y la elección barata gana.**
  **(b) LA REGLA CARGA SUS PROPIAS GUARDAS.** Los límites de una regla van EN LA REGLA,
  nunca solo en sus criterios: **el criterio PRUEBA, no almacena.** 🔴 **Caso medido
  (04-09-2026): la única regla que autorizaba mover material de una cuenta a OTRA
  —competidoras del mismo rubro— eran tres líneas sin una sola guarda; las guardas
  existían, en dos criterios de §15. Leída sola —que es como la lee quien codifica—
  copiaba los precios y el catálogo de un cliente al set de pruebas de su competidor.**

🔴 **LOS TRES CAMPOS DEL MEDIO NO SON ADORNO: SON LO QUE §11 VA A EXIGIR, ADELANTADO AL MOMENTO DE
ESCRIBIR.** Se escriben AL NACER la regla, no al revisarla. **Evidencia de por qué (03-09-2026):** en
un BRD real, medido con esos mismos ejes, **solo el 22% de las reglas estaba listo para codificarse**
—39% tenía prueba pero no decía contra QUÉ dato comparar— y la causa no era que los controles
fallaran: **la skill dedicaba el 45% de su texto a auditar un elemento y 82 caracteres a escribirlo.**
El elemento nacía con tres campos y se juzgaba con quince obligaciones que no tenían dónde escribirse.

⚠️ **Cómo se llena cada uno, y por qué en ese orden:**
- **VERIFICA** es la vara del §11 punto 7 traída aquí: **no «¿cómo sabríamos?» —que acepta un juicio—
  sino «¿con qué REGISTRO o EVENTO se responde sí o no?»**. Si la respuesta es *«leyendo la
  conversación»*, la conducta es **salida (b)** y se declara así, con la consecuencia que eso trae:
  **ninguna consecuencia dura puede colgar de ella**.
- **DATO** es contra qué compara el código en ejecución. Si no hay ninguno, o falta el elemento de §6
  que lo declare, **eso es un hueco de la sección de datos y se abre ahí** — no se deja implícito.
- **FUENTE** aplica a **todo número con unidad**: días, %, dinero, mensajes, intentos. Sin ella, quien
  codifique no sabe si el número es ley, estándar, deseo o error de copia.

---

## §10 · datos (DA-EST)

🔴 **La cuarta familia existe porque su ausencia tuvo costo medido (03-09-2026): un BRD real describía
lo que el sistema HACE y casi nada de lo que GUARDA, y al escribir el esquema de base de datos
salieron 22 de 69 entidades sin respaldo aquí — entre ellas la conversación, LA UNIDAD DE COBRO y las
trazas.** Entrada, salida y consumidor describen el TRÁNSITO del dato; ninguna describe el objeto que
queda. **Y quien construye no puede inventarlo sin decidir en silencio de quién es cada fila.**

⚠️ **Todo `[DA-EST-XXX]` declara su dueño: qué lo separa de los datos de otra cuenta.** Es la línea que
después se vuelve esquema, y equivocarla no se corrige: se rehace.

---

## §10 · criterios de éxito (dato)

🔴 **La casilla del DATO es obligatoria y nace del defecto medido: en un BRD aprobado,
  las 18 métricas —incluidas dos comprometidas por contrato— no decían con qué dato se
  calculaban, y de DOS el dato no existía en §6.** Una métrica sin su dato no es una
  meta: es un deseo. ⚠️ **Y si el dato no existe, NO se inventa la métrica: se crea el
  dato en §6 o la métrica se declara no calculable todavía, con lo que le falta.**

---

## §10 · pendientes (QUIÉN RESUELVE / CIERRA CUANDO)

🔴 **Los dos campos nuevos nacen de una cifra: en un BRD real había 219 marcas abiertas y 206 no
decían quién podía resolverlas.** Sin «quién resuelve», toda marca termina en el usuario —y de siete
que se le presentaron, **cinco no eran suyas**—. Sin «cierra cuando», una marca que espera medición y
otra que espera una decisión **se leen igual**, y ninguna se cierra.

---

## §10 · criterios de aceptación (PR y salida b)

🔴 **`PR-XXX` está en la lista porque su ausencia ya costó: la cláusula de cobertura del §11 punto 8
solo nombraba `[RN]` y `[CB]`, y por ese punto ciego los procesos Must llegaron aprobados sin un solo
criterio SIENDO CONFORMES con la regla escrita. Se arregló la cláusula que audita y no la plantilla
que escribe** — el mismo defecto que esta skill denuncia entre documentos, cometido dentro de sí.
⚠️ **Y la marca de salida (b) existe porque unos 22 criterios de tono y cortesía se contaban como
cobertura dura: legítimos como criterio, falsos como cobertura.**

---

## §11 · revisión de consistencia (puntos 1 a 12)

1. Contradicciones entre [RN-XXX] solapados o contradictorios. **La clase que
   mejor se esconde: la negación global.** Un elemento que niega en general
   ("no hay X fuera de Y") es una afirmación falsable por cualquier elemento
   posterior que establezca X por otra vía — y sobrevive porque los dos pueden
   nombrar X con PALABRAS DISTINTAS, así que ni la relectura ni el cotejo de
   vocabulario idéntico la cazan. Caso registrado: "no hay notificación fuera
   de la consola" convivió `[CONFIRMADO]` con "el aviso sale por el canal que
   la cuenta eligió", también `[CONFIRMADO]`, y de las dos lecturas salían dos
   productos; se descubrió recién al redactar un criterio que necesitaba
   apoyarse en ambos. Dos defensas que se complementan: el foco de exclusiones
   de `salud-brd.py` lista los candidatos mecánicos, y **redactar CA es la otra
   mitad del control** — escribir el criterio obliga a leer juntos los
   elementos que verifica, y ahí es donde las contradicciones aparecen:
   registrarlas al verlas, no seguir de largo.
   **Y la segunda clase que se esconde: la respuesta capturada por la entidad
   dominante.** Cuando el documento declara una taxonomía de N entidades de una
   clase (agentes, módulos, canales), toda regla «de sistema» tiende a
   escribirse solo para la entidad más nombrada — la gravedad del corpus lo
   empuja. Caso medido (28-08-2026): la entidad principal con **580 menciones
   contra 13/8/2** de sus hermanas; el dueño corrigió TRES veces en un día la
   respuesta por-una-entidad —capas, señales, saturación— y las tres veces la
   entidad dominante escondía hoyos reales en las otras. Dos defensas: **toda
   pregunta o regla de sistema se responde POR CADA entidad de la taxonomía
   antes de darse por cerrada**; y contra el goteo de piezas faltantes, **la
   FICHA: una plantilla de campos obligatorios por instancia** (definición ·
   herramientas · guardas · registro · pruebas · ciclo de vida · conducta de
   saturación) **auditada de una vez contra todas las instancias** — el goteo
   se acaba cuando ya no queda dónde gotear.
   **Y la disciplina del hallazgo del propio auditor, porque dos veces en un
   día (28-08) el cazado fue el analista y quien lo cazó fue el dueño:** un
   hallazgo de AUSENCIA (*«el documento no lo dice»*) solo se reporta tras
   búsqueda EXHAUSTIVA — sin límite de resultados y con sinónimos: un *«no
   existe»* se concluyó sobre una lista truncada a 15 resultados y la regla
   estaba pasado el corte. Y un hallazgo de CONTRADICCIÓN exige confirmar que
   ambos textos hablan de LA MISMA entidad — el patrón dos-nombres también
   fabrica contradicciones FANTASMA: dos entidades distintas fusionadas por el
   analista bajo un nombre produjeron una contradicción que no existía. Ambas
   comprobaciones existen para que el dueño no tenga que ser el último control.
2. [SA-XXX] que contradiga [RN-XXX] confirmado.
3. TODOS los ítems sin lenguaje vago: subjetivos ("fácil de usar", "amigable"),
   loopholes ("si es posible", "según corresponda"), comparativos sin referencia,
   pronombres ambiguos, términos abiertos ("entre otros"), absolutos ("siempre",
   "nunca", "todo") y **alcance ambiguo de una enumeración**: un modificador
   detrás de una lista cuyo dominio sobre los ítems no está claro. Con la forma
   "el cliente elige A, B y C **desde la lista cerrada de C**", ¿salen los tres
   de la lista o solo el tercero? Caso registrado: una regla así estuvo
   `[CONFIRMADO]` y Must durante meses admitiendo las dos lecturas —de cada una
   salía un producto distinto— y ninguna de las otras clases de esta lista la
   detecta. Un ítem = UNA sola regla:
   dividir los compuestos con "y/o". **La regla compuesta que sobrevive cobra
   dos veces:** caso registrado — una regla Must con TRES conductas tenía UNA
   sola prueba (el CA cubría dos y la tercera quedó sin criterio que obligara
   a leerla) y una sola marca de pendientes que contaba los valores de dos.
   La conducta sin prueba y sin marca fue invisible para todos los filtros
   hasta que una herramienta cruzó las señales. Los candidatos mecánicos a
   este punto los lista `salud-brd.py` foco [4]: regla larga con prueba única.
   **Y una clase más, que se detecta con el usuario y no leyendo: la palabra que
   significa dos cosas.** Cuando el usuario usa un término distinto del que el
   documento usa para lo mismo —o el mismo término para dos cosas distintas—, **eso
   no es un descuido suyo: es la prueba de que el documento admite las dos
   lecturas**. Se escribe una nota de vocabulario que distinga los ejes, y se revisa
   qué elementos quedaron redactados con la palabra equivocada. Caso registrado: el
   dueño llamó "roles" a lo que el documento llamaba "categorías"; el documento
   distinguía categoría de *nivel* desde hacía versiones pero **nunca categoría de
   *rol***, y esa ambigüedad ya había producido una regla que hacía a un rol dueño de
   un guion, contradiciendo a la que decía que la dueña es una persona.
   ⚠️ **Y su variante silenciosa, que ese disparador NO caza: el término usado
   BIEN y nunca declarado.** El caso anterior se detecta porque el usuario emplea
   otra palabra; este no emite ninguna señal — el documento usa el término de forma
   consistente en más de cien apariciones y aun así **cada lector nuevo tiene que
   inferir a cuál de las entidades de la cadena designa**. La consistencia no
   sustituye a la declaración: quien lee no tiene manera de saber que es
   consistente. **Contra quién se mide la ambigüedad, y este es el criterio que
   decide:** no contra el lector humano —que repregunta y lo resuelve en un turno—
   sino contra **el lector que no puede repreguntar**, el que toma el documento para
   construir. Ahí la lectura se elige en silencio y queda escrita en el código: la
   misma frase que cuesta una pregunta en la sala cuesta un defecto en el
   repositorio. **Por eso la nota de vocabulario declara también la cardinalidad de
   cada eslabón** (1:1, 1:n): esa línea es la que después se vuelve esquema de
   datos, y el usuario suele dictarla entera sin saber que está dictando un modelo.
   Caso registrado: el dueño dibujó la cadena a mano en una sola frase —*"yo tengo
   uno, y el mío tiene muchos"*— recién después de que dos documentos consecutivos
   la dieran por obvia, y la misma ambigüedad volvió a costar una pregunta al día
   siguiente.
4. [BN-XXX] con evidencia documentada y al menos una alternativa.
5. [PE-XXX] que bloqueen decisiones de fases posteriores.
6. Respuestas "no sé" sin activar §7.
7. Todo [RN]/[PR]/[RE] es comprobable — **y la vara NO es *«¿cómo sabríamos que se
   cumple?»*, que acepta un juicio como respuesta** (*«leyendo la conversación se
   ve»*), **sino: «¿con qué REGISTRO o EVENTO se responde sí/no?»**. El que
   construye no puede mirar una conversación y opinar; puede mirar un registro.
   🔴 **Caso registrado (26-08-2026): una cacería con este lente sobre un BRD
   APROBADO** — todos los filtros de lectura en verde, 1.157 elementos — **encontró
   92 frases no programables** (*hostilidad, negativa explícita, «pide hablar con
   una persona», «señales de duda», «contenido anómalo»*), que pasaban la pregunta
   débil; **33 tenían consecuencia dura colgando de un juicio del modelo**.
   **El usuario habla en su idioma y ese es SU rol; operacionalizar es de esta
   skill:** sus palabras quedan `[CONFIRMADO]` tal cual, y la skill agrega el
   ancla — el registro, el evento, la lista cerrada o el número — o la marca que
   declara su ausencia. **Toda conducta cuya condición solo el modelo puede leer
   se resuelve en UNA de tres salidas, en el momento de escribirla: (a)** colgarla
   de una **ACCIÓN REGISTRADA** — lo que el agente HIZO, no lo que el mensaje
   ERA — (el precedente: un cobro que dependía de «hostilidad» se movió al cierre
   registrado que la hostilidad produce); **(b)** declararla **«solo pedible al
   modelo»** — vive en el prompt y **NINGUNA consecuencia dura** (cobro, bloqueo,
   cierre, escalamiento obligatorio) **puede colgar de ella**; **(c)** crear el
   **evento registrable** como dato de §6. Si no se puede elegir salida, no falta
   redacción: **falta una decisión de negocio, y se pregunta**. Si aun así queda
   sin ancla, marcar [DUDA].
8. Cobertura: toda [RN], todo [PR] (incluidos [PR-ALT]/[PR-EXC]) y todo [CB] tienen
   al menos un [CA] que los cubre; todo [RN]/[PR] contribuye a algún [OB] o [CE] (el
   huérfano se elimina o se justifica). **Los procesos TAMBIÉN exigen criterio:** la
   versión anterior de esta regla solo nombraba [RN] y [CB], y por ese punto ciego
   los procesos Must llegaron aprobados sin un solo [CA] **siendo CONFORMES con la
   regla escrita** — el hueco no era negligencia contra la ley: ERA la ley. También
   explica una asimetría que se repite al medir: los casos borde salen muy por
   encima de los procesos, porque solo ellos estaban en la cláusula.
9. **La regla 8 se MIDE, no se estima leyendo.** Evidencia del dolor: un BRD
   aprobado, con varios filtros de auditoría pasados, tenía **el flujo principal
   completo sin UN SOLO [CA]**, casi un tercio de sus elementos inertes (nadie los
   citaba y ningún CA los verificaba) y reglas de más de mil caracteres — los
   filtros eran de lectura y la enfermedad era estructural. El estudio mecánico
   mide: (a) cobertura de CA por familia — **el camino feliz primero**: los casos
   borde suelen quedar mejor cubiertos que el flujo central, porque lo central "se
   da por obvio"; todo elemento prioridad M sin CA se lista y se cubre o se acepta
   por escrito; (b) elementos inertes; (c) longitud — un ítem sobre ~400 caracteres
   suele ser varias reglas juntas: partir conservando el ID original con el núcleo
   para no romper citas; (d) hubs no confirmados — un ítem [INVESTIGADO]/[SUPUESTO]
   citado por 3+ es riesgo estructural: si cambia, arrastra; (e) cada ola de reglas
   nuevas entra CON sus CA — si crecen las reglas y no los criterios, la cobertura
   se degrada en silencio (evidencia: una sola versión metió decenas de elementos
   normativos con un puñado de CA; la deuda nació en la captura, no en la
   revisión); (f) cuando el medidor
   encuentra N casos de una clase, la corrección se dimensiona con la LISTA COMPLETA
   del medidor, nunca con los casos que motivaron la alerta — modo de falla
   registrado: un saneamiento cerró los primeros procesos de la lista y declaró
   victoria mientras quedaban decenas de elementos Must sin criterio; se cierra la
   query, no el síntoma; (g) **la cifra de cobertura mezcla DOS enfermedades
   distintas: falta el CRITERIO o falta la CONDUCTA.** Si para escribir el CA hay
   que inventar qué hace el sistema, no falta el criterio — falta la regla: es un
   hueco de negocio con disfraz de deuda técnica, y se deriva de las reglas
   vigentes (entrando [SUPUESTO] con el contraste del Principio 12) o se enruta
   como decisión — nunca se tapa con un CA, que se leería como cobertura real.
   Evidencia: de siete casos borde sin CA, cuatro se cubrieron citando conducta
   ya escrita y tres no tenían conducta que citar; (h) **una marca de
   no-exigibilidad acota LO QUE NOMBRA, no el elemento entero**: lo demás del
   elemento se verifica hoy. Evidencia: tres reglas con marca llevaban versiones
   sin CA teniendo la conducta principal perfectamente verificable — la marca
   cubría un detalle (una lista por declarar, el lugar donde vive un dato) y se
   leyó como bloqueo total; (i) **la marca se re-deriva contra la regla ENTERA
   cada vez que la regla crece**: la marca escrita durante una ampliación tiende
   a contar solo los pendientes de la ola que la amplió. Evidencia: una regla
   amplió sus límites con dos valores nuevos y su marca quedó diciendo "los dos
   números exactos" — la tercera magnitud, que ya vivía en la regla, quedó fuera
   de la marca, fuera de la lista de calibración y fuera de toda lectura.
10. 🔴 **La prueba que legisla.** Un `[CA]` VERIFICA lo que una regla dice; **nunca
    introduce una decisión que ninguna regla enuncia** — una métrica, un modo, un aviso,
    un cobro. Cuando el «entonces» de un criterio no se puede rastrear al texto de una
    regla, hay dos salidas y ninguna es dejarlo: **la decisión sube a una regla** (con su
    dueño y su contraste) **o el criterio se recorta**. Caso registrado (01/02-09-2026):
    barridos los 588 criterios de un BRD aprobado, 10 legislaban; uno mandaba una
    advertencia que **contradecía a la propia regla que decía verificar** (la regla
    declaraba esa función como ajena al proveedor); otro guardaba **la diferencia
    comercial del producto solo en una prueba** — y una diferencia comercial que vive en
    un test no la ve ningún comprador ni ningún panel. Para quien construye, un criterio
    es una obligación igual que una regla: **si legisla, legisla en silencio y sin dueño.**
11. 🔴 **Cifras huérfanas.** Toda regla viva que lleve un **número con unidad** —días,
    horas, %, dinero, mensajes, intentos— declara de dónde salió, con UNA de cuatro
    marcas: cita a la investigación (`INV-XXX`) · palabras del dueño · `[A CALIBRAR]` ·
    heredada de una regla que cita. Un número sin marca lo va a programar alguien **tal
    cual**, y nadie sabe si es ley, estándar, deseo o error de copia. **Y la cifra LEGAL se
    verifica contra el TEXTO OFICIAL de la norma y cita el artículo — nunca contra un
    resumen, y nunca heredada de otra jurisdicción.** Caso registrado (02-09-2026): de
    125 reglas con cifra, 5 huérfanas; **la de la ley de datos tenía dos de tres plazos
    falsos** — decía «días hábiles» donde la ley dice «corridos», y traía un plazo de «72
    horas» **que la ley chilena no contiene: era el del reglamento europeo, copiado**. Las
    dos cifras falsas estaban repetidas en once documentos derivados. Los criterios
    (`CA-`) quedan fuera del barrido: ahí un número es dato de escenario, no regla.
    🔴 **Y el CONTEO que una regla declara sobre una lista que vive en otro documento se recuenta
    sobre las filas de esa lista, con instrumento, en cada versión que la toque** *(13-09-2026: la
    regla madre de las barreras traía 313 · 169/49/45 desde veinte versiones atrás cuando las filas
    daban 317 · 192/58/51; el total se corrigió una vez copiando una cabecera que también venía
    desviada — copiar no es recontar)*. La skill hermana lo mide del lado del derivado (§5 punto 10).
12. **Las coordenadas del mapa: identificador único · sintaxis · familia · taxonomía.**
    Son cuatro planos distintos y se auditan aparte: ID repetido o hueco sin mecanismo;
    ID mal formado; elemento que vive en la familia equivocada (una restricción escrita
    como regla, un pendiente escrito como riesgo); y elemento cuya sección no coincide con
    su prefijo. **Un elemento en la familia equivocada NO se renumera: se deroga y renace
    con ID nuevo en su familia** —las citas al viejo siguen existiendo—. Lo mecánico lo
    caza `mapa-brd.py` (crea-suite); lo semántico se lee.

---

## §11 · criterios de cierre (EARS)

- Criterios de aceptación verificables, **separando el EVENTO del ESTADO**: `CUANDO` un evento ocurre · `SI` un estado se cumple · `MIENTRAS` algo dura · `DONDE` rige un contexto, y la respuesta siempre en `DEBERA`. *(Es la sintaxis EARS, que Amazon Kiro adoptó como estándar de sus specs **porque una máquina la puede leer**; ver `braingrid.ai/blog/ears-notation`.)* 🔴 **`Dado/Cuando/Entonces` NO basta y por eso se cambió el 09-09-2026: su «cuando» tapa evento y estado en la misma palabra, y esa es justo la distinción que un control no puede comprobar en prosa** — un criterio que dice *«cuando el agente detecta hostilidad»* no deja ver si espera un hecho registrado o un juicio del modelo, que es el defecto que este método ya midió cinco veces y las cinco costaban plata o exposición legal.

---

## §11 · cambios posteriores a la aprobación (C4)

### Cambios posteriores a la aprobación (C4)

Todo cambio al BRD después de C4: (1) incrementa la versión del encabezado; (2) agrega
fila en §19 con los IDs afectados; (3) avisa que crea-suite debe invalidar y
re-verificar SOLO los pasos que dependen de esos IDs — nunca regenerar la suite entera.

**Los ID los asigna quien escribe en el BRD, y no se reutilizan.** Reservarlos desde
fuera —una nota, un enrutador de correcciones, un borrador— es asignar a ciegas: solo
el propio documento muestra cuál es el último ocupado. Y un ID cerrado o derogado
conserva su fila: se marca, no se borra ni se recicla, porque las citas que lo nombran
siguen existiendo. Evidencia de las dos mitades: un pendiente se numeró sobre uno ya
cerrado, y en otra pasada varios ID propuestos desde un documento externo dieron ROJO
en `docs-check` por citar definiciones que aún no existían.

**(4) El aviso no basta: el mismo turno cierra la cascada de desactualización.** Correr
`tools/docs-fresh.py` y resolver cada línea de *Herencia fina* antes de dar el cambio por
hecho. El BRD es el mandante: cuando cambia, no se desactualiza el documento entero de
cada heredero, **se desactualiza la parte que cita lo que cambió** — y eso se computa por
ID, cruzando la columna de §19 contra las citas de cada documento.

Por qué está escrito así, con evidencia: la versión anterior de esta cláusula terminaba en
"avisa". Un aviso solo llega si esta skill está corriendo, y solo alcanza a los **pasos**
de la cascada. Caso registrado: un BRD avanzó ocho versiones en un solo día, el aviso se
dio, el documento heredero se re-corrió — y quedaron **decenas de contradicciones vivas
repartidas en casi veinte documentos**, porque la mayoría no eran pasos y nadie los
miraba. Algunas estaban dentro del propio BRD: un criterio de aceptación seguía
condicionado a una excepción que la regla verificada había eliminado cuatro versiones
antes.

**Corolario para este mismo archivo:** cuando una regla del BRD cambia, barrer también los
**criterios de aceptación y las notas** que la citan. Un `CA` que verifica el mundo
anterior no rompe ningún verificador de IDs y se lee como vigente.

🔴 **(4-bis) Y el barrido va en las DOS DIRECCIONES, no en una. Esto se agrega el
29-08-2026 porque la cláusula anterior miraba solo una y el caso se escapó por la otra.**
El corolario de arriba cubre **quién CITA al elemento que cambió**. Falta la dirección
contraria: **a quién CITA el elemento NUEVO.** Un elemento nuevo suele nombrar a los
viejos como respaldo —*«la doctrina ya existía: `RN-169`, `PR-075`»*— y **al mismo tiempo
deroga una de sus cláusulas sin decirlo**; el citado queda vivo, diciendo lo de antes.

**Evidencia, del propio proyecto:** `RN-351` nació citando a `RN-169` como respaldo y
declarando que **en voz la consulta es SIEMPRE DIFERIDA**, mientras `RN-169` seguía
ofreciendo una rama *«en línea, donde el lead ESPERA»*. **Ni siquiera era el caso «dos
reglas que no se citan» que el cazador asume: SE CITABAN.** La premisa muerta además
había bajado a `AL-029`, que hoy tiene una cola llamada *«un lead esperando en línea»*.
Lo detectó el dueño preguntando, no una herramienta — y su reacción fue la correcta:
*«¿hay mecanismo para que estas reglas obsoletas desaparezcan cuando aparece otra que las
reemplaza?»*.

**Cómo se ejecuta, y ya no depende de acordarse:**

```bash
python tools/cazador-obsoletos.py --relectura
```

Imprime, para los IDs que la fila de **§19** declara tocados, las dos listas: **(b) a
quién citan** —la que ninguna otra herramienta nombra— y **(a) quién los cita**. Con
`--relectura <version>` se revisa una versión anterior. ⚠️ **Nombra, no compara
significados: leerlos sigue siendo trabajo humano**, y la corrida debe declarar que lo
hizo, igual que la estampa *«leídas las partes que el control nombró»* hace con los
documentos derivados. **Medido sobre la v4.08 del proyecto que lo originó, la lista (b)
contenía los tres defectos que la cacería con agente confirmó después** (`RN-351`→`RN-169`,
`RN-352`→`RN-199`, y `CA-453` contra el predicado nuevo de `RN-319`).


**(5) Correr `tools/cazador-obsoletos.py`, porque la cascada por cita tiene un punto
ciego estructural.** `docs-fresh` computa la herencia **por ID citado** — su propio código
lo dice: *«solo mira los IDs que este doc ya cita»*. **Dos elementos que se contradicen sin
citarse son invisibles para él, por diseño**, y esa es justo la forma que toma el defecto
cuando una decisión nueva no baja a la regla que la heredaba.

Evidencia del caso que lo motiva: una regla se corrigió con la decisión del dueño, se
escribió su fila de §19… y **el criterio no se bajó al texto de la regla que la heredaba**,
que quedó diciendo lo del día anterior. El documento afirmaba dos cosas incompatibles y
quien codificara elegiría una en silencio. Lo detectó **el dueño preguntando**, no una
herramienta. Un barrido posterior encontró **24 casos más en 1.155 elementos**, y **18 de
los 24 eran el mismo patrón: el barrido se detuvo un nivel antes**. Los criterios de
aceptación fueron el nivel más olvidado (9 de 24) y las marcas `[NO EXIGIBLE]` el segundo.

**El reparto del trabajo, y hay que respetarlo o se cree cubierto lo que no lo está:**

- **Lo mecánico lo caza el script**, en segundos y sin falsos positivos medidos: titular
  con numeral contra su enumeración interna, citas a IDs derogados o fuera de alcance
  usadas como vigentes, y conteos citados (*«las seis funciones de X»*) cruzados contra lo
  que X enumera. Cubrió 3 de los 24 de aquella corrida.
- **Lo semántico necesita leer.** Las contradicciones entre dos elementos que no se citan
  **ninguna herramienta las ve**: eso exige un agente que recorra el documento entero. El
  script no lo suple y lo declara en su propia cabecera.

**El aviso periódico es parte del protocolo, no una sugerencia.** El script sella la
versión de la última cacería profunda (`--sellar`) y **avisa cuando han pasado 8 versiones
sin una nueva**. Al ver ese aviso, esta skill **lo dice en el mensaje de cierre** y ofrece
lanzarla; no la ejecuta por su cuenta. El umbral se ajusta con `--avisar-cada`.

⚠️ **La línea base no es para silenciar.** `--sellar` marca como *conocidos* los hallazgos
**que ya tienen fila en el enrutador de correcciones**, para que el reporte muestre lo
nuevo en vez de repetir deuda enrutada. **Sellar algo que no está enrutado lo desaparece**,
y es la única forma de que este control mienta.

**(6) Lo que dejó de regir SALE del documento vivo — y toda idea nueva se contrasta
contra lo que ya se descartó.** Un documento que crece acumula lo que rige JUNTO a lo que
dejó de regir —elementos derogados, notas *«hasta la vX decía…»*, estampas viejas— y quien
lee de corrido se queda con lo último, no con lo vigente; **y paga por leerlo**: en un caso
medido, casi un quinto del documento era historia. Regla: **el BRD guarda lo que rige;
`docs/BRD-evidencia.md` guarda el porqué (§18); `docs/BRD-historial.md` guarda lo que dejó
de regir.** Los tres comparten el espacio de IDs —un ID derogado conserva su fila en el
historial— y `docs-check` los lee a los tres como fuente de definición, de modo que mudar
la historia no rompe ninguna cita. La estampa de un derivado dice solo la versión. **Y el
historial no es un archivo muerto: antes de proponer, se consulta** (`tools/historia.py
<ID>` · `--buscar TEXTO`) — el dueño lo pidió con estas palabras: *«para que no lo vuelvas
a proponer, cada idea debería contrastarse con ese documento»*. Una propuesta que ya se
descartó y vuelve sin decir por qué esta vez sí le cuesta al dueño la misma conversación
dos veces.

---

## Anti-patrón 23

| 23 | Recuperar una decisión de una sesión antigua y etiquetarla `[CONFIRMADO]` sin verificar QUIÉN dijo cada cifra. Lo que el asistente propuso y el usuario no respondió es `[SUPUESTO]`, nunca "textual" — una cifra lavada como cita entra con la autoridad de una cita, y una cita no se re-verifica. Evidencia: un cobro único entró como parte de "lo acordado, textual" siendo una propuesta del asistente construida sobre el plan de un competidor que el usuario había pegado como referencia; vivió `[CONFIRMADO]` hasta que el usuario lo desautorizó, y la verificación forense de la sesión original le dio la razón. |

---

## §12 · cómo se cuentan las cifras

**Cómo se cuentan esas cifras, porque es contraintuitivo:** salen de las **filas de
elementos de §1 a §15**, nunca de contar ocurrencias de la etiqueta en el archivo. El
§16 reexpone cada elemento y el §19 los nombra otra vez, así que un conteo por etiqueta
los suma dos y tres veces. Evidencia: un cierre reportó más del doble de supuestos y de
pendientes de los que había — el usuario preguntó qué significaban esos números y no
había forma de sostenerlos. Un cuadro de cierre con
cifras infladas es peor que uno sin cifras: se lee como medición.

---

---


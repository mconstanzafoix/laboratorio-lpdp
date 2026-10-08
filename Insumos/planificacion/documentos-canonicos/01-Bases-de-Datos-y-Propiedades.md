# 01 — Bases de datos y tablas de propiedades

**Estado:** contenido previo visado por MCF; ajustes solicitados el 01-10-2026 incorporados para revisión, sin atribuirles un visado posterior. **Última revisión:** 01-10-2026. El historial anterior vive en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/`. *(El 30-09-2026 este paquete se trasladó a `Laboratorio LPDP/Insumos/planificacion/documentos-canonicos/`.)*
**Fecha:** 25-09-2026
**Quién usa este documento:** es la referencia canónica del esquema **para personas y para el Agente de Arquitectura**. **Los agentes operativos NO lo cargan**: cada `PROMPT.md` de la carpeta de agentes contiene exactamente los campos que ese agente lee o escribe, y nada más. Así se evita el context rot y que un cambio de esquema se propague suelto: cambia aquí → el Agente de Arquitectura actualiza los prompts afectados → visado → recién entonces se despacha (ver `02-Gobernanza-y-Context-Engineering.md` §1 y §10).
**Regla 3.0:** lo que excede dos líneas es 🧾 contenido de página, no propiedad. La razón: una propiedad es lo que se ve en la vista de tabla sin abrir la ficha; si el criterio largo viviera en una columna, la tabla se vuelve ilegible y la columna nadie la lee. El texto largo va en el cuerpo de la página, la propiedad guarda solo lo comparable de un vistazo.
**IDs reales de las bases** (preservados; ver manifiesto-notion.json): Fuentes `56828aa7…` · Disposiciones `0a74b01a…` · Exigencias `930efc14…` · Dominios `73bc3ace…` · Agrupaciones `9383055f…` · Ítems `6f4c5ed1…` · Subítems `6f8138c8…` · Escaladas `b6a6cad3…` · Formas `a0eb0f91…` · Bitácora `be8ae32a…`. (El ID histórico de la base Prompts, `04feb604…`, queda registrado aquí como antecedente tras su eliminación el 25-09-2026.)
**Ubicación propuesta:** Administración → Bases maestras; las páginas de uso contienen vistas enlazadas, sin copias.

---

## ① Fuentes

Un cuerpo normativo **con su versión determinada**.

| Propiedad | Tipo | Valores / nota |
|---|---|---|
| Nombre | Título | |
| Tipo de fuente | Select | Ley / Reglamento / Jurisprudencia / Acto administrativo / Norma técnica / Doctrina / Comparada |
| Nivel de autoridad | Select | Vinculante nacional / Reglamentaria / Interpretativa / Doctrinal / Comparada no vinculante / **Sin calificar** |
| Fundamento del nivel | Texto | |
| Nivel visado | Checkbox | **decisión humana** |
| Visado por | Person | |
| Jurisdicción | Select | 12 opciones |
| Fecha de publicación | Date | |
| Estado de vigencia | Select | Vigente / Vigente con vacancia / Derogada / Proyecto |
| Enlace oficial | URL | |
| Acceso al texto | Select | Repositorio oficial / Mirror oficial / Documento cargado / Bloqueado—pendiente |
| Nota de acceso | Texto | protocolo de mirrors oficiales si aplica |
| Etapa del ciclo | Select | 8 etapas: Ingresada → En fragmentación → Fragmentada → En destilación → Destilada → En auditoría → Auditoría completada → Lista para uso en Dominio |
| Vía de ingreso | Select | Vigilancia normativa / Agente investigador / Carga humana / Documento en chat |
| Quién la incorporó | Person | |
| Qué la originó | Texto | |
| Alcance delimitado | 🧾 página | |
| Disposiciones | Relación → ② | |
| Dominios afectados | Relación → ⑤ | |
| Chat de trabajo | URL | |
| Revisión del corpus | Date | |
| Última conciliación | Date | |

🧾 Contenido de página: **inventario de cobertura** (toggle `Inventario de cobertura`): tabla acumulativa por Fuente, cinco columnas — **Unidad esperada | Fragmentación | Destilación | Auditoría | Detalle y evidencia** — cada una `Pendiente / Parcial / Completa`, una fila por artículo/unidad, construida desde el primario.

## ② Disposiciones

La unidad normativa con texto literal conservado. Clave de identidad: cuerpo normativo + versión + identificador de la unidad declarado en `ARBOL.md`; la ruta apunta al archivo que la materializa.

| Propiedad | Tipo | Valores / nota |
|---|---|---|
| Identificador | Título | Identificador jurídico completo de la unidad, preservando su estructura real: artículo ordinario o intercalado, transitorio, inciso, numeral, subnumeral, letra, fragmento, instrucción modificatoria o artículo reproducido, según corresponda. Ver regla de identidad bajo la tabla. |
| Fuente | Relación → ① | |
| Texto literal | 🧾 bloque sincronizado | **vive una sola vez, aquí**; espejos en Exigencias/Agrupaciones/Ítems |
| Localización y versión | 🧾 toggle | documento, página verificable, vigencia |
| Tipo de norma | Select | lista cerrada, **exactamente un valor**: `Regulativa / Constitutiva / Declarativa / Delimitadora de aplicación / Sancionadora` — qué clase de norma es según su función en el cuerpo, con marcador expreso (minuta 7 en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/Minutas-de-decision-2026-09-29.md`). Solo las `Regulativa` regulan conducta; los principios jurídicos que regulan conducta son `Regulativa` — normas regulativas de textura abierta, no declaraciones |
| Clasificación normativa / deóntica | Select | lista cerrada, **exactamente un valor**, restringida — aplica solo si `Tipo de norma` = `Regulativa` (minuta 7): Obligación / Prohibición / Permiso / Permiso condicionado / Derecho del titular / `Sin marcador expreso` (regulativa sin marcador que respalde una clase — afirma un hecho del texto, no un fallo del agente) / `No aplica — norma no regulativa` (para todo otro `Tipo de norma`). *(Los antiguos valores `Definición` y `Sanción` salen de esta lista: sus casos se clasifican `Constitutiva` y `Sancionadora` en `Tipo de norma`. La propiedad pasa de Multi-select a Select: un solo valor por Disposición; doble marcador deóntico ⇒ fragmentación atómica, nunca doble valor.)* |
| Control de ingreso | 🧾 toggle | constancia de verificación del texto literal y del localizador |
| Fecha de ingreso | Created time | |
| Nivel de autoridad heredado | Rollup → ① | |
| Remisiones | Auto-relación | |
| Exigencias derivadas / asociadas | Relación → ③ | enlaza las fichas pertinentes; la razón de ausencia vive en el resultado detallado, no en una relación vacía |
| Resultado de destilación | Select | Pendiente / Examen incompleto / Examinada con Exigencias / Examinada sin Exigencias. En el harness su asiento único es la fila de la Disposición en `Articulos/<unidad>/RESULTADO.md` del Destilador; `COBERTURA.md` resume por artículo. No se escribe en los archivos del Fragmentador. La relación vacía por sí sola no distingue «no examinada» de «examinada sin Exigencias». |
| Revisión del anclaje · Revisión examinada | campos de control de versión | |

*(25-09-2026, decisión de MCF: eliminadas las propiedades `N.º de ingreso`, `Lote` y `Clave de orden normativo` — sobrecomplejizaban el sistema sin aportar trazabilidad que no cubran el Identificador y la Fecha de ingreso. La ordenación cronológica la da `Fecha de ingreso`; la ordenación normativa, el Identificador.)*

Estructura de ficha: advertencias → callout ⚖️ `Texto literal (Bloque sincronizado)` → quote exterior → toggles `Localización y versión`, `Control de ingreso`, `Exigencias asociadas — resultado de destilación`.

**Regla de identidad y enlace entre archivos y ficha:** una ruta de archivo es un puntero técnico, no el identificador jurídico. El Fragmentador declara en `ARBOL.md` cada unidad y su ruta; en el frontmatter de la Disposición conserva su `identificador`. El Destilador lee ambos y comprueba que correspondan al mismo cuerpo y versión. La pareja identificador + ruta permite detectar una renombración o un cruce erróneo sin reconstruir el identificador a partir del nombre del archivo. Una carpeta o `articulo.md` que sea solo índice estructural, sin `## Texto literal (bloque espejo)` propio, no constituye Disposición; una unidad madre con texto propio sí puede constituirla aunque tenga hijas.

Las abreviaturas usuales (`Art.`, `inc.`, `num.`, `lit.`, `frag.`) facilitan la lectura, pero no autorizan a forzar toda unidad al patrón numérico antiguo. Se preservan intercalados (`bis`, `ter`), transitorios, numeraciones romanas, subnumerales, instrucciones modificatorias y artículos reproducidos. La identidad completa incluye siempre cuerpo y versión; una disposición de la ley modificatoria no se confunde con la disposición resultante de la ley consolidada. Ante divergencia entre árbol, identificador y archivo, se devuelve el hallazgo al Orquestador para corrección; no se elige una versión «a ojo».

## ③ Exigencias

Lo que se concluyó que debe cumplirse. Nace `Candidata`, sin visado.

| # | Campo | Valores / nota |
|---|---|---|
| 0 | Identificador | `<fuente-y-version>/EX-018`: clave completa de la ficha; `EX-018` es el número local dentro de esa Fuente y versión |
| 1 | Enunciado | una sola regla |
| 2 | Destinatario | Responsable de datos / Encargado del tratamiento / Titular / Agencia / Delegado de protección de datos / Tercero. *(La lista cerrada y una glosa de una línea por rol — anclada a las definiciones de la Ley 21.719 y con el mapeo de términos de los cuerpos anteriores («el responsable», «responsable de la base de datos» → `Responsable de datos`) — viven en el prompt del Destilador de Exigencias, por la regla de autosuficiencia: los agentes operativos no cargan este documento. Todo prompt futuro que escriba este campo debe llevar el mismo vocabulario.)* |
| 3 | Modalidad | Obligación / Prohibición / Permiso / Permiso condicionado / Derecho del titular (una por Exigencia) |
| 4 | Conducta exigida | |
| 5 | Condición de aplicación | estructura Y/O («A O (B Y C)») |
| 6 | Plazo | Valor + Tipo de día (Corridos/Hábiles/No aplica) + Prorrogable (No/Una vez/Más de una vez/No determinado) |
| 7 | Disposición de anclaje | Relación → ②, múltiple, con función de cada una |
| 8 | Cita textual de respaldo | |
| 9 | Agrupación(es) candidata(s) | Relación → ④; legítimamente vacía en extracción; **nunca directo a Ítems** |
| 10 | Estado de determinación | Determinada / Delegada / Indeterminada; **sin valor por defecto**. Ver regla bajo la tabla. |
| 11 | Enumeración contenida | |
| — | Sanción (desglose) | Una etiqueta para filtrar vistas: `3 Gravísima / 2 Grave / 1 Leve` exigen identificar la conducta hipotética infractora, el tipo y la subsunción fundada; `0 No tipificada` exige examen negativo del régimen pertinente, incluida la cláusula residual cuando corresponda; `Calificación variable según la conducta` exige al menos dos conductas de la misma Exigencia con calificaciones distintas (`0`, `1`, `2` o `3`) ya fundamentadas en su ficha. Vacío indica examen o decisión material todavía pendiente, no pluralidad ya resuelta. El prefijo es parte del nombre de cuatro etiquetas; no permite ejecutar `Max` directamente sobre esa etiqueta. El indicador del Ítem se deriva de los grados fundados, incluidas las vías de una calificación variable. Multa máxima UTM y accesorias solo si constan. |
| — | Nivel de autoridad | Fórmula de dos saltos (Exigencia → Disposición → Fuente) |
| — | Dominio | Relación two-way → ⑤ |
| — | Estado | Candidata → Auditada → **Visada** (humana) / Descartada / Superada *(el valor inicial `Candidata` lo fija el sistema al crear la ficha; el Destilador no lo escribe)* |
| — | Carácter | Obligatoria / Condicional / Transversal |
| — | Sin agrupación | Checkbox (🟡 atención) |
| — | Relacionada con | Auto-relación |
| — | Verificada contra texto literal | Checkbox |
| — | Visada por / Fecha de visado | Person / Date — **decisión humana** |
| — | Origen del cambio de estado | Texto |
| — | Resultado de auditoría vigente | Pendiente / Verificada / Corregible / Cuestión jurídica escalada / Revisión pendiente por cambio |

**Identidad, cobertura y alcance de las relaciones.** La destilación de una Fuente y versión comienza cuando todos los artículos y unidades declaradas en su `ARBOL.md` figuran `[completo]` y los archivos existen y se abren. Las fichas de Exigencia se guardan separadas en `Resultados/<fuente-y-version>/Exigencias/`. El número local `EX-NNN` puede repetirse en otra Fuente; cualquier relación, informe, encargo o mapa que cruce Fuentes usa la clave completa `<fuente-y-version>/EX-NNN`. Cada ficha tiene al menos una Disposición principal de su Fuente y versión. **Anclaje** es la Disposición concreta cuyo texto respalda la regla o uno de sus componentes: se identifica por cuerpo, versión, identificador, localizador y archivo, y se explica su función. El anclaje principal expresa la regla en la Fuente encargada; otras Disposiciones pueden definir, limitar, exceptuar o tipificar. Una remisión externa puede figurar como contexto con función identificada, sin cambiar la Fuente de extracción; solo se registra como relación a Disposición si su ficha existe y fue comprobada. El resultado detallado de cada Disposición vive en una sola fila de `Articulos/<unidad>/RESULTADO.md`. Si un artículo extenso necesita resultados por subunidad declarada en el árbol, el resultado del artículo enlaza esos subíndices y conserva solo sus filas directas. `COBERTURA.md` tiene una fila por artículo de primer nivel con enlace y conteos únicos del artículo y sus subíndices, y conserva el último número local asignado. Así la Exigencia de la ley modificatoria y la de la ley consolidada permanecen separadas hasta que el ciclo de Dominio examine su concordancia. Una Agrupación conserva ambas relaciones y no borra ninguna ficha de origen.

**Relaciones entre artículos y reanudación.** El artículo del `ARBOL.md` es la unidad de recorrido y cobertura; la Exigencia es una regla que puede apoyarse en Disposiciones de varios artículos de esa misma Fuente. Al retomar una regla ya documentada se conserva su identificador y se concilian su ficha y las filas de `RESULTADO.md`. Durante la destilación, un artículo posterior puede completar o delimitar esa regla: se actualizan ficha y filas con la función jurídica de cada Disposición, sin crear otra Exigencia por una mera excepción ni fusionar reglas por semejanza textual. Al terminar todos los artículos se coteja transversalmente el catálogo de la Fuente; `INFORME-DESTILACION.md` concilia los resultados, sin crear un segundo catálogo. Una vez que el Orquestador cerró la destilación, un cambio material posterior se le comunica para conservar la versión anterior, revisar dependencias y encargar la corrección correspondiente.

**Informe global de destilación.** `INFORME-DESTILACION.md` es el informe técnico del productor por Fuente y versión. Se escribe después de recorrer todos sus artículos y cotejar transversalmente el resultado, antes de devolverlo al Orquestador; no se emite por artículo. Puede declarar un resultado parcial si el recorrido terminó con asuntos incompletos, y se actualiza tras una corrección y nueva comprobación. Su estructura fija presenta: resultado y alcance; método y controles con cantidades y enlaces a la evidencia; cortes y relaciones normativas relevantes; cotejos con otras Fuentes cuando se realizaron; hallazgos, límites y pendientes localizados; cierre técnico con fecha y procedencia. Se construye desde `ARBOL.md`, todas las Disposiciones y sus filas de `RESULTADO.md` —incluidas las que no produjeron Exigencia—, `COBERTURA.md` y las fichas de `Exigencias/`. Resume decisiones analíticas materiales sin reproducir el catálogo ni sustituir la auditoría independiente. Un control no realizado queda pendiente, no se convierte en «sin hallazgos».

**Desarrollo de la ficha en el harness.** El frontmatter YAML conserva únicamente los campos canónicos de la base ③. El cuerpo Markdown de cada Exigencia definitiva contiene cuatro apartados obligatorios: `Fundamento textual e interpretación` (regla, modalidad, destinatario y justificación del corte), `Alcance de la regla` (supuesto, condiciones, excepciones, remisiones, plazo, carácter y determinación), `Anclajes y función` (enlaces a las Disposiciones con Fuente, versión y papel de cada una) y `Sanción`. **Todo análisis sancionatorio** se escribe en `Sanción`, también para `0 No tipificada` y cuando `sancion` queda vacía; en este último caso, `Límites del análisis` solo resume el impedimento y remite a esa sección. Una calificación de infracción tipificada (`3 Gravísima / 2 Grave / 1 Leve`) o `Calificación variable según la conducta` exige conducta hipotética, tipo y subsunción; `0` exige examen negativo fundado. Ningún valor significa que se haya aplicado una sanción a la organización. Si hay varias vías, se describen en una tabla dentro de `Sanción`; su número no determina cuántas multas se impondrían. El método se desarrolla en `skills/calificar-sancion-exigencia/SKILL.md`, cargada en toda ejecución del Destilador y aplicada a toda ficha creada o revisada y al cotejo final de todas las fichas. El artículo reproducido y la instrucción modificatoria que lo incorpora se identifican en `Anclajes y función`; `Incorporación normativa y vigencia` se añade solo si la forma de incorporación o su vigencia exigen razonamiento adicional para esa regla. Las coincidencias comprobadas entre Fuentes se reúnen en el informe global de destilación como antecedentes del contraste posterior, sin crear una sección rutinaria en cada ficha. El `RESULTADO.md` de cada artículo conserva una fila por Disposición con cinco columnas estables: Disposición enlazada, resultado, Exigencias originadas, Exigencias apoyadas y función, motivo breve. Durante la extracción de una regla localizada, si un dato de clasificación recibido del Fragmentador impide formularla, el Destilador deja la fila en `Examen incompleto` para que el Orquestador encargue revisar el origen.

**Estado de determinación.** Una remisión es la referencia expresa a otra disposición, norma o instrumento. El estado se asigna tras examinar los textos necesarios, sin valor por defecto: `Determinada` cuando fijan los elementos esenciales de la regla, incluso si una remisión solo conduce a contenido normativo ya fijado y examinado; `Delegada` cuando el texto atribuye expresamente a otra autoridad o instrumento normativo la concreción de un elemento esencial, aunque el instrumento complementario ya exista; `Indeterminada` cuando el propio texto deja un concepto abierto que exige valoración jurídica. Una remisión indispensable cuyo texto todavía no se leyó deja la regla afectada en `Examen incompleto`: no crea un cuarto valor ni justifica escoger uno por conjetura.

**Calificación sancionatoria y pendientes localizados.** `0 No tipificada` es una conclusión negativa acotada al régimen sancionador pertinente de la Fuente y sus remisiones expresas examinadas; `Calificación variable según la conducta` es una conclusión fundada sobre calificaciones distintas (`0`, `1`, `2` o `3`) para conductas diferentes de la misma Exigencia. La ausencia de vínculo todavía no examinada o una controversia material sin resolver dejan `sancion` vacío. Todo el examen y el impedimento se conservan en `Sanción`; `Límites del análisis` lo señala sin duplicarlo y el informe global enlaza la ficha. `RESULTADO.md` registra `Examen incompleto` cuando falta un componente necesario para formular la regla, sin ficha definitiva. El Auditor comprueba estos datos con independencia; el Detector conserva todas las fichas del alcance y evalúa cada comparación con sus datos decisivos, sin excluir una ficha por un dato ajeno a esa comparación.

**Auditoría y estados técnicos.** El Auditor conserva su mapa independiente y sus veredictos con evidencia en `Auditor-de-anclaje/Resultados/<fuente-y-version>/`. `VERIFICADA` sustenta `Resultado de auditoría vigente = Verificada`; `CORREGIBLE` sustenta `Corregible`. `ESCALAR A HUMANO` es un hallazgo devuelto al Orquestador: `Cuestión jurídica escalada` se registra solo cuando este crea o vincula la Escalada. Falta de acceso o revisión inconclusa mantiene `Pendiente`; un cambio material posterior deja `Revisión pendiente por cambio` hasta la reauditoría. El Orquestador verifica el informe y aplica los estados técnicos correspondientes. `Auditoría completada` cierra el examen completo aun si conserva cuestiones con ruta pendiente; solo `Lista para uso en Dominio` acredita que todo el alcance y las fichas activas fueron comprobados sin pendientes materiales para su uso como insumo técnico. La transición y sus condiciones se registran en `Ejecuciones/`, sin crear otra propiedad. `Verificada contra texto literal` acredita solo el cotejo del literal y la versión indicados; `Estado = Auditada` y `Lista para uso en Dominio` no son `Visada` ni prueban cumplimiento de la organización o aplicabilidad a un Dominio concreto.

**Forma de cumplimiento.** Si la norma exige expresamente una forma, se conserva en `Conducta exigida`, `Condición de aplicación` y el anclaje pertinente de la Exigencia. No se infiere una forma a partir de una categoría genérica. La manifestación concreta y el criterio de cierre se definen al abrir el Subítem; el Investigador de Formas de cumplimiento aporta referentes para orientar esa decisión.

**Campos estrictos vs. semánticos:** en un campo estricto, dos respuestas distintas significan que una está mal; en uno semántico, pueden estar ambas bien. El Auditor coteja los datos estrictos y revisa también la interpretación, el corte y el alcance de la regla con evidencia y razones explícitas.

*(El fundamento de tres campos de esta tabla vive en el consolidado — `00-Sistema-LPDP.md`, tabla de Exigencias del ciclo de Fuente — y no se duplica aquí: **Plazo** (las dos velocidades del art. 11: treinta días corridos prorrogables por una vez para pronunciarse sobre la solicitud y dos días hábiles para responder al requerimiento de bloqueo; el texto literal no califica expresamente este último como «no prorrogable»), **Enumeración contenida** (dato necesario para la Regla 5 de concordancia) y **Sanción** (el texto tipificador vive en la Disposición; aquí va la calificación y el enlace). La instrucción operativa con ejemplos está en el prompt del Destilador de Exigencias.)*

### Slugs YAML canónicos (convención del harness)

Los archivos del harness (la carpeta de agentes) llevan frontmatter YAML cuyas claves deben poder exportarse a las bases **campo a campo, sin reinterpretación**. Convención: slug = nombre de la propiedad en minúsculas, sin tildes, espacios como guiones bajos. **Esta tabla es la fuente única de la equivalencia nombre ↔ slug**: cambia aquí → el Agente de Arquitectura propaga a los prompts → visado → recién entonces se despacha (proceso de promoción, `02-Gobernanza-y-Context-Engineering.md` §10). Los prompts no deben inventar claves fuera de esta lista.

**Base ② Disposiciones (escribe el Fragmentador):**

| Propiedad | Slug YAML |
|---|---|
| Identificador | `identificador` |
| Fuente | `fuente` |
| Localización y versión | `localizacion_y_version` |
| Tipo de norma | `tipo_de_norma` |
| Clasificación normativa / deóntica | `clasificacion_normativa_deontica` |
| Control de ingreso | `control_ingreso` |
| Remisiones | `remisiones` |

**Base ③ Exigencias (escribe el Destilador):**

| Propiedad | Slug YAML |
|---|---|
| Identificador | `identificador` |
| Enunciado | `enunciado` |
| Destinatario | `destinatario` |
| Modalidad | `modalidad` |
| Conducta exigida | `conducta_exigida` |
| Condición de aplicación | `condicion_de_aplicacion` |
| Plazo | `plazo` |
| Disposición de anclaje | `disposicion_de_anclaje` |
| Cita textual de respaldo | `cita_textual_de_respaldo` |
| Estado de determinación | `estado_de_determinacion` |
| Enumeración contenida | `enumeracion_contenida` |
| Carácter | `caracter` |
| Sanción (desglose) | `sancion` |

*Nota (29-09-2026): `sancion` y `plazo` son campos únicos legibles que agregan varios datos en su valor (ver justificación y alternativa de desglose en `Propuestas-pendientes.md`, P-03). Las propiedades automáticas y de decisión humana no tienen slug: no se escriben desde los prompts.*

## ④ Agrupaciones

Conjunto de Exigencias a trabajar juntas en un Dominio.

| Propiedad | Tipo / valores |
|---|---|
| Nombre | Título |
| Tipo | Hipótesis inicial / Emergente |
| Origen | Texto |
| Dominio | Relación → ⑤ |
| Exigencias | Relación → ③ |
| Regla(s) que la produjeron | Regla 1–6 / Pase ciego / Propuesta humana |
| Estado | Propuesta → Relatada → (decisión humana) Sostenida / No sostenida / Fusionada / Dividida |
| Criterio de cohesión | 🧾 |
| Evidencia a favor / en contra | 🧾 |
| Decisión y fundamento | 🧾 — **escritura humana** |
| Visada por / Fecha de visado | Person / Date |
| Ítem resultante | Relación → ⑥ |
| Chat de trabajo | URL |

Plantilla obligatoria (ficha de decisión): **«Qué tienes que decidir» va primero**, evidencia después, decisión humana al final. La `No sostenida` conserva la razón y no se elimina.
En el harness, la clave local de una propuesta en `Detector-de-concordancias/Resultados/<dominio>/AGRUPAR.md` sirve para conciliar el relato y la decisión; no crea por sí sola un registro maestro de Agrupación ni un Ítem. El informe de cierre de `Decidir` del Relator enlaza cada propuesta del Detector y cada propuesta humana añadida al ciclo con su decisión humana o pendiente; si se divide o fusiona una propuesta, enlaza también cada propuesta resultante con su propia decisión o pendiente. Concilia por separado las formulaciones de Ítem con sus decisiones y fichas resultantes. Una propuesta sin decisión permanece pendiente: no recibe por inferencia ninguno de los estados de decisión de esta tabla.

## ⑤ Dominios

Área organizacional. **Registro maestro** (esta base) distinto del **home** (página de trabajo bajo la página principal Dominios); los filtros de las vistas se vinculan al **ID del registro maestro**.

| Propiedad | Tipo / valores |
|---|---|
| Nombre | Título |
| Etapa del ciclo | Delimitar / Diagnosticar / Investigar / Agrupar / Decidir |
| Responsable | Person |
| Ítems propios | Relación → ⑥ |
| Agrupaciones | Relación → ④ |
| Fuentes aplicables | Relación → ① |
| Exigencias | Relación two-way → ③ |
| Enlace | `Abrir espacio de trabajo del Dominio` |
| Chat de trabajo | URL |

🧾 Contenido: Qué es / Por qué importa / Qué implica hacerlo + toggle `Proceso y fundamentos del Dominio` con las cinco fases y sus sub-entregas.

**Alcance de Fuentes:** `Fuentes aplicables` relaciona solo las Fuentes y versiones cuya aplicabilidad al Dominio fue confirmada por una persona. La propuesta del Delimitador parte del inventario completo de Fuentes y versiones conocidas, conserva en `Fase - Delimitar` el período del análisis y clasifica cada par según su pertinencia temporal con fundamento y decisión humana cuando hay exclusión. Una exclusión temporal propuesta sin confirmar y toda pertinencia temporal pendiente siguen en el universo por examinar. Las versiones excluidas permanecen visibles en el inventario, con razón; los proyectos se identifican fuera del análisis normativo ordinario salvo escenario encargado expresamente. Una Fuente pendiente no se presenta como no aplicable; una confirmada aplicable sin destilar o todavía no `Lista para uso en Dominio` produce advertencia de cobertura separada. El resumen del Dominio muestra `Análisis de alcance completo: se examinaron X/Y Fuentes y versiones del universo temporal` cuando todas las candidatas se examinaron sustantivamente, o `Análisis de alcance limitado: se examinaron X/Y Fuentes y versiones del universo temporal` cuando alguna no se examinó; `X` y `Y` se definen en `00-Sistema-LPDP.md` §5. Sin período declarado no se calcula `X/Y`; si `Y = 0`, se usa la declaración de alcance indeterminado correspondiente. El indicador no se calcula a partir de la relación `Fuentes aplicables`, pues una Fuente examinada y no aplicable también cuenta en `X`. En el harness, el indicador, las decisiones y los pendientes se conservan en los productos de Delimitar y Diagnosticar antes de implementar la relación. La revisión por cambio se sigue en un expediente `Revisiones/REV-NNNN.md`, separado de `Etapa del ciclo`; esta especificación no agrega otra base de datos.

## ⑥ Ítems

Cuestión jurídica de trabajo. Dos vistas sobre la misma base: **Decisiones sobre Ítems** (kanban de estados, colores con texto) y **Ejecución de Ítems** (tabla: decisión, progreso, siguiente actuación).

| Propiedad | Tipo / valores |
|---|---|
| Nombre | Título |
| Alcance | 🌐 Dominio / 🏢 Organizacional |
| Dominio | Relación → ⑤ |
| Agrupación de origen | Relación → ④ |
| Cuestión jurídica que organiza | 🧾, formulada como pregunta |
| Tipo de resultado | 7 valores |
| Estado (decisión) | Propuesto / Validado / Descartado / Fusionado — **decisión humana** |
| Justificación del estado | 🧾 |
| Aporta a / Recibe aporte de | Auto-relación tipada («la pertenencia es única; el aporte es la relación») |
| Bloqueado por | Relación → ⑧ |
| Exigencias | Relación → ③ |
| Subítems | Relación → ⑦ |
| Formas de cumplimiento | Relación → ⑨ |
| Progreso derivado | Rollup + barra de progreso (un Ítem sin Subítems muestra `Sin descomponer`, nunca 100 %) |
| Severidad máxima | Indicador derivado de los grados fundados en las Exigencias. Si falta calificar alguna y ya existe una vía fundada `3 Gravísima`, muestra `3`; si el mayor grado conocido es inferior, queda sin valor hasta completar el examen. La cobertura incompleta y las fichas afectadas se explican en el fundamento visible del Ítem, no en esta propiedad. La automatización futura debe usar un valor numérico derivado, no un `Max` directo sobre la etiqueta. |

🧾 Ficha: fundamento visible (Agrupación → Exigencias → Disposiciones → Fuentes/versiones, sin copiar el literal completo), con el párrafo `Severidad y cobertura sancionatoria` que identifica el grado sustentado, la cobertura completa o los pendientes y sus fichas enlazadas; toggles `Decisión de creación y antecedentes`, `Cambios y revisiones`, `Resultados y evidencias`. Este párrafo pertenece al cuerpo de la misma ficha, no a una propiedad nueva.

*(La regla del alcance — un Ítem pertenece al Dominio donde vive y se mantiene su **artefacto principal** (el documento, mecanismo o registro que materializa el cumplimiento); y el test de prerrequisito — un prerrequisito es Ítem propio solo si exige trabajo verificable independiente — están desarrolladas con sus ejemplos en el consolidado, sección de estados de decisión del Ítem. Toda implementación LPDP tiene Ítems 🏢 Organizacionales: el RAT es el ejemplo típico, por eso ese alcance existe siempre. La instrucción operativa para clasificar candidatos vive en el prompt del Delimitador de Dominio.)*

## ⑦ Subítems

Parte ejecutable de un Ítem. (En la campaña de testeo actual la base está construida pero no poblada — asunto de `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`, no del canon.)

| Propiedad | Tipo / valores |
|---|---|
| Nombre | Título |
| Ítem padre | Relación → ⑥ |
| Exigencia(s) que lo originan | Relación → ③ |
| Manifestación concreta | Texto |
| Etapa | Delimitar / Estándar / Diagnosticar / Comparar / Decidir / Preparar / Implementar / Evidenciar |
| Estado | 7 valores, incl. `En curso — trabajo parcial`, `Requiere reverificación`, `Bloqueado por dependencia` |
| Criterio de cierre | **declarado al abrir** |
| Bloqueado por | Relación → ⑧ |
| Área responsable | 6 valores |
| Responsable | Person |
| Plazo | Date |
| Formas consultadas | Relación → ⑨ |
| Evidencia de ejecución | Files/URL — obligatoria para `Verificado` («la prueba de que opera») |
| Verificado por | Person — **distinta del responsable** |
| Requiere validación jurídica | Checkbox |
| Chat de trabajo | URL |

## ⑧ Escaladas

Cuestión que el texto no resuelve. Una sola base con vistas (Fuentes, Dominios, decisiones pendientes, bloqueos, historial) y subpágina por home de Dominio.

| Propiedad | Tipo / valores |
|---|---|
| Enunciado | Título |
| Tipo | Laguna / Delegación / Discrepancia de alcance / Conflicto normativo · Revisión de decisión por cambio de fundamento |
| Nace de | Relación → ③ Exigencias |
| Bloquea | Relación → ⑦ Subítems («nace de» y «bloquea» no son sinónimos) |
| Afecta | Relación → ⑥ Ítems |
| Estado | Detectada → Opciones propuestas → Decidida (**humana**) → Superada o desbloqueada |
| Visado por / Fecha de visado | Person / Date |
| Pendiente de instrucción de la Agencia | Checkbox |
| Chat de resolución | URL |
| Fuentes de origen · Disposiciones de origen · Subítems de origen · Dominios afectados · Requiere actuación de · Antecedentes relacionados | Relaciones |
| Criterio requiere revisión | Checkbox (señal) |

🧾 Conserva: opciones mapeadas **incluida la no elegida**, resumen del chat, decisión y fundamento.

**Representación vigente en el harness de archivos:** una ficha
`harness-md-lpdp/Escaladas/ESC-NNNN.md` por cuestión jurídica distinta y una
fila localizadora en `harness-md-lpdp/Escaladas/INDICE.md`, ambas escritas por
el Orquestador. La ficha conserva los campos y relaciones anteriores como
enlaces o pendientes explícitos; si aún no existe Exigencia, registra la
`Disposición de origen` y deja `Nace de` sin Exigencia vinculada, sin alterar
el significado de esa relación. El informe del agente de
Opciones se enlaza como antecedente y no sustituye la ficha. El ID del
archivo es estable y no se reutiliza; `Decidida` requiere decisión humana
con fundamento, y el cierre requiere comprobar dependencias y efectos.

## ⑨ Formas de cumplimiento

Referentes de cómo otros cumplieron. Regla dura: una Exigencia jurídica nunca se funda en fuente extranjera.

| Propiedad | Tipo / valores |
|---|---|
| Nombre | Título |
| Organización/autoridad | Texto |
| Nivel de la jerarquía | ① Norma chilena / ② Instrucción o dictamen de la Agencia / ③ Estándar técnico o comparado |
| Jurisdicción | Select |
| Tipo | 5 valores |
| Qué resolvió | 🧾 |
| Trasladabilidad a Chile | 🧾 (material comparado con advertencia «no vinculante en Chile») |
| Disposición chilena análoga | Relación → ② |
| Ítem que orienta | Relación → ⑥ |
| Subítem que orienta | Relación → ⑦ (declarado, sin uso aún) |

## ~~⑩ Prompts~~ — base eliminada (decisión de MCF, 25-09-2026)

**Decisión:** los prompts dejan de vivir en una base de Notion. Motivo: obligar a un agente a mirar AGENTS.md, luego su PROMPT.md y además una página de Notion añade pasos sin valor y multiplica fuentes de verdad (riesgo de divergencia y doc rot). Desde el 25-09-2026 los prompts viven **solo en archivos**, en la carpeta de agentes (`<Nombre-del-Agente>/PROMPT.md`), con el contrato común en su `AGENTS.md`.

Lo que la base hacía y cómo queda cubierto:

| Función anterior | Cómo queda |
|---|---|
| Nombre del agente | nombre de la carpeta del agente |
| Versión | el archivo vigente es único; una versión anterior se conserva como captura o exportación fechada, sin sufijos en el nombre canónico |
| Fecha de vigencia / Motivo del cambio | decisión humana persistida cuando corresponda y registro de ejecución con fecha real, motivo, ruta y huella o versión comprobable del prompt usado; no se añade una línea de Estado al prompt |
| Vigente (uno por agente) | trivial: hay exactamente un archivo por agente |
| Cuerpo del prompt | el propio archivo |
| ~~Resultado en golden set~~ | sigue eliminado (decisión anterior): la calibración es externa, a cargo del Equipo Legal |

El registro de `Ejecuciones/` identifica el prompt usado mediante ruta, fecha real y huella o versión comprobable de su contenido; una fecha sola no fija la versión exacta.

## ⑪ Bitácora

«Las páginas responden "cómo está esto". La bitácora responde "qué ha pasado".»

| Propiedad | Tipo / valores |
|---|---|
| ID de corrida | Título |
| Corrida | `corrida-AAAA-MM-DD-NN` |
| Fecha y hora | Date — reales, sin retrofechar |
| Agente ejecutor | Select — los 14 nombres |
| Prompt usado | Texto — agente, ruta y fecha real del `PROMPT.md` usado, más huella o versión comprobable de su contenido (la base Prompts se eliminó el 25-09-2026) |
| Tipo de entidad procesada | Select (7 valores) |
| Entidad procesada | URL (Notion no admite relación polimórfica) |
| Veredicto | Verificada / Corregible / Escalada / Sin hallazgos |
| Errores detectados | Texto |
| Acción tomada | 5 valores |
| Validador humano | Person |
| Fecha de validación | Date |
| Observación del validador | Texto |
| Tipo de registro | Ejecución / Incidencia técnica / Corrección material / Referencia de decisión |
| Estado de ejecución | Abierta / En curso / Interrumpida / Requiere actuación / Cerrada |
| Identidad de encargo · ciclo/etapa · último checkpoint · relaciones a Fuente/Dominio/Escalada | campos de trazabilidad de ejecución |

**Principio de proporcionalidad:** conservar fundamento y cambios relevantes, evitando registros equivalentes. Los registros históricos no se borran ni se fusionan retrospectivamente.

Durante la fase de archivos, `Ejecuciones/` y los productos conservan los hechos
del trabajo. La base Bitácora sirve para relaciones y consultas en el espacio
de datos: puede alimentarse como índice o proyección de esos asientos, sin
constituir un segundo historial editable del harness. Antes de implementarla
se definirán identificadores, enlaces y sincronización que permitan comprobar
la correspondencia con los registros de origen.

---

## ⚠️ Dependencias entre bases

**Regla:** ninguna de las propiedades, relaciones o relaciones de esta tabla se borra, renombra, reclasifica o «depura» sin comprobar antes el impacto en la dependencia que la consume. Están dispersas en la prosa de `00-Sistema-LPDP.md` y de este documento; esta tabla las consolida para que una limpieza bienintencionada no rompa la lógica del sistema en silencio.

| # | Propiedad o relación (base) | Depende de / es consumida por | Qué se rompe si se toca sin cuidado | Referencia del fundamento |
|---|---|---|---|---|
| 1 | **Sanción — Calificación** de Exigencias (③): `3 Gravísima / 2 Grave / 1 Leve / 0 No tipificada / Calificación variable según la conducta` | Vistas que filtran la etiqueta y el indicador derivado **Severidad máxima** del Ítem (⑥) | Un máximo directo sobre la etiqueta omite vías variables o vacías; el indicador usa los grados fundados de `## Sanción` y la cobertura incompleta se explica en el fundamento visible del Ítem | `00-Sistema-LPDP.md` §6.2 (indicador y cobertura) |
| 2 | **Texto literal** de Disposiciones (②) como bloque sincronizado | Espejos en Exigencias (③), Agrupaciones (④) e Ítems (⑥): el original vive una sola vez en ② | Convertirlo en texto plano o duplicarlo rompe la propagación del literal y crea divergencias de contenido canónico (documentation drift) | `00-Sistema-LPDP.md` §8 (trazabilidad, bloques sincronizados) |
| 3 | **Nivel de autoridad heredado** de Disposiciones (②) | Rollup → Nivel de autoridad de la Fuente (①) | Desaparece la herencia de autoridad sin releer cada Disposición | §② de este documento |
| 4 | **Nivel de autoridad** de Exigencias (③) | Fórmula de dos saltos Exigencia → Disposición → Fuente, que en Notion requiere `map()` sobre la relación intermedia | La fórmula deja de computar si cambia la relación intermedia | §③ de este documento y «Restricciones técnicas» |
| 5 | **Dominio** de Exigencias (③) | Relación two-way con la base Dominios (⑤) | Romper la two-way deja Exigencias huérfanas de Dominio en una sola dirección | §③ y §⑤ de este documento |
| 6 | **ID del registro maestro** del Dominio (⑤) | Todas las vistas filtradas de los homes de Dominio se vinculan a este ID, no a la página | Recrear el registro cambia el ID y deja todos los filtros de las vistas huérfanos | `00-Sistema-LPDP.md` §5 (estructura del home) y §⑤ de este documento |
| 7 | **Remisiones** de Disposiciones (②) | Auto-relación entre Disposiciones del mismo cuerpo | Perderla obliga a re-leer el corpus para reconstruir el mapa de remisiones | §② de este documento |
| 8 | **Progreso derivado** del Ítem (⑥) | Rollup + barra sobre los Subítems (⑦); regla «un Ítem sin Subítems muestra `Sin descomponer`, nunca 100 %» | Cambiar la regla del rollup falsifica el avance mostrado | `00-Sistema-LPDP.md` §6.2 |
| 9 | **Escaladas (⑧): relaciones `nace de` y `bloquea`** | `nace de` → Exigencias (③); `bloquea` → Subítems (⑦); son relaciones distintas con funciones distintas | Fusionarlas o renombrarlas como sinónimas rompe el circuito de desbloqueo | `00-Sistema-LPDP.md` §6.4 |
| 10 | **Enumeración contenida** de Exigencias (③) | Regla 5 de concordancia (discrepancia de alcance) de la etapa Agrupar | Si se rellena por rutina con «no aplica», la Regla 5 no tiene datos sobre los que computar y la discrepancia vuelve a depender de lectura humana | `00-Sistema-LPDP.md` §5 (etapa Agrupar) y §12.2 |
| 11 | **Resultado de destilación** de Disposiciones (②) | Cobertura del ciclo de Fuente: distingue «no examinada» de «examinada sin Exigencias»; en fase harness su asiento detallado es `Articulos/<unidad>/RESULTADO.md` del Destilador y `COBERTURA.md` resume por artículo | Si desaparece, no hay forma de demostrar cobertura de la destilación; ver §② | `00-Sistema-LPDP.md` §4 (Etapa 4) |
| 12 | **Disposición de anclaje** de Exigencias (③) y regla dura de anclaje | Cadena de custodia completa Exigencia → Disposición → Fuente/versión → documento primario; sin ella la Exigencia «no existe como dato válido» | Una Exigencia sin anclaje verificable es contenido plausible sin fuente (AI slop) | `02-Gobernanza-y-Context-Engineering.md` §6 |

---

## Restricciones técnicas de Notion conocidas

- **Rollup de dos saltos** (Exigencia → Disposición → Fuente) requiere `map()` sobre la relación intermedia.
- **No hay relaciones polimórficas**: «Entidad procesada» en Bitácora es URL.
- **Dominio multi-select → relación two-way** (corrección histórica del Anexo C de v6).
- **Los colores nunca son el único canal**: mapa oficial 🟢 finales positivos · 🔵 en proceso · 🟡 atención · 🔴 bloqueado/gravísimo/testeo · ⚪ cerrado sin continuar (`Fusionada`/`Dividida` en gris, no verde).
- **Vistas filtradas ≠ permisos.** Ninguna fórmula es correcta por no fallar en una base vacía.
- **No hay transacción atómica** entre archivos y Notion: escritura coordinada + comprobación antes de reanudar.

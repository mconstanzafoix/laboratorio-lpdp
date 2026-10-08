# 02 — Gobernanza, fuentes únicas de verdad y context engineering

**Estado:** contenido previo visado por MCF; ajustes de gobierno solicitados el 01-10-2026 y el 02-10-2026 incorporados para revisión de su redacción, sin atribuirles un visado posterior. **Última revisión:** 02-10-2026. El historial anterior vive en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/`. *(El 30-09-2026 este paquete se trasladó a `Laboratorio LPDP/Insumos/planificacion/documentos-canonicos/` — única ubicación vigente del canon.)*
**Propósito:** que este sistema pueda traspasarse a fuentes únicas de verdad y documentos canónicos sin pudrirse: contratos de traspaso efectivos, trazabilidad, divulgación progresiva, gates humanas, política de retención y defensas explícitas contra AI slop, artifact sprawl, filename versioning, documentation drift, context rot, prompt sprawl, provenance gap y deuda técnica generada por IA.

---

## 1. Mapa de fuentes únicas de verdad (SSOT)

Cada tipo de conocimiento tiene **una** fuente canónica y una sola. Todo lo demás es copia derivada, vista o caché — y se nombra como tal.

| Conocimiento | Fuente única de verdad | Derivados permitidos (no canónicos) |
|---|---|---|
| Reglas de gobierno del sistema | `planificacion/harness-md-lpdp/AGENTS.md` | referencias desde otros documentos |
| Contratos de agentes | `planificacion/harness-md-lpdp/<Nombre-del-Agente>/PROMPT.md` (uno por agente) + el `AGENTS.md` de la raíz del harness | otras carpetas de prompts son antecedentes o copias no despachables; no se sincronizan en dos direcciones |
| Arquitectura del sistema | `planificacion/documentos-canonicos/00-Sistema-LPDP.md`; esquema de propiedades en `01-Bases-de-Datos-y-Propiedades.md` | exportaciones fechadas de solo lectura; ninguno de estos archivos se sustituye por un nombre de arquitectura inexistente |
| Estado de implementación futura | las bases de datos cuando se implementen | informes y registros; no condiciona el trabajo actual en archivos |
| Instrucciones vigentes para ejecución | `AGENTS.md` + el `PROMPT.md` del rol + cada `SKILL.md` obligatoria declarada por ese prompt en `planificacion/harness-md-lpdp/` | `MEMORY.md` se carga solo si existe; perfiles de corrida solo cuando aplican; referencias de una skill se leen según el caso |
| Método intensivo de dudas normativas durante destilación | `planificacion/harness-md-lpdp/skills/examen-intensivo-destilacion/SKILL.md` | referencia de casos de control dentro de su propia carpeta; no es una segunda fuente de derecho ni un catálogo de resultados |
| Método de calificación sancionatoria de Exigencias | `planificacion/harness-md-lpdp/skills/calificar-sancion-exigencia/SKILL.md` | subsunción de una conducta infractora hipotética en un tipo, con fundamento en la ficha; no decide sanciones de casos concretos |
| Qué ha pasado en el harness | `planificacion/harness-md-lpdp/Ejecuciones/*.md` y productos persistidos | resúmenes enlazados; la Bitácora conserva su función cuando se trabaje en el espacio de datos |
| Estado y decisiones de cada Escalada durante la fase de archivos | `planificacion/harness-md-lpdp/Escaladas/ESC-NNNN.md` | `Escaladas/INDICE.md` localiza fichas; informes de Opciones son antecedentes, no expedientes |
| Estado y autorizaciones de cada Revisión por cambio durante la fase de archivos | `planificacion/harness-md-lpdp/Revisiones/REV-NNNN.md` | `Revisiones/INDICE.md` localiza fichas; el mapa del Analista y `Ejecuciones/` conservan sus funciones propias |
| Texto normativo primario | `planificacion/harness-md-lpdp/Fuentes-primarias/<cuerpo-y-versión>/*.pdf` (con SHA-256 en el `FUENTE.md` de la Fuente fragmentada) | mirrors oficiales documentados |
| Fragmentos y resultados de agentes | `planificacion/harness-md-lpdp/Fragmentador-de-Fuentes/Fuentes/<fuente-y-version>/…` y `planificacion/harness-md-lpdp/Destilador-de-Exigencias/Resultados/<fuente-y-version>/…` | fichas de datos derivadas cuando se implementen; Exigencias de Fuentes distintas no comparten carpeta |

**Regla de traspaso:** mover conocimiento de una fuente a otra exige un **contrato de traspaso**: qué campo/bit viaja, de qué fuente a cuál, quién escribe, quién comprueba, y qué queda deprecado. Un traspaso sin deprecación explícita crea dos verdades. La decisión del 01-10-2026 fija el harness como fuente vigente de prompts; `workspace-lpdp/` deja de ser fuente de despacho, sin borrar su historia.

## 2. Prohibiciones absolutas de higiene documental

1. **Prohibido versionar con sufijos** (`doc-v2-final-FINAL2.md`). Un archivo canónico tiene **un solo nombre estable**; la versión vive dentro (frontmatter) y la historia vive en el registro. Los respaldos antes de un cambio material viven en `registros/` con fecha, nunca junto al canónico con un nombre competidor.
2. **Prohibido duplicar contenido canónico del sistema.** Otro documento de arquitectura puede *referenciar* (`ver X, §N`), nunca copiar una regla de gobierno para crear dos fuentes de instrucción. Esta prohibición no elimina el texto literal presente en **dos cuerpos normativos primarios distintos**: la ley modificatoria puede reproducir lo que aparece en la consolidada, y cada transcripción conserva su propia identidad, versión y procedencia. Esa coincidencia se coteja; no se borra por parecer duplicada.
3. **Prohibido el consenso por silencio.** Un documento propuesto no se vuelve canónico por ausencia de objeción: requiere visado humano con nombre y fecha (misma regla que los estados jurídicos).
4. **Prohibido retrofechar** o «regularizar» registros. Fechas reales; si la hora original no se registró, se escribe literalmente eso.
5. **Prohibido declarar hecho lo propuesto.** «No presentes una propuesta como resultado ya ejecutado.»

## 3. Estructura del espacio de trabajo

El mapa vigente de los documentos canónicos y de la carpeta de agentes vive una sola vez: en el `README.md` de este nivel y en el `INDICE.md` de la carpeta de agentes. No se duplica aquí (prohibición 2 de §2): el árbol ASCII que esta sección contenía se retiró el 30-09-2026 por divergencia con el disco (minuta 12 en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/Minutas-de-decision-2026-09-30.md`).

**Nota:** el espacio de trabajo de ejecución es
`planificacion/harness-md-lpdp/`, declarado en el `README.md` del paquete.
El Orquestador queda **separado** de AGENTS.md, en `Orquestador/PROMPT.md` — la
regla «un agente = una carpeta» no tiene excepciones.

Reglas del árbol:

- **Divulgación progresiva:** cada carpeta explica su contenido en su propio `INDICE.md`/README de ≤ 1 pantalla, con enlaces — nadie (humano ni IA) necesita cargar todo el sistema para trabajar en una carpeta. Un agente recibe en su encargo solo lo que su tarea requiere.
- **Un `INDICE.md` desactualizado es un defecto reportable**, no un adorno. Su árbol y verificación deben reflejar las carpetas y prompts realmente despachables.
- **Artifact sprawl:** todo archivo nuevo debe tener (a) un dueño-agente o humano, (b) un destino canónico en el árbol, (c) un motivo registrado en la ejecución que lo creó. Un archivo sin las tres cosas es un huérfano y se reporta.

### 3.1 Método del árbol anotado

Regla de context engineering adoptada como estándar canónico de documentación, aprobada por MCF el 25-09-2026:

1. **Todo índice o documento que organiza otros archivos lleva un árbol ASCII anotado**: el mapa completo antes del detalle, con una anotación corta por entrada (rol o función, no resumen). Un agente o persona que aterrice en la carpeta entiende el esqueleto sin abrir nada más. Es el mismo principio del `ARBOL.md` del Fragmentador aplicado a la propia documentación.
2. **Cada árbol declara el orden de lectura por rol**: quién carga qué y — igual de importante — qué **no** debe cargar. Esto opera la divulgación progresiva (§8) y es la defensa concreta contra el context rot.
3. **Artefacto visual de la regla «índice desactualizado = defecto reportable»**: el árbol cierra con una **línea de verificación** mecánica — `Verificación del índice: N entradas listadas — última comprobación DD-MM-AAAA contra disco`. La comprobación es contar entradas del árbol contra el disco (listar la carpeta y comparar); si difieren, el índice está roto y cualquiera (humano o agente) puede reportarlo sin juicio de valor. Quien agrega, renombra o elimina un archivo actualiza el árbol y la fecha en la misma operación.
4. **Dónde está implementado:** el `README.md` de los documentos canónicos (árbol del paquete + orden de lectura por rol) y el `INDICE.md` de la carpeta de agentes (árbol de prompts + regla de lectura acotada).
5. **Alcance canónico:** esta regla aplica a todo espacio de trabajo futuro del Laboratorio (el árbol de ejecución de §3 y cualquier carpeta nueva con más de 3 archivos).

## 4. AGENTS.md consolidado — reglas de gobierno

> El texto vigente vive en el `AGENTS.md` de la carpeta de agentes — un solo archivo de arranque, por decisión de MCF (25-09-2026), que fusiona las reglas de gobierno (Parte I) con el contrato común inyectable (Parte II). Ante cualquier diferencia, manda ese archivo. Su contenido no se duplica aquí (prohibición 2 de §2): la cita del texto fundacional que esta sección contenía se retiró el 30-09-2026 al diverger del vigente (minuta 12 en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/Minutas-de-decision-2026-09-30.md`).

## 5. Cómo usar SKILL.md y MEMORY.md (y cómo no)

El sistema distingue tres tipos de instrucción persistente:

| Pieza | Qué contiene | Cuándo se carga | Quién la edita |
|---|---|---|---|
| **AGENTS.md** | Reglas de gobierno del sistema (lo de §4) | Siempre, al inicio de toda sesión en el espacio | Humano + Agente de Arquitectura, con visado |
| **PROMPT.md por agente** | Contrato específico del rol | Solo cuando ese agente es despachado | Agente de Arquitectura propone y una persona decide; el Orquestador registra en `Ejecuciones/` la ruta, fecha real y huella o versión comprobable del prompt usado, sin añadir metadatos editoriales al contrato |
| **SKILL.md** (obligatoria solo cuando un prompt la declara) | Método especializado y reutilizable, con operaciones de razonamiento que exceden el contrato breve de un rol sin sustituirlo; puede servir a uno o más roles | La skill declarada obligatoria se entrega íntegra en cada ejecución del rol; su examen profundo opera cuando se cumple su disparador | Agente de Arquitectura, con registro |
| **MEMORY.md** (opcional por agente) | Punteros operativos que cambian una decisión futura y no se recuperan fácilmente desde productos y `Ejecuciones/` | Solo si existe, después del PROMPT.md | El propio agente propone; Orquestador verifica que no duplique canon ni registro |

Reglas anti-rot para estas piezas:

- **SKILL.md no es un cajón de sastre**: el `PROMPT.md` conserva rol, disparador obligatorio y destino del resultado; la skill desarrolla un método complejo que puede repetirse entre Disposiciones o roles. Una regla que rige a todos sigue en `AGENTS.md`. No se duplican pasos extensos ni respuestas de casos en prompt y skill.
- **Ubicación y carga de los métodos vigentes:** `harness-md-lpdp/skills/examen-intensivo-destilacion/SKILL.md` y `harness-md-lpdp/skills/calificar-sancion-exigencia/SKILL.md` son las rutas maestras respectivas. El prompt del Destilador exige cargar ambos textos íntegros en toda ejecución; el Orquestador comprueba ruta y SHA-256 de cada uno y los incluye expresamente en el despacho. El examen intensivo se aplica por su disparador; la calificación sancionatoria se aplica a toda ficha creada o revisada y se comprueba en todas las fichas al cerrar el cotejo de una Fuente. La lectura de `references/casos-de-control.md` del primer método depende de la duda. El Orquestador comprueba la presencia y trazabilidad del examen en `RESULTADO.md` y de la subsunción o el pendiente sancionatorio en la ficha; ninguna comprobación es visado jurídico.
- **MEMORY.md tiene política de retención**: cada entrada lleva fecha; las entradas superadas se marcan `superada el DD-MM-AAAA por <qué>` (no se borran); entradas > 90 días sin uso se revisan o se archivan a `registros/`. La memoria nunca contradice al canon: si lo hace, el canon manda y la memoria se corrige.
- **Todo lo durable que un agente necesita saber debe vivir en archivos o en Notion, no en la conversación** (esa es la defensa central contra el context rot: el sistema se reconstruye desde sus artefactos).

### 5.1 Diseño de MEMORY.md

1. **No se crea por rutina.** Si una necesidad repetida justifica un `MEMORY.md`, vive junto al `PROMPT.md` de ese rol y solo ese rol la carga. El Orquestador recupera trabajos en curso desde `Ejecuciones/` y productos; su memoria tampoco es obligatoria.
2. **Orden de arranque de sesión** (fijado también en el contrato común): `AGENTS.md` → `PROMPT.md` del agente → `SKILL.md` obligatoria declarada por ese prompt, si la hay → `MEMORY.md`, si existe → perfil aplicable, si existe → encargo. Si una skill obligatoria falta o no puede leerse, el trabajo dependiente no se despacha; mencionar su nombre no equivale a cargarla.
3. **Regla de escritura**: solo se anota lo que **cambia una decisión futura**; entrada = línea fechada + una frase + enlace al artefacto durable; lo que ya está en el canon o en una base se enlaza, no se copia; prohibido párrafos narrativos.
4. **Jerarquía**: canon > precedentes visados > memoria operativa. La memoria nunca es fuente de verdad: es un puntero fechado a las fuentes.
5. **Criterio de escala** (declarado para evitar sobre-ingeniería): no se usan embeddings, curación automática ni resúmenes de sesión — con decenas de entradas, un archivo legible con retención fechada da más trazabilidad que cualquier mecanismo. Si el volumen crece, el siguiente escalón son índices de memoria por tema, a decidir cuando duela.
6. En el harness vigente no se requiere ningún `MEMORY.md` para arrancar. Los archivos de memoria de otras carpetas conservan su carácter de antecedente, no de instrucción despachable.

### 5.2 Criterios de redacción de prompts

Reglas obligatorias al escribir o revisar el `PROMPT.md` de cualquier agente. Quien edita prompts (Agente de Arquitectura propone, humano visa) las aplica; se estrenaron en la revisión del Fragmentador de Fuentes del 25-09-2026.

1. **Fronteras negativas sin nombres de rol.** Un prompt delimita el alcance diciendo qué **no** es trabajo del agente («no extraes Exigencias», «la extracción pertenece a una etapa posterior»), **sin nombrar al agente que sí lo hace**. Nombrar roles de contenido acopla los prompts (si el otro cambia, este queda obsoleto sin aviso) e infla el contexto con información que no cambia la conducta.
2. **Excepción Orquestador.** Es el único rol nombrable, porque no es una etapa de contenido sino la **interfaz** de todo agente: de él recibe el encargo y a él le devuelve. Nombrarlo no acopla ni sesga.
3. **Sin conceptos de decisión ajenos que puedan sesgar el juicio.** Un agente productor no conoce objetos de decisión del sistema que no opera (p. ej. la Escalada no se menciona en prompts de producción: el agente registra hallazgos; qué se hace con ellos «no es su materia»).
4. **Propiedades ajenas: prohibido completarlas y deben quedar vacías.** No basta «no las escribas»: se declara explícitamente que quedan vacías, para que el completismo no las rellene.
5. **Autosuficiencia.** Todo término usado como instrucción se define en el propio prompt (bloque «Términos de este prompt» o glosa en línea en su primer uso). Las referencias cruzadas internas van **por nombre de campo, nunca por número**. Todo ejemplo lleva disclaimer («sólo muestra el formato: no atribuye…»).
6. **Sin vocabulario de etapas ajenas.** Si el agente no actúa sobre un concepto (p. ej. la Modalidad en fragmentación), no se menciona: nombrarlo es contexto muerto que confunde.

## 6. Cadena de custodia y proveniencia (anti provenance gap)

Todo dato del sistema puede responder «¿de dónde saliste?»:

1. **Exigencia → Disposición → Fuente/versión → documento primario (SHA-256).** La clave de Exigencia es `<fuente-y-version>/EX-NNN`; `EX-NNN` aislado es solo local. Cada ficha tiene al menos un anclaje principal de su Fuente. Sin esta cadena, la Exigencia no existe como dato válido.

   > **¿Qué es SHA-256, en palabras simples?** Es una **huella digital de un archivo**: una función matemática que convierte cualquier archivo en un código único de 64 caracteres (p. ej. `3e32f910…`). Si cambia aunque sea una coma del PDF, la huella cambia por completo. Sirve para dos cosas: (a) **demostrar que el texto con el que se trabajó es exactamente ese documento oficial y no otro parecido**, y (b) **detectar** si el archivo cambió después. La regla del sistema: cada PDF primario en `Fuentes-primarias/` tiene su huella registrada en su `FUENTE.md`, y cada cotejo de literales declara contra qué huella se hizo. Lo que la huella **no** hace: permitir reconstruir el archivo si se pierde — por eso la política de retención (§7) exige conservar copias, no solo huellas.
2. **Resultado de agente → prompt usado y skills obligatorias, si las hubo (rutas, fecha real y huellas o versiones comprobables en `Ejecuciones/`) → encargo → comprobación técnica del Orquestador → decisión humana, solo cuando corresponde.** La comprobación técnica no equivale a visado jurídico.
3. **Documento canónico → propuesta fechada → visado humano → registro del cambio.** Las correcciones se hacen por **fe de erratas trazable** (práctica heredada del análisis comparativo), nunca por reescritura silenciosa.
4. **Fragmento de archivo → `FUENTE.md` con hash → cotejo mecánico** (el harness ya demuestra el patrón: «147.567 caracteres normalizados, coincidencia exacta»).

**Comprobación de proveniencia al cerrar cada etapa:** Orquestador verifica que cada objeto nuevo tiene su cadena completa; un objeto con cadena rota queda `pendiente con responsable`, nunca se «completa» por decoro.

## 7. Política de retención

| Qué | Política |
|---|---|
| Registros históricos (Bitácora, Ejecuciones) | **No se borran ni se fusionan retrospectivamente.** |
| Versiones anteriores de un objeto corregido | Se conservan como **contenido estable** (captura/exportación fechada). Una huella detecta cambios pero no permite reconstruir: no basta. |
| Decisiones humanas | Permanentes, con fundamento, incluida la opción no elegida. |
| Fichas de decisiones negativas (`No sostenida`, `Descartado`) | Permanentes: «son la evidencia de que se consideró y se descartó». |
| ~~N.º de ingreso~~ | Eliminada del esquema el 25-09-2026 (decisión de MCF): la identidad inmutable la da el Identificador canónico, que **no se reasigna ni se reutiliza** — esa es la regla de retención que queda en su lugar. |
| Respaldos pre-cambio | En `registros/` con fecha, antes de cada reorganización. |
| Artefactos temporales de verificación (`tmp/`) | Conservables mientras la comprobación que sustentan siga citada; luego se archivan, no se borran en caliente. |

## 8. Divulgación progresiva y manejo de contexto (context engineering)

- **El encargo es la unidad de contexto**: el agente recibe contrato común + contrato específico + `MEMORY.md` si existe + perfil si aplica + encargo concreto, y nada más. «No entregues solo enlaces ni supongas que el ejecutor hereda tu contexto.»
- **Contextos separados donde el rol lo exige**: el Auditor preserva su mapa desde el PDF primario, cuerpo, versión y huella esperada, sin `FUENTE.md`, `ARBOL.md`, Disposiciones ni productos de los autores; después examina esos razonamientos como objeto de auditoría. El Detector de concordancias preserva su pase ciego antes de ver el mapa interpretativo de Investigar, Agrupaciones e Ítems; el Relator conserva su contraste independiente antes de conocer el mapa del Detector. Después de preservar ambos resultados, el Orquestador concilia divergencias por clave: un texto o cotejo faltante vuelve al especialista, y un hecho de la organización faltante sigue el circuito de Diagnosticar con pregunta humana presentada por el Orquestador; este no escoge entre interpretaciones jurídicas. Una cuestión jurídica persistente se encamina a decisión humana.
- **Lectura escalonada**: índice primero (AGENTS.md → INDICE.md → ARBOL.md/COBERTURA.md), detalle después. Nadie lee 1.583 archivos para encargar una corrección de uno.
- **Alcance del Dominio sin selección silenciosa**: el Orquestador registra el período del análisis y entrega al Delimitador el inventario completo de Fuentes y versiones conocidas, con rutas, vigencia y estados técnicos. El Delimitador conserva todas las entradas, clasifica su pertinencia temporal con fundamento y examina de forma escalonada las candidatas; una exclusión temporal propuesta necesita confirmación humana para salir del denominador `Y`. «Examinar todas las candidatas» no exige cargar todos los primarios simultáneamente ni permite descartar una Fuente por no estar destilada o aún no lista. En Diagnosticar, el Delimitador prepara y analiza preguntas agrupadas por ronda; el Orquestador comunica y conserva cada respuesta junto al texto preguntado, sin sustituir su análisis ni los hechos de la organización. Antes de Investigar, el Orquestador fija una lista identificable de claves completas de las Exigencias activas de Fuentes confirmadas aplicables y `Lista para uso en Dominio`, conciliada con `COBERTURA.md` y su cierre de aptitud, y transmite el mismo universo al Detector y al Relator en contextos separados; mantiene las demás Fuentes, incluidas las aplicables aún no listas, y las fichas históricas fuera del universo activo con su razón o bloqueo visible.
- **Checkpoints**: si un trabajo queda parcial, bloqueado o a la espera de decisión, su propio producto y el registro breve del Orquestador indican última unidad comprobada, pendientes, impedimento, siguiente acción y responsable para reanudar «sin depender de recordar esta conversación». Un trabajo completo declara que no tiene reanudación pendiente; no se exige un archivo de checkpoint por agente.
- **Conciliación al reanudar**: Orquestador compara estado persistido vs. real antes de continuar (la concurrencia técnica real queda declarada como límite, no simulada).

## 9. Catálogo de anti-patrones y su defensa concreta en este sistema

| Anti-patrón | Defensa del sistema |
|---|---|
| **AI slop** (contenido plausible sin anclaje) | Regla dura de anclaje; cita textual obligatoria; «no inventes un campo para llenarlo»; auditoría con contexto separado |
| **Artifact sprawl** | Árbol canónico (§3); todo archivo con dueño, destino y motivo registrado; huérfanos reportables |
| **Filename versioning** | Prohibición absoluta (§2.1); la versión anterior se conserva como captura o exportación fechada, y el cambio queda en el registro de ejecución y la decisión humana correspondiente |
| **Documentation drift / doc rot** | SSOT por tipo de conocimiento (§1); referencias en vez de copias; INDICE desactualizado = defecto; Agente del Manual vigila el Manual, Agente de Arquitectura la coherencia estructural |
| **Context rot** | En la fase actual todo lo durable vive en `planificacion/`; encargos autónomos; checkpoints en productos y registro; conciliación al reanudar |
| **Prompt sprawl** | Un `PROMPT.md` por agente y una versión vigente del método en su `SKILL.md`; el contrato común se mantiene una vez y se inyecta; cada skill tiene un disparador definido, sin duplicar contratos ni casos resueltos |
| **Provenance gap** | Cadena de custodia de §4 verificada al cerrar cada etapa; `Ejecuciones/` identifica el prompt exacto y la Bitácora del espacio de datos puede indexar esa referencia |
| **Deuda técnica generada por IA** | Clasificación de cambios (presentación/visibilidad/funcional/incierta) con comprobación del Agente de Arquitectura y decisión humana cuando corresponda; fe de erratas; registro de decisiones operativas con motivo en cada ejecución |

## 10. Proceso de promoción a canónico

1. Propuesta fechada (archivo nuevo o edición) →
2. Revisión humana →
3. Visado con nombre y fecha (go/no-go o con fundamento, según contenido) →
4. Agente de Arquitectura actualiza versiones (`p`/`i`/`v`, sin cruzar contadores), regenera exportaciones y manifiesto con huellas →
5. Agente del Manual actualiza el Manual →
6. Orquestador registra el cambio en `Ejecuciones/`; cuando se trabaje en el espacio de datos, la Bitácora puede indexarlo →
7. Lo superado se marca `superado el DD-MM-AAAA por <qué>`, nunca se borra en caliente.

## 11. Registro de riesgos operativos

Los riesgos identificados en la Propuesta-Spec v6, actualizados al estado del sistema consolidado. Cuando la mitigación ya existe en el diseño, se dice dónde vive; cuando sigue abierta, se dice qué falta.

| # | Riesgo | Prob. | Impacto | Mitigación y su estado |
|---|---|---|---|---|
| 1 | El sistema absorbe el tiempo de la implementación real | Alta | Crítico | Dos carriles: ningún entregable legal espera al sistema. **Sigue siendo disciplina de gestión, no del diseño.** |
| 2 | Un agente mal calibrado modifica en masa cientos de entradas | Media | Alto | Respaldo externo antes de cada corrida masiva; probar sobre vista filtrada de pocos registros antes de escalar. Regla vigente en testeo (`/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`). |
| 3 | Falso negativo: una Exigencia relevante nunca se destila | Media | Crítico | **Mitigación de diseño:** `ARBOL.md` del Fragmentador se coteja con el texto primario; desde ese árbol el Destilador crea `RESULTADO.md` por artículo o, si la estructura real declarada en el árbol lo requiere, por subíndice de unidad, con una fila única por Disposición, y `COBERTURA.md` agrega el avance de la Fuente. Se distingue «no examinada» de «examinada sin Exigencias». El Auditor de anclaje preserva una lectura propia del PDF antes de ver la destilación y luego contrasta omisiones y fidelidad; ese segundo control importa porque la revisión del productor puede repetir su propio punto ciego. `Lista para uso en Dominio` exige resolver los hallazgos materiales y reauditar sus efectos antes de usar esas Exigencias en Investigar. El detalle de los dos pases y la compuerta vive en `00-Sistema-LPDP.md` §4. Su funcionamiento sobre una destilación completa todavía no se ha comprobado. |
| 4 | Contaminación por derecho comparado | Media | Alto | **Mitigado:** regla dura de anclaje — una Exigencia nunca se funda en fuente extranjera; el comparado solo orienta. Es punto de checklist del Auditor. |
| 5 | Sesgo de automatización (aceptar lo que la IA propone sin revisar) | Alta con el tiempo | Alto | Procedencia del prompt, distinción entre comprobación técnica y decisión jurídica, y espacio humano vacío cuando corresponde. La calibración periódica con errores sembrados sigue **pendiente de implementar**. |
| 6 | Costo de créditos con agentes por lotes | Media | Medio | Medir consumo en calibración antes de escalar. Abierto. |
| 7 | El sistema audita texto, no práctica | Alta | Alto | El estándar de evidencia de ejecución (inspirado en el art. 14 quinquies: **existencia y funcionamiento**, no solo documento) se aplica a todo Subítem — ver el consolidado, sección de enrutamiento de validación. El Orquestador exige la forma de la evidencia; la declaración `Verificado` es humana. |
| 8 | La complejidad del sistema se vuelve barrera de uso | Alta | Alto | La capa de lectura (Qué es / Por qué importa / Qué implica hacerlo, en lenguaje llano para no técnicos) es la mitigación de diseño; los árboles ASCII anotados con orden de lectura por rol (§3.1 de este documento) la complementan. |
| 9 | Rotación del equipo antes de que llegue el DPO | Media | Alto | Escaladas con fundamento documentado (incluida la opción no elegida): el conocimiento de las decisiones no depende de personas. **Mitigado por diseño.** |
| 10 | Numeración o identidad de unidades incorrecta | Media | Alto | **Mitigación de diseño:** identidad = cuerpo + versión + identificador declarado + ruta comprobable en `ARBOL.md`; cotejo con texto primario y posterior auditoría de anclaje. Los esquemas numéricos simples no cubren intercalados, transitorios o instrucciones modificatorias; la comprobación completa sigue pendiente. |
| 11 | Una Exigencia `Delegada` se implementa como definitiva | Media | Medio | **Mitigado en el dato:** el campo Estado de determinación (Determinada / Delegada / Indeterminada, sin valor por defecto) hace visible la condición. La futura vigilancia dará prioridad a las Exigencias `Delegada` relacionadas con el pronunciamiento, sin excluir otras potencialmente afectadas; queda **diseñada pero no implementada** — ver el consolidado, sección de cambio normativo. |
| 12 | Fuente aplicable sin destilación o sin aptitud para uso en Dominio | Media | Alto | **Mitigación diseñada:** advertencias separadas por condición en el home del Dominio y entrada sustantiva a Investigar limitada a Fuentes `Lista para uso en Dominio` (consolidado, ciclos de Fuente y Dominio); todavía se debe comprobar que las advertencias se generen y desaparezcan con el estado real. |

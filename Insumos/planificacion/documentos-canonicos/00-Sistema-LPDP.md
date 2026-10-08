# 🧪 Laboratorio LPDP — Sistema consolidado, explicado de inicio a fin

**Documento:** consolidado canónico de lectura
**Estado:** contenido previo visado por MCF; ajustes solicitados el 01-10-2026, el 02-10-2026 y el 08-10-2026 incorporados para revisión, sin atribuirles un visado posterior. Ninguna parte de este documento está activa por sí sola: su promoción sigue el proceso de `02-Gobernanza-y-Context-Engineering.md` §10. **Última revisión:** 08-10-2026. El historial anterior vive en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/`. *(El 30-09-2026 este documento se trasladó a esta carpeta.)*
**Fecha:** 25-09-2026

> **Convención de estos documentos:** nada se cita por números sueltos («03», «R2»). Los archivos se nombran por su nombre real. Las fechas se escriben DD-MM-AAAA. Las reglas de **testeo, compuertas y corridas NO son canónicas** y viven aparte; este documento describe solo la arquitectura canónica. **Nombres por función, no por carpeta:** el canon nombra «la carpeta de agentes», «el `PROMPT.md` del "Nombre de Agente"», «el `AGENTS.md`» — nombres de archivo estables — y **no** el nombre de la carpeta contenedora, que es circunstancial; su nombre y ubicación vigentes se declaran una sola vez, en el `README.md` de este paquete.

> **Cómo leer este documento.** Se lee de corrido: primero qué es el sistema y por qué existe, luego el mapa de piezas, y después cada ciclo etapa por etapa — con el agente que interviene, lo que entrega y la tabla de propiedades de Notion que usa. Los detalles finos viven en las piezas hermanas: contratos completos de agentes — el contrato común en el `AGENTS.md` de la carpeta de agentes y cada contrato específico en el `PROMPT.md` de la carpeta de su agente —, todas las propiedades de las bases en `01-Bases-de-Datos-y-Propiedades.md`, las reglas de gobierno en `02-Gobernanza-y-Context-Engineering.md`, y los problemas detectados con sus correcciones en `/Users/mcfoix/Desktop/Gestion del Caos/informes/04-Diagnosticos-y-Desfases.md`.

***

## 1. Qué es el sistema y por qué existe

El Laboratorio LPDP es un sistema para **implementar la Ley chilena de Protección de Datos Personales** (Ley 19.628 consolidada con la reforma 21.719, y su reglamento, Decreto 662) en una organización, usando un espacio de trabajo en **Notion** operado por **agentes de IA** bajo supervisión humana.

El fundamento combina exigencias jurídicas y una regla interna de gobierno responsable. El art. 8° bis de la Ley 19.628 protege al titular frente a decisiones automatizadas que le producen efectos jurídicos o le afectan significativamente; el art. 14 quáter exige medidas de protección desde el diseño y por defecto. Ninguno impone literalmente visado humano para cada decisión interna del Laboratorio. La supervisión y trazabilidad internas son una decisión de gobierno del sistema, informada por los riesgos y deberes del régimen. De ahí la frase rectora del sistema:

> «Un sistema de cumplimiento LPDP que operara sin supervisión humana sería, él mismo, un problema de cumplimiento LPDP.»

Consecuencias estructurales de ese fundamento:

* **Las decisiones con contenido jurídico son humanas**: `Visada`, `Sostenida`, `Validado`, `Verificado`, `Decidida` y el visado de autoridad de una Fuente los fija una persona, con nombre y fecha. Un agente nunca mueve nada a esos estados por conclusión propia, y un silencio humano no autoriza nada.

* **La intervención humana en decisiones jurídicas reservadas es una regla permanente del sistema**: su alcance se determina por el riesgo y la responsabilidad de esas decisiones. Se distingue del derecho del titular a intervención humana ante decisiones automatizadas del art. 8° bis.

* **El sistema no decide, no acredita cumplimiento y no reemplaza criterio jurídico.** Que un Ítem esté `Validado` significa que se decidió trabajarlo, no que esté cumplido.

* **El sistema debe decir cuándo su propia información está incompleta.** Si un Dominio muestra «N Exigencias» mientras hay una Fuente aplicable sin destilar, ese número no es el universo completo — y el sistema debe advertirlo por sí mismo, no depender de que alguien lo recuerde (mecanismo concreto en §5, «Estructura del home del Dominio»).

### 1.1 Qué NO es el sistema

* No es un pipeline de un encargo puntual.

* No es una auditoría de la práctica operativa de la organización.

* No es un generador de texto legal: es una **máquina de conocimiento jurídico trazable**, donde cada conclusión puede seguirse hacia atrás hasta el literal del artículo que la funda.

### 1.2 La lógica deóntica: la pieza que sostiene todo

**Qué es.** Rama de la lógica que formaliza los enunciados sobre **deberes**: lo obligatorio, lo permitido y lo prohibido.

| Operador               | Significado          | Marcador típico en la ley        |
| ---------------------- | -------------------- | -------------------------------- |
| **Obligación** — O(p)  | Es obligatorio que p | «deberá», «estará obligado a»    |
| **Permiso** — P(p)     | Está permitido que p | «podrá», «estará facultado para» |
| **Prohibición** — F(p) | Está prohibido que p | «no podrá», «queda prohibido»    |

Se relacionan: `F(p) ≡ O(¬p)` y `P(p) ≡ ¬O(¬p)`.

**Por qué importa.** La diferencia entre *«deberá informar»* y *«podrá informar»* no es de redacción: es de naturaleza jurídica. **Un modelo de lenguaje leyendo prosa jurídica tiende a aplanar esa diferencia**, porque en el uso corriente ambos son «el responsable informa». Ese aplanamiento explica que una salida sin método califique todos los riesgos con intensidad media. **La solución no es pedir más cuidado al modelo**: es fijar la modalidad como **propiedad del dato**, determinada una vez, auditada, y disponible desde entonces sin depender de que el modelo vuelva a leer bien.

**El núcleo deóntico.** Los cuatro elementos mínimos que hacen una norma comparable y verificable:

| Elemento                    | Pregunta                          |
| --------------------------- | --------------------------------- |
| **Destinatario**            | ¿Quién está sujeto?               |
| **Modalidad**               | ¿Obligado, permitido o prohibido? |
| **Conducta**                | ¿A qué exactamente?               |
| **Condición de aplicación** | ¿Bajo qué circunstancias?         |

Con esos cuatro campos, dos normas de cuerpos distintos se comparan **mecánicamente**. Sin ellos, comparar dos artículos requiere leerlos y opinar, que es lo que no escala y no deja trazabilidad.

**Dónde vive en este sistema.** Estos cuatro campos son, literalmente, propiedades de las bases: la `Clasificación normativa/deóntica` de las Disposiciones (§4, Etapa 2) y `Destinatario`, `Modalidad`, `Conducta exigida` y `Condición de aplicación` de las Exigencias (Tabla ③, §4, Etapa 4). Y la comparación mecánica que promete el núcleo deóntico es la que ejecutan las seis reglas de concordancia de la etapa Agrupar (§5, Etapa 4): la Regla 3 detecta precisamente **oposición deóntica** — una obligación contra una prohibición sobre la misma conducta — algo imposible de computar si la modalidad no estuviera fijada como dato.

**Método de extracción de reglas.** La unidad del texto y la unidad de la regla no son necesariamente iguales. El Destilador recorre los artículos de la Fuente y versión encargadas tal como figuran en el `ARBOL.md` del Fragmentador; el `articulo.md` orienta sobre su estructura y los archivos de Disposición conservan el texto literal. Primero ubica enunciados que pueden expresar una posición normativa y los textos que la delimitan; luego reconstruye sujeto, modalidad, conducta y objeto, supuesto activador, condiciones, excepciones, plazo, remisiones y ámbito temporal. Decide el corte después de esa reconstrucción: mantiene juntos los componentes de una misma posición, separa conductas o efectos autónomos respaldados por el texto y evita duplicar un derecho con su deber estrictamente correlativo. Para deberes y prohibiciones, poder cumplir o infringir por separado es una prueba de control, no un criterio jurídico exclusivo; en derechos y permisos se examina si su ejercicio o aplicación tiene efectos autónomos. Una Disposición puede originar varias Exigencias, apoyar una regla ubicada en otra o no originar ninguna. **Anclaje** significa la Disposición concreta cuyo texto respalda la regla o uno de sus componentes, identificada por cuerpo, versión, identificador, localizador, archivo y función; cada Exigencia tiene un anclaje principal de su propia Fuente. Antes de crear otra ficha, el Destilador comprueba si la regla ya está documentada en esa Fuente: integra otra Disposición solo si determina esa misma regla y explica su función, sin fusionar por semejanza de palabras. Al terminar cada artículo comprueba sus filas y relaciones conocidas; al terminar toda la Fuente coteja transversalmente sus Exigencias y Disposiciones para conectar reglas, condiciones y excepciones situadas en artículos diferentes, sin repetir la extracción ni fusionar reglas autónomas. Ese control del productor no reemplaza la auditoría independiente. Una duda jurídicamente defendible se devuelve localizada. Mientras la Fuente siga en destilación, un artículo posterior puede completar una ficha anterior de la misma regla y se concilian ficha y filas con el identificador conservado. Una vez cerrada la destilación por el Orquestador, un cambio material activa la revisión de dependencias. El método aplica una lectura contextual compatible con el [art. 22 del Código Civil](https://www.bcn.cl/leychile/navegar?idNorma=172986&idVersion=2024-06-14) y usa la distinción doctrinal entre [normas permisivas, derechos y deberes correlativos](https://www.scielo.cl/scielo.php?pid=S0718-34372014000200005&script=sci_arttext). Es una regla metodológica del Laboratorio, no una fórmula de atomización ordenada por la ley.

El Destilador formula las condiciones y excepciones como **supuestos normativos**: identifica los
requisitos acumulativos y alternativos y el efecto que producirían si concurrieran, sin afirmar
que se cumplen en una actividad concreta. Para una remisión explica si aporta contenido de la
regla, elige otro régimen o señala una condición de aplicación; una referencia externa no vuelve
incompleta por sí sola la regla abstracta. Una letra que delimita la aplicación de un derecho no
se transforma por esa función en un permiso autónomo para el responsable. La operación y el
ejemplo de control del artículo 8 bis se desarrollan en la skill de examen intensivo
declarada por el `PROMPT.md` del Destilador.

***

## 2. El mapa completo de piezas

### 2.1 Las diez bases de datos de Notion

*(Hasta el 24-09-2026 eran once: la base **Prompts** se eliminó por decisión de MCF del 25-09-2026 — obligaría a los agentes a mirar AGENTS.md, luego su PROMPT.md y además una página de Notion, pasos extra sin valor. Los prompts viven solo en archivos, en la carpeta de agentes.)*

| #     | Base                       | Qué es                                                                                                                                                     | Pregunta que responde                                                                      |
| ----- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| ①     | **Fuentes**                | Cada cuerpo normativo **con su versión determinada** (Ley 19.628 consolidada, Ley 21.719, Decreto 662…)                                                    | «¿Qué textos entran al sistema y con qué autoridad?»                                       |
| ②     | **Disposiciones**          | Cada unidad normativa (artículo, inciso, numeral, letra, fragmento) **con su texto literal conservado**                                                    | «¿Qué dice exactamente el texto, dónde?»                                                   |
| ③     | **Exigencias**             | Lo que se concluyó que debe cumplirse; nace como `Candidata`, sin visado                                                                                   | «¿Qué regla concreta emerge del texto?»                                                    |
| ④     | **Agrupaciones**           | Conjuntos de Exigencias que conviene trabajar juntas en un Dominio                                                                                         | «¿Qué exigencias forman una sola cuestión de trabajo?»                                     |
| ⑤     | **Dominios**               | Áreas organizacionales (registro maestro + home de trabajo)                                                                                                | «¿Dónde de la organización se trabaja esto?»                                               |
| ⑥     | **Ítems**                  | Cuestiones jurídicas de trabajo decididas                                                                                                                  | «¿Qué hay que resolver y qué se decidió?»                                                  |
| ⑦     | **Subítems**               | Partes ejecutables con responsable, plazo y evidencia                                                                                                      | «¿Quién hace qué, para cuándo, y quién lo verificó?»                                       |
| ⑧     | **Escaladas**              | Cuestiones que el texto no resuelve (laguna, delegación, discrepancia, conflicto)                                                                          | «¿Qué no se puede decidir leyendo y hay que escalar?»                                      |
| ⑨     | **Formas de cumplimiento** | Referentes de cómo otros cumplieron (jerarquía Chile-primero)                                                                                              | «¿Cómo se ha resuelto esto antes?»                                                         |
| ~~⑩~~ | **~~Prompts~~**            | **Eliminada 25-09-2026** (ver nota sobre la tabla): los prompts viven en la carpeta de agentes, con nombre de archivo estable y fecha de cambio registrada | «¿Con qué instrucción exacta operó cada agente?» → se responde desde la carpeta de agentes |
| ⑪     | **Bitácora**               | Registro relacional de lo ocurrido                                                                                                                         | «¿Qué ha pasado?» (las páginas responden «cómo está esto»)                                 |

Los **Chats** no son una base más: hay un chat por unidad de trabajo, enlazado por URL. La disciplina de un chat por unidad es convención, no exigible por el sistema.

**Regla 3.0 (propiedad vs. contenido de página):** lo que excede dos líneas es contenido de página 🧾, no propiedad de la base. **Por qué existe esta regla:** una propiedad de Notion se muestra en una columna angosta de formulario; veinte líneas ahí son ilegibles en tabla y difíciles de leer incluso dentro de la ficha. No es una regla estética: campos largos declarados como propiedad fueron un error real de versiones anteriores que hubo que reclasificar. Sin la razón registrada, la regla parece flexible — y no lo es. Las propiedades completas de cada base están en `01-Bases-de-Datos-y-Propiedades.md`.

### 2.1.1 ⚠️ Dependencias entre bases

**Ninguna de las propiedades de esta tabla se borra, renombra, reclasifica o «depura» sin comprobar antes el impacto en lo que la consume.** Su fundamento está disperso en las secciones indicadas; la tabla lo consolida. Es la misma tabla que la sección «⚠️ Dependencias entre bases» de `01-Bases-de-Datos-y-Propiedades.md` (se mantiene en ambos por decisión de MCF del 29-09-2026 como excepción declarada a la regla de no duplicar contenido canónico; ante cualquier cambio, ambas se actualizan en la misma operación).

| #  | Propiedad o relación (base)                                                                                             | Depende de / es consumida por                                                                                                                      | Qué se rompe si se toca sin cuidado                                                            | Fundamento                                                               |
| -- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1  | **Sanción — Calificación** de Exigencias (③): `3 Gravísima / 2 Grave / 1 Leve / 0 No tipificada / Calificación variable según la conducta` | Filtra vistas y alimenta el indicador derivado **Severidad máxima** del Ítem (⑥), mediante grados fundados | Un máximo directo sobre la etiqueta omite la pluralidad y los vacíos; el resultado debe indicar si su cobertura es completa | §6.2 de este documento |
| 2  | **Texto literal** de Disposiciones (②) como bloque sincronizado                                                         | Espejos en Exigencias (③), Agrupaciones (④) e Ítems (⑥): el original vive una sola vez en ②                                                        | Convertirlo en texto plano o duplicarlo rompe la propagación del literal (documentation drift) | §8 de este documento                                                     |
| 3  | **Nivel de autoridad heredado** de Disposiciones (②)                                                                    | Rollup → Nivel de autoridad de la Fuente (①)                                                                                                       | Se pierde la herencia de autoridad sin releer cada Disposición                                 | `01-Bases-de-Datos-y-Propiedades.md` §②                                  |
| 4  | **Nivel de autoridad** de Exigencias (③)                                                                                | Fórmula de dos saltos ③→②→① (en Notion requiere `map()` sobre la relación intermedia)                                                              | La fórmula deja de computar si cambia la relación intermedia                                   | `01-Bases-de-Datos-y-Propiedades.md` §③                                  |
| 5  | **Dominio** de Exigencias (③)                                                                                           | Relación two-way con Dominios (⑤)                                                                                                                  | Romper la two-way deja Exigencias huérfanas en una sola dirección                              | `01-Bases-de-Datos-y-Propiedades.md` §③ y §⑤                             |
| 6  | **ID del registro maestro** del Dominio (⑤)                                                                             | Todas las vistas filtradas de los homes se vinculan a este ID, no a la página                                                                      | Recrear el registro cambia el ID y deja los filtros huérfanos                                  | §5 de este documento                                                     |
| 7  | **Remisiones** de Disposiciones (②)                                                                                     | Auto-relación entre Disposiciones del mismo cuerpo                                                                                                 | Perderla obliga a re-leer el corpus para reconstruir el mapa                                   | `01-Bases-de-Datos-y-Propiedades.md` §②                                  |
| 8  | **Progreso derivado** del Ítem (⑥)                                                                                      | Rollup + barra sobre Subítems (⑦); «Sin descomponer nunca 100 %»                                                                                   | Cambiar la regla del rollup falsifica el avance mostrado                                       | §6.2 de este documento                                                   |
| 9  | **Escaladas (⑧): `nace de` y `bloquea`**                                                                                | `nace de` → Exigencias (③); `bloquea` → Subítems (⑦); no son sinónimas                                                                             | Fusionarlas rompe el circuito de desbloqueo                                                    | §6.4 de este documento                                                   |
| 10 | **Enumeración contenida** de Exigencias (③)                                                                             | Regla 5 de concordancia (discrepancia de alcance) de Agrupar                                                                                       | Rellenada por rutina con «no aplica», la Regla 5 queda sin datos                               | §5 y §12.2 de este documento                                             |
| 11 | **Resultado de destilación** de Disposiciones (②)                                                                       | Cobertura del ciclo de Fuente: distingue «no examinada» de «examinada sin Exigencias»; en fase harness su asiento detallado es `Articulos/<unidad>/RESULTADO.md` del Destilador y `COBERTURA.md` resume por artículo | Sin él no hay forma de demostrar cobertura de la destilación                                   | §4 (Etapa 4) de este documento y `01-Bases-de-Datos-y-Propiedades.md` §② |
| 12 | **Disposición de anclaje** de Exigencias (③) y regla dura de anclaje                                                    | Cadena de custodia Exigencia → Disposición → Fuente/versión → documento primario                                                                   | Una Exigencia sin anclaje verificable es contenido plausible sin fuente (AI slop)              | `02-Gobernanza-y-Context-Engineering.md` §6                              |

### 2.2 Los catorce agentes

Trece agentes jurídicos más un agente de diseño. Todos operan bajo un **contrato común** (ver §3) y cada ejecución efectiva se compone de: **contrato común íntegro + contrato específico íntegro + perfil de ejecución íntegro, solo si aplica + encargo concreto**. El Orquestador verifica la recepción real. **Los agentes se nombran por su nombre, sin códigos** (los códigos «A.0»–«A.12» de documentos antiguos quedan solo como referencia histórica).

La tabla sigue el **orden de trabajo** (ciclo de Fuente → Dominio → Subítem → transversales). La columna «Activación» reemplaza a la antigua etiqueta «Nivel» (que era solo una etiqueta de este consolidado, sin injerencia en la arquitectura) y dice **qué hace que el agente entre en escena**: por turno en la secuencia de un ciclo o por **trigger** — un evento que lo gatilla en cualquier momento (una nueva versión de una Fuente, un cierre, un cambio estructural), sin turno fijo.

| Agente                                              | Activación                                  | En una frase                                                                                                                |
| --------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Orquestador**                                     | Siempre activo                              | Dirige encargos, verifica escrituras, registra el trabajo actual en `Ejecuciones/` y **es el único que mueve la etapa** de una Fuente o un Dominio; en el espacio de datos, la Bitácora cumple la función relacional |
| **Fragmentador de Fuentes**                         | Secuencia · ciclo de Fuente                 | Ingresa, inventaría y fragmenta una Fuente en Disposiciones fieles al texto                                                 |
| **Destilador de Exigencias**                        | Secuencia · ciclo de Fuente                 | Examina cada Disposición y extrae Exigencias candidatas                                                                     |
| **Auditor de anclaje**                              | Secuencia · ciclo de Fuente                 | Revisa con contexto separado; veredictos VERIFICADA / CORREGIBLE / ESCALAR A HUMANO                                         |
| **Analista de impacto de Fuente**                   | Trigger · resultado anterior potencialmente afectado | Devuelve la detección al Orquestador; tras autorización humana para analizar, produce el mapa de impacto; no implementa |
| **Delimitador de Dominio**                          | Secuencia · ciclo de Dominio                | Examina las Fuentes conocidas, propone alcance y preguntas de diagnóstico, interpreta las respuestas sin inventar hechos; el humano decide las fronteras |
| **Detector de concordancias**                       | Secuencia · ciclo de Dominio (dos pasadas)  | Dos modos: correspondencia normativa (Investigar) y concordancias con pase ciego (Agrupar)                                  |
| **Relator de Agrupación**                           | Secuencia · ciclo de Dominio (dos pasadas)  | Dos modos: contraste independiente (Investigar) y relato de Agrupación (Agrupar); reúne evidencia, no dictamina             |
| **Investigador de Formas de cumplimiento**          | Secuencia · ciclo de Subítem                | Busca referentes con jerarquía Chile-primero; nada jurídico se funda en fuente extranjera                                   |
| **Opciones de resolución y examen de antecedentes** | Trigger · hallazgo/duda encaminada          | Mínimo dos opciones defendibles por Escalada; prohibido «recomiendo»                                                        |
| **Relator**                                         | Trigger · cierre de formulación o etapa     | Documenta formulaciones y cierres volviendo a la evidencia; no compila resúmenes                                            |
| **Agente del Manual**                               | Trigger · cambio en reglas o flujo          | Mantiene las instrucciones de uso del sistema                                                                               |
| **Agente de Arquitectura**                          | Trigger · cambio estructural solicitado     | Especifica y comprueba cambios estructurales; guardián del versionado                                                       |
| **Agente de Diseño del espacio**                    | Trigger · cambio de presentación autorizado | Cambios de presentación autorizados; efectos funcionales pasan por Agente de Arquitectura                                   |

*Trigger = evento que gatilla al agente (no tiene turno fijo en una secuencia): una nueva versión de Fuente, un cierre que documentar, un cambio estructural o de presentación. Los agentes de secuencia entran cuando el ciclo llega a su etapa.*

Hay etapas deliberadamente **sin un agente especialista que sustituya el juicio o la acción humana**: Diagnosticar, Comparar, Preparar/Implementar/Evidenciar y decidir sobre una Agrupación. En Diagnosticar, el Delimitador prepara las preguntas y examina las respuestas para revisar sus propuestas de alcance; el Orquestador las transmite y registra fielmente; solo las personas aportan o confirman hechos de la organización.

**Por qué no se delega el juicio a otro agente** (registrado para que nadie agregue uno sin conocer el motivo): **Diagnosticar** requiere acceso a la realidad de la organización — saber qué cookies instala el sitio exige inspeccionarlo y preguntarle a personas, no leer la ley. El Delimitador puede preparar preguntas y localizar efectos de las respuestas sobre el alcance, pero no verificar por sí mismo los hechos ni reemplazar el levantamiento humano o técnico. El Orquestador conserva una sola interfaz de comunicación con la persona sin asumir el análisis sustantivo. **Comparar**, estando el estándar y el diagnóstico en campos estructurados, es una vista filtrada: un agente ahí agrega riesgo de alucinación sin agregar capacidad. **Preparar, Implementar y Evidenciar** reservan la ejecución o comprobación decisiva a personas según la gobernanza interna del Laboratorio; el art. 8° bis no impone por sí mismo un visado humano de estas etapas. **Decidir sobre una Agrupación** es ponderación humana, no comparación de campos.

### 2.3 Los ciclos y etapas

Esta sección es el **mapa**; el detalle operativo de cada ciclo sigue en §4–§7. Los ciclos son: **Fuente**, **Dominio** (Agrupación e Ítem son estados dentro de él) y **Subítem** (ciclo aparte); la **Escalada** y la **Revisión por cambio** son transversales y pueden nacer en cualquier etapa. `(*)` = agente transversal que puede intervenir en ese punto, activado por trigger (evento), sin turno fijo.

**Ciclo de Fuente** (8 etapas):

`Ingresada → En fragmentación → Fragmentada → En destilación → Destilada → En auditoría → Auditoría completada → Lista para uso en Dominio`

| Etapa/estado         | Quién trabaja             | Qué ocurre                                                                                | Qué se entrega                                                               |
| -------------------- | ------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Ingresada            | Orquestador               | Se registra la Fuente con su documento primario y versión                                 | Fuente registrada con identificación completa                                |
| En fragmentación     | Fragmentador de Fuentes   | Inventario del cuerpo normativo y fragmentación en Disposiciones fieles al texto          | Archivos de Disposiciones con texto literal y control de ingreso             |
| Fragmentada          | Orquestador               | Verifica escritura real y cobertura del cuerpo                                            | Transición aplicada; Disposiciones disponibles                               |
| En destilación       | Destilador de Exigencias  | Examina cada Disposición y extrae Exigencias candidatas                                   | Exigencias candidatas ancladas a su Disposición                              |
| Destilada            | Orquestador               | Verifica cobertura de la destilación                                                      | Transición aplicada; Exigencias listas para auditoría                        |
| En auditoría         | Auditor de anclaje        | Revisión con contexto separado; veredictos VERIFICADA / CORREGIBLE / ESCALAR A HUMANO     | Veredictos por Exigencia; correcciones encargadas si procede                 |
| Auditoría completada | Orquestador               | Cierre técnico del examen completo, aunque persistan hallazgos con ruta pendiente visible | Fuente con auditoría documentada; todavía no se presume apta para Dominio  |
| Lista para uso en Dominio | Orquestador          | Comprueba que no quedan hallazgos o datos materiales pendientes y que las correcciones fueron reauditoradas | Fuente y versión aptas como insumo técnico auditado para el ciclo de Dominio |

**Ciclo de Dominio** (5 etapas; Agrupación e Ítem son estados dentro de él):

`Delimitar → Diagnosticar → Investigar → Agrupar → Decidir`

| Etapa/estado               | Quién trabaja                                                   | Qué ocurre                                                                                  | Qué se entrega                                    |
| -------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Delimitar                  | Delimitador de Dominio + humano                                 | Examina todas las Fuentes conocidas; propone fronteras y aplicabilidad por Fuente y versión; el humano decide cuando hay base suficiente | Fronteras decididas o pendientes identificadas y alcance de Fuentes trazable |
| Diagnosticar               | Delimitador de Dominio + Orquestador + humano                  | Delimitador prepara preguntas y revisa sus propuestas con las respuestas; Orquestador pregunta y registra; la persona aporta hechos y evidencia | Diagnóstico, lagunas y fronteras afectadas registrados |
| Investigar                 | Detector de concordancias + Relator de Agrupación               | Correspondencia normativa y contraste independiente                                         | Evidencia de correspondencias                     |
| Agrupar                    | Detector de concordancias (pase ciego) + Relator de Agrupación  | Propuesta de Agrupaciones y relato que reúne evidencia, sin dictaminar                      | Agrupaciones propuestas y relatadas               |
| Decidir                    | humano; Relator (\*)                                            | El humano decide sobre Agrupaciones e Ítems («es ponderación, no comparación»)              | Decisiones registradas; Relator documenta cierres |
| ↳ estados de la Agrupación | Detector propone → Relator de Agrupación relata → humano decide | Propuesta → Relatada → Decisión → Promoción (cuando procede)                                | Agrupación con decisión y fundamento              |
| ↳ estados del Ítem         | humano decide; Relator (\*) documenta                           | Propuesto / Validado / Descartado / Fusionado (cuatro estados de decisión, no secuenciales) | Ítem con decisión fundamentada                    |

**Ciclo de Subítem** (8 etapas, una fila por etapa):

Delimitar → Estándar → Diagnosticar → Comparar → Decidir (si procede) → Preparar → Implementar → Evidenciar

| Etapa/estado         | Quién trabaja                                                 | Qué ocurre                                                                                                                                                | Qué se entrega                                                                     |
| -------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Delimitar            | humano (sin agente)                                           | Se delimita la manifestación concreta del Ítem y se **declara el criterio de cierre al abrir**                                                            | Subítem abierto con manifestación y criterio de cierre                             |
| Estándar             | Investigador de Formas de cumplimiento                        | Busca referentes con jerarquía Chile-primero (① norma chilena ② instrucción/dictamen de la Agencia ③ estándar técnico/comparado «no vinculante en Chile») | Referentes consultados (`Formas consultadas`)                                      |
| Diagnosticar         | humano (sin agente)                                           | Ponderación de la brecha entre el estándar y la situación                                                                                                 | Diagnóstico del Subítem                                                            |
| Comparar             | humano (sin agente)                                           | Comparación de las formas de cumplimiento posibles                                                                                                        | Comparación registrada                                                             |
| Decidir (si procede) | humano; Opciones de resolución y examen de antecedentes (\*)  | Si hay duda genuina, se examinan antecedentes y se proponen mínimo dos opciones defendibles; el humano decide                                             | Decisión con fundamento, o Escalada vinculada                                      |
| Preparar             | humano (sin agente)                                           | Se prepara lo necesario para ejecutar                                                                                                                     | Preparación completada                                                             |
| Implementar          | humano (sin agente); puede quedar `Bloqueado por dependencia` | Ejecución de la forma decidida                                                                                                                            | Subítem `Implementado`                                                             |
| Evidenciar           | persona **distinta** del responsable verifica; Relator (\*)   | Se aporta la evidencia de ejecución («no es el documento redactado: es la prueba de que opera») y se verifica                                             | Subítem `Verificado` con evidencia y `Verificado por`; Relator documenta el cierre |

**Escalada (transversal; puede nacer en cualquier etapa de cualquier ciclo):**

`Detectada → Opciones propuestas → Decidida → Superada o desbloqueada` *(puede nacer en cualquier etapa de cualquier ciclo)*

| Etapa/estado            | Quién trabaja                                                 | Qué ocurre                                                                                                              | Qué se entrega                                     |
| ----------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Detectada               | agente que detecta; Opciones examina; Orquestador registra    | Hallazgo localizado → examen independiente de texto y antecedentes → expediente creado o vinculado si persiste duda genuina | Ficha de Escalada o vínculo a una existente |
| Opciones propuestas     | Opciones produce; Orquestador comprueba y mueve etapa         | Informe con al menos dos opciones defendibles (consecuencia, riesgo, reversibilidad); prohibido «recomiendo» | Opciones propuestas verificadas; sin decisión humana |
| Decidida                | humano                                                        | El humano elige y funda la decisión                                                                                     | Decisión registrada con fundamento                 |
| Superada o desbloqueada | Orquestador; Relator (\*)                                     | Cierre del bloqueo o sustitución                                                                                        | Escalada cerrada; Relator documenta el cierre      |

**Revisión por cambio (transversal; expediente por cambio, no por Dominio):**

`Detectada → En análisis → Impacto evaluado → En revisión → Comprobada → Cerrada`,
con salida `Cerrada sin impacto` tras examen suficiente. Una detección nueva
puede afectar varias Fuentes, Dominios y entregas. El Orquestador pregunta directamente a
la persona si autoriza **iniciar el análisis de impacto** antes de encargar el
mapa; el Analista devuelve la detección al Orquestador y no pregunta ni
despacha por su cuenta. Tras el mapa, una segunda autorización humana fija
el alcance de las correcciones. La revisión conserva un expediente propio;
cada Dominio afectado mantiene su etapa y vuelve a la primera fase que deba
reexaminarse. El detalle y las condiciones de cierre están en §7.

**Notas de diseño importantes:**

* `Integrada` se **eliminó** del ciclo de Fuente; `Superada` dejó de ser etapa y pasó a ser una relación de sustitución normativa.

* El ciclo de Dominio **no tiene sexta etapa**: no existe `Implementar` como columna del Dominio; la ejecución continúa visible tras el cierre.
* `Reabierto por cambio normativo` no es valor de `Etapa del ciclo` del Dominio: la revisión por cambio tiene expediente y estados propios, y enlaza los Dominios afectados.

* Las cuatro decisiones de una Agrupación (sostener / no sostener / dividir / fusionar) **no son cuatro columnas** que cada Agrupación deba atravesar.

* `Auditoría completada` acredita el examen técnico completo, pero **no** aptitud automática para uso en Dominio. `Lista para uso en Dominio` acredita aptitud como insumo técnico auditado; ninguna de las dos etapas significa Exigencias visadas, aplicabilidad a un Dominio concreto ni cumplimiento empresarial.

### 2.4 El circuito universal de trabajo

Todo encargo sigue el mismo circuito:

```
humano o evento → Orquestador encarga → agente ejecutor → devolución estructurada al Orquestador
→ Orquestador encarga revisión → agente revisor → devolución al Orquestador → Orquestador aplica transición (si corresponde)
```

Reglas del circuito:

* **«No basta "listo".»** Toda devolución es estructurada, con resultado `completo / parcial / bloqueado / requiere decisión`, objetos creados/modificados/reutilizados, comprobaciones, hallazgos, decisiones humanas necesarias y fecha/hora reales.

* Orquestador **verifica la escritura real** (relee desde Notion) antes de aplicar cualquier transición. Un «terminé» en un chat no mueve nada.

* **Un fallo técnico de acceso NUNCA es un descarte jurídico.** No se traduce en `Descartada`.

* Reintentos: máximo 3 técnicos con espera incremental; máximo 2 rondas sustantivas tras la primera auditoría (configurable en el perfil; una ronda extra nunca transforma un error en aprobación).

***

## 3. El contrato común y la anatomía de un encargo

### 3.1 Contrato común (lo que todo agente recibe siempre)

Sus secciones: identidad e instrucciones; significado de los trabajos y los estados; Dominio/Ítem/ejecución; handoff, contexto separado y conservación de versión; trabajo completo y contexto normativo; escritura, identidad y versiones; hallazgos y enrutamiento; registro proporcionado y entrega; presentación y advertencias. El texto completo está en el `AGENTS.md` de la carpeta de agentes (Parte II — Contrato común).

**Salidas del harness:** cada `PROMPT.md` declara el esquema mínimo de su carpeta y los archivos que ese rol produce. El especialista reutiliza el expediente de la Fuente, Dominio o encargo al continuar, enlaza resultados existentes y no abre un documento por cada hallazgo, alternativa o avance. El Orquestador conserva sus registros breves en `Ejecuciones/` y los expedientes de dudas jurídicas en `Escaladas/`; no duplica informes de agentes. Los nombres entre ángulos de un esquema son marcadores de posición, no carpetas literales. Cualquier otro destino escribible requiere un encargo expreso y debe permanecer dentro de `planificacion/` durante esta fase.

### 3.2 Recepción obligatoria (lo que Orquestador entrega al encargar)

Encargo ID, ciclo/etapa, rol y ruta más huella o versión comprobable del prompt, arquitectura y perfil vigentes, entradas identificadas, operaciones autorizadas, objetos escribibles, criterio de terminación, evidencia esperada, checkpoint, modo y contexto excluido, ID de registro maestro, elegibilidad de entradas, revisión posterior exigida y decisiones humanas pendientes.

### 3.3 Devolución obligatoria (lo que el agente devuelve al Orquestador)

Resultado (`completo / parcial / bloqueado / requiere decisión`), alcance examinado, versiones usadas, objetos creados/reutilizados/modificados, comprobaciones hechas, hallazgos, dependencias afectadas, decisiones humanas necesarias, relecturas, checkpoint de reanudación si quedó trabajo abierto — ruta, última unidad comprobada, pendientes, impedimento, siguiente acción y responsable — o `Cerrado; sin reanudación pendiente`, informe, transición solicitada, advertencias y fecha/hora reales. El checkpoint se conserva en el producto y se enlaza desde `Ejecuciones/`; no exige un archivo nuevo por agente.

**Marcas de procedencia y estado en toda salida de agente** (regla operativa en el `AGENTS.md` de la carpeta de agentes): 🤖 identificar agente productor y `PROMPT.md` usado; el Orquestador registra ruta, fecha real y huella o versión comprobable del contenido exacto, sin inventar una marca `v[n]`. ⏳ Una salida técnica se presenta como «Propuesta pendiente de comprobación técnica» hasta que el Orquestador comprueba su escritura y cobertura en el destino y registra el resultado; una propuesta que requiere decisión jurídica humana se presenta como «Propuesta sin visar» hasta esa decisión. La comprobación técnica no constituye visado jurídico: puede cerrar una etapa de Fuente y versión sin visar su nivel de autoridad; una Exigencia sigue `Candidata` hasta el visado humano; relatar una Agrupación no la sostiene ni aprueba la formulación del Ítem. ✍️ **Campo de decisión humana:** cuando la salida requiere que una persona decida, incluye un espacio reservado y vacío, de escritura exclusiva del validador, que el agente nunca pre-llena (ni «para ahorrar tiempo»: un visado sobre texto pre-redactado por el agente degrada la decisión a confirmación, la forma blanda de la inversión del art. 8° bis). El campo ✍️ es un bloque del cuerpo de la página (o del archivo, en el harness), nunca una propiedad de la base: una decisión con fundamento es texto largo (Regla 3.0) y el bloque visible deja claro quién escribió.

**Convención REGLA / HECHOS / CUESTIÓN:** toda ejecución sustantiva de un agente abre declarando la regla aplicable, los hechos disponibles y la cuestión concreta a resolver, antes de razonar. Viene de la Propuesta-Spec v6 (origen: Chain of Logic) con impacto medido: quitarla cuesta 25,9 puntos porcentuales de exactitud. Se perdió inadvertidamente al reescribir los prompts en el formato actual; se restaura como regla común en el `AGENTS.md` de la carpeta de agentes (que se inyecta íntegro a cada agente — es el lugar único correcto, sin duplicarla en cada prompt).

### 3.4 Canon y testeo: la frontera que no se cruza

* **Canon** (este documento y sus hermanos 01 y 02): ciclos, papeles, evidencia, retorno al Orquestador y reglas de decisión. Es lo permanente.

* **Testeo y corridas** (documento aparte, `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`): compuertas C0–C6, excepciones E-01/E-02, perfiles de implementación (`i0.x`) y todo permiso experimental. Es lo temporal y revisable.

La regla de separación, textual de la especificación consolidada: «Los ciclos, papeles, evidencia, retorno al Orquestador y reglas de decisión pertenecen a la arquitectura canónica. Las compuertas de la corrida, permisos experimentales y excepciones pertenecen a un perfil de implementación y testeo separado.» **No existe una etapa canónica `Cerrada en testeo`.** Nada de lo canónico depende de una compuerta, y ninguna compuerta cambia el significado de una etapa.

***

## 4. Ciclo de Fuente, etapa por etapa

Unidad ordinaria de trabajo: **el artículo completo**. (Se retiró el umbral de cinco artículos como excepción automática.)

### Etapa 1 — Ingresada

**Quién actúa:** el humano incorpora la Fuente (carga humana, vigilancia normativa o documento en chat); Orquestador registra el encargo al Fragmentador de Fuentes.

**Tabla ① Fuentes — propiedades que se escriben aquí:** Nombre · Tipo de fuente · Jurisdicción · Fecha de publicación · Estado de vigencia · Enlace oficial · Acceso al texto · Nota de acceso · Vía de ingreso · Quién la incorporó · Qué la originó · Etapa del ciclo = `Ingresada`.

**Regla dura de anclaje:** nada se cita como fundamento si no existe en Fuentes con **nivel de autoridad asignado por humano**. Material de chat entra como `Sin calificar` y no puede anclar Exigencias mientras lo sea. En testeo (E-01) se admite nivel propuesto sin visar, nunca `Sin calificar`.

**Escrutinio graduado por vía de ingreso.** La verificación de una Fuente es siempre humana, pero el nivel de escrutinio varía según cómo entró — y la razón es el problema que evita: un documento pegado en un chat puede ser una reproducción alterada, un borrador o una versión derogada, mientras una publicación detectada en la fuente oficial tiene procedencia casi garantizada. Si ambas recibieran el mismo escrutinio, una Fuente de chat mal verificada podría terminar anclando Exigencias, y todo lo destilado de ella heredaría el vicio.

| Vía de ingreso       | Escrutinio                                                                            |
| -------------------- | ------------------------------------------------------------------------------------- |
| Vigilancia normativa | **Bajo** — procedencia oficial; comprobar enlace y vigencia                           |
| Agente investigador  | **Medio** — comprobar que el enlace es oficial, no una reproducción                   |
| Carga humana         | **Medio** — mismo criterio                                                            |
| Documento en chat    | **Alto** — única vía sin control de origen: verificar autoría, oficialidad y vigencia |

### Etapa 2 — En fragmentación (Fragmentador de Fuentes, Fragmentador de Fuentes)

**Qué hace Fragmentador de Fuentes, muy definido:**

1. **Inventaría toda la Fuente antes de fragmentar**: crea `ARBOL.md` con el árbol completo de artículos ordinarios, intercalados (bis, ter), transitorios y, bajo cada artículo, incisos, numerales, letras, enumeraciones y excepciones — con estados `[pendiente] / [parcial] / [completo]` válidos **solo para fragmentación**.
2. **Prepara los archivos del artículo**: una carpeta por artículo, con `articulo.md` estructural cuando no tenga texto literal propio y archivos para las unidades efectivamente presentes (incisos, numerales, subnumerales, letras, fragmentos u otras estructuras del cuerpo). Una unidad madre con texto literal propio también puede ser Disposición aunque tenga hijas.
3. **Lee el artículo completo antes de decidir sus cortes** y escribe cada Disposición con sus campos obligatorios (ver abajo).
4. **Comprueba y entrega al Orquestador**: reconstruye la cobertura desde los archivos, la compara con el artículo entero y escribe el informe global de fragmentación. Devuelve juntos el informe, `ARBOL.md`, `FUENTE.md` y la identificación del documento primario, con límites y pendientes localizados. El Orquestador comprueba esa entrega antes de mover la etapa técnica.

**Qué entrega:** las Disposiciones (en el harness, archivos `.md`; en Notion, fichas con callout ⚖️ `Texto literal` en bloque sincronizado, quote exterior y toggles `Localización y versión`, `Control de ingreso`, `Exigencias asociadas`), el inventario acumulativo por Fuente y el informe enlazado desde `Ejecuciones/` por el Orquestador; en el espacio de datos, desde la Bitácora.

**Límites del rol:** no extrae Exigencias, no audita su propio trabajo, no decide aplicación a un Dominio.

**Tabla ② Disposiciones — propiedades que se escriben aquí:** Identificador (título con localizador exacto) · Fuente (relación) · Texto literal (bloque sincronizado; **vive una sola vez, aquí**) · Tipo de norma (lista cerrada de cinco valores — minuta 7 en `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/Minutas-de-decision-2026-09-29.md`) · Clasificación normativa/deóntica (restringida a normas regulativas — minuta 7) · Remisiones (auto-relación) · `Resultado de destilación` = `Pendiente` (decisión de la especificación consolidada). *(25-09-2026: eliminadas `N.º de ingreso`, `Lote` y `Clave de orden normativo` por decisión de MCF — sobrecomplejizaban; ver 02.)*

> *(Desfase D-01 — resuelto: corregido el 29-09-2026 y visado el 30-09-2026 (minuta 7); el prompt vigente del Fragmentador de Fuentes ya incorpora la corrección y la taxonomía en dos ejes. Diagnóstico histórico en `/Users/mcfoix/Desktop/Gestion del Caos/informes/04-Diagnosticos-y-Desfases.md`.)*

### Etapa 3 — Fragmentada

Orquestador verifica el informe global de fragmentación y la cobertura desde el primario («contar fichas creadas no demuestra que se cubrió la Fuente») y mueve la Fuente a `Fragmentada`. En la página de la Fuente queda el **inventario de cobertura**: tabla acumulativa con cinco columnas — Unidad esperada | Fragmentación | Destilación | Auditoría | Detalle y evidencia — una fila por artículo, cada celda `Pendiente / Parcial / Completa`.

### Etapa 4 — En destilación (Destilador de Exigencias, Destilador de Exigencias)

Si una Fuente nueva, versión nueva o corrección material puede alterar
resultados anteriores, se abre o vincula la Revisión por cambio de §7.3.
El Analista devuelve una alerta localizada; el Orquestador pregunta
directamente a la persona si autoriza iniciar el análisis de impacto y
registra su respuesta. Solo tras esa autorización fija el inventario de
productos anteriores y encarga el mapa cuando existan o no pueda comprobar
su ausencia. Una Fuente nueva puede afectar entregas que aún no la citan;
una falta de enlaces no acredita ausencia de impacto. La autorización de
revisión no sustituye las condiciones del ciclo ordinario de Fuente ni lo
bloquea por sí misma. El mapa se obtiene antes de corregir resultados
anteriores; el Analista analiza y no implementa esas correcciones.

**Qué hace Destilador de Exigencias, muy definido:**

1. **Prepara la Fuente y sus resultados**: antes de iniciar, comprueba que todos los artículos y unidades declaradas de esa Fuente y versión figuren `[completo]` en `ARBOL.md` y que sus archivos existan y se abran. El árbol es el inventario de entrada; la salida se organiza en `Resultados/<fuente-y-version>/`. Su `COBERTURA.md` resume un artículo o unidad equivalente de primer nivel por fila, con enlace y conteos. Cada `Articulos/<unidad>/RESULTADO.md` conserva una sola fila por Disposición de ese artículo. Si el artículo extenso contiene subunidades declaradas en `ARBOL.md` y sus filas dificultan la consulta, crea subíndices para esas subunidades: el resultado del artículo conserva sus filas directas y enlaza los subíndices, sin repetir las filas de éstos. Por ejemplo, puede haber un resultado por numeral dentro del artículo primero de la Ley 21.719.
2. **Extrae sin perder el sentido jurídico**: recorre los artículos de la Fuente y versión indicadas en el encargo en el orden de su `ARBOL.md`, examina cada Disposición con el artículo completo y conecta desde esta etapa las definiciones, excepciones y remisiones pertinentes de otros artículos de esa misma Fuente. Recibe íntegros en toda ejecución los métodos de las skills obligatorias declaradas en su `PROMPT.md`; el examen intensivo se aplica cuando dos lecturas cambian materialmente el resultado o antes de registrar o mantener `Examen incompleto`, no por cada remisión rutinaria; el método sancionatorio se aplica a toda ficha creada o revisada y se comprueba para todas las fichas al cotejar la Fuente, antes de decidir el valor de `sancion`. Aplica el método de §1.2; una Exigencia expresa **una sola regla normativa** (obligación, prohibición, derecho del titular, permiso o permiso condicionado), con sus condiciones y excepciones. No convierte una definición aislada en obligación, ni un permiso en deber sin apoyo en el texto literal. Una Disposición puede producir varias Exigencias, compartir una con otras, o no producir ninguna.
3. **Escribe una Exigencia por archivo** en `Resultados/<fuente-y-version>/Exigencias/`, con sus campos (ver tabla abajo). `EX-NNN` es un número local: la identidad completa que recibe cualquier otro agente es `<fuente-y-version>/EX-NNN`. «No inventes un plazo, sanción, destinatario o relación para llenar un campo.»
4. **Revisa el conjunto y entrega** al Orquestador: coteja `ARBOL.md` y el texto literal de todas las Disposiciones con sus filas de resultado, incluidas las `Examinada sin Exigencias`; después revisa transversalmente fichas y anclajes de esa Fuente para detectar condiciones, excepciones, remisiones o reglas entre artículos omitidas y duplicaciones. Tras recorrer todos los artículos y conciliar cobertura, filas y fichas, emite `INFORME-DESTILACION.md` **antes de la devolución al Orquestador**, no al cerrar cada artículo. Si completó el recorrido con filas incompletas, el informe expresa un resultado parcial y sus impedimentos; si una interrupción impidió terminar el recorrido, informa el avance al Orquestador y pospone el informe global hasta poder hacer el cotejo transversal. Tras una corrección, actualiza el mismo informe luego de repetir los controles afectados. Su estructura fija es: resultado y alcance; método y controles con evidencia; cortes y relaciones relevantes; cotejos con otras Fuentes cuando existieron; hallazgos, límites y pendientes; cierre técnico. El informe explica y enlaza las fichas existentes; no vuelve a extraerlas, no las fusiona ni crea Agrupaciones de Dominio.

**Resultado posible por Disposición** (propiedad `Resultado de destilación`): `Pendiente / Examen incompleto / Examinada con Exigencias / Examinada sin Exigencias`. `Pendiente` significa que el Destilador todavía no examinó la Disposición; solo después de leerla, reconstruir las reglas que integra y determinar su función registra uno de los otros tres resultados. Esta operación es distinta de asignar `Tipo de norma` y `Clasificación deóntica`, que corresponde al Fragmentador, y no acredita que una condición se cumpla en un caso concreto. Regla clave: «Una relación vacía no permite distinguir "no examinada" de "examinada sin Exigencias".» En el harness, el asiento es una fila única por Disposición en `Articulos/<unidad>/RESULTADO.md`, con cinco columnas estables: Disposición enlazada, resultado, Exigencias originadas, Exigencias apoyadas y función, motivo breve. `COBERTURA.md` agrega solo el avance por artículo. El desarrollo jurídico de la regla vive en la ficha enlazada, sin duplicarlo en la tabla; el razonamiento específico de una Disposición que no se entienda en el motivo breve, incluida una que carezca de ficha, se conserva debajo de la tabla en el mismo `RESULTADO.md`. Antes de mantener `Examen incompleto`, el Destilador desarrolla bajo esa tabla el examen intensivo de la skill, con cuestión, pasajes, lecturas si existen, componente faltante y conclusión fundada; el Orquestador comprueba su presencia y trazabilidad, sin visar la conclusión. El Destilador usa `Tipo de norma` y `Clasificación deóntica` recibidos del Fragmentador como datos de entrada. Durante la extracción de una regla localizada, si un dato de origen falta, queda fuera del vocabulario, es incompatible con el otro campo o impide cerrar la regla sin sustituirlo, registra `Examen incompleto` y el impedimento localizado en `RESULTADO.md`: campo y valor recibidos, operación impedida y dato que requiere revisión. El Orquestador encarga al Fragmentador revisar el origen y luego dispone la reanudación del examen. Las reglas independientes pueden avanzar sin cerrar la fila impedida. El Orquestador concilia árbol, filas, fichas e informe antes de cerrar técnicamente la destilación; la auditoría de omisiones es posterior e independiente.

**Ley modificatoria y ley consolidada.** Si el corpus contiene una ley modificatoria y
la ley consolidada de la ley modificada para el mismo período, cada cuerpo y versión
conserva sus Disposiciones, fichas y cobertura. El Orquestador identifica las
disposiciones correspondientes por instrucción de cambio, destino, localizadores y
vigencia; registra también las que no tienen pareja. Para cada par encarga primero
la lectura de la ley consolidada y después la lectura de la ley modificatoria, en
contextos separados. Cada primera lectura formula la regla desde el texto de su
propia Fuente, sin recibir razonamientos anteriores sobre esa regla ni los de la
otra Fuente; si existió exposición previa, se declara y no se presenta esa
lectura como independiente. El Orquestador conserva las dos entregas antes de
revelar los resultados recíprocos y encargar el cotejo de los textos y las
fichas en ambos sentidos. Este orden organiza el trabajo: no da
prioridad automática a una interpretación ni autoriza copiar etiquetas.

En este corpus, una instrucción de la Ley 21.719 se examina por su función
modificatoria y el artículo que reproduce puede originar Exigencias de esa ley.
El texto incorporado origina fichas propias de la Ley 19.628 consolidada desde
01-DIC-2026, referencia del régimen integrado que se pretende implementar para
ese período. Los transitorios y demás efectos propios de la Ley 21.719 se examinan
por separado aunque no tengan pareja en la Ley 19.628 consolidada. Para el mismo
pasaje y período, las dos fichas aplican los mismos criterios de clasificación:
una diferencia necesita una causa textual, temporal o contextual identificada,
con su efecto, o queda pendiente. Dos explicaciones individuales plausibles no
cierran el cotejo. Una coincidencia literal tampoco prueba por sí sola identidad
de todas las condiciones ni crea dos deberes organizacionales. Si persiste una
duda jurídica material, sigue el circuito de decisión humana; el cotejo no
sustituye la auditoría independiente ni la comparación posterior en Dominio.
El Auditor conserva primero su mapa independiente de una sola Fuente; en su
segundo pase comprueba también la correspondencia y las diferencias del par
desde los dos textos primarios, sin trasladar el veredicto de una Fuente a la
otra ni decidir una controversia jurídica reservada. Cada Fuente conserva su
cierre técnico por cobertura propia, pero una diferencia
material abierta impide presentar el par como resultado conciliado apto para
uso posterior. El `PROMPT.md` del Destilador y el del Orquestador fijan el
procedimiento y los registros.

Antes de usar un piloto como patrón de redestilación, el Orquestador comprueba
que se preservaron ambas primeras lecturas, que el mapa de correspondencias y
vigencias está completo para su alcance, que cada diferencia tiene conclusión
fundada o pendiente con efecto visible, y que las garantías y enlaces sobreviven
a la corrección y auditoría independiente. El piloto del artículo 8 bis se
contrasta además con otro par real que tenga una remisión o condición temporal.
Esta prueba del método no declara lista una Fuente cuya cobertura o auditoría
general permanezca abierta ni abre por sí sola una etapa de Dominio.

**Tabla ③ Exigencias — propiedades que se escriben aquí** (la Exigencia nace como `Candidata`, sin visado: el valor inicial del campo `Estado` lo fija el sistema al crear la ficha; el Destilador no lo escribe — por eso `Estado` no está en esta tabla ni en su esqueleto YAML):

| Campo                          | Contenido                                                                                                                                                            |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identificador                  | `<fuente-y-version>/EX-018`; `EX-018` solo es local a la carpeta de esa Fuente                                                                                      |
| Enunciado                      | la regla en una frase                                                                                                                                                |
| Destinatario                   | Responsable de datos / Encargado del tratamiento / Titular / Agencia / Delegado de protección de datos / Tercero                                                     |
| Modalidad                      | Obligación / Prohibición / Permiso / Permiso condicionado / Derecho del titular (una por Exigencia)                                                                  |
| Conducta exigida               | la conducta atómica                                                                                                                                                  |
| Condición de aplicación        | con estructura Y/O («A O (B Y C)»)                                                                                                                                   |
| Plazo                          | valor + día Corridos/Hábiles/No aplica + prorrogable No/Una vez/Más de una vez/No determinado                                                                        |
| Disposición de anclaje         | múltiple, con la función de cada una                                                                                                                                 |
| Cita textual de respaldo       | del literal                                                                                                                                                          |
| Agrupaciones candidatas        | legítimamente vacía en extracción                                                                                                                                    |
| Estado de determinación        | Determinada / Delegada / Indeterminada; sin valor por defecto. Ver regla bajo la tabla.                                                                             |
| Enumeración contenida          | si la hay                                                                                                                                                            |
| Carácter                       | Obligatoria / Condicional / Transversal                                                                                                                              |
| Sanción                        | etiqueta única para filtrar: `3 Gravísima / 2 Grave / 1 Leve` con disposición tipificadora y vínculo razonado; `0 No tipificada` tras examen negativo fundado; `Calificación variable según la conducta` cuando se fundaron calificaciones distintas (`0`, `1`, `2` o `3`) para conductas comprendidas en la misma Exigencia; vacío solo si el examen o una decisión material siguen pendientes. La ficha explica cada vía. Multa y accesorias solo si constan. |

**Determinación y forma.** Una remisión es la referencia expresa a otra disposición, norma o instrumento. El Estado de determinación se asigna tras leer los textos necesarios: `Determinada` si fijan los elementos esenciales, incluso cuando la remisión solo conduce a contenido normativo ya fijado y examinado; `Delegada` si el propio texto atribuye expresamente a otra autoridad o instrumento la concreción de un elemento esencial, aunque el instrumento ya exista; `Indeterminada` si el texto deja un concepto abierto que requiere valoración jurídica. Si, tras analizar la función de una remisión, su contenido resulta indispensable para formular un componente de la regla y ese texto no puede leerse, la Disposición afectada queda en `Examen incompleto`: no se añade otro valor de determinación ni se elige uno por defecto. La mera referencia externa o la falta de un caso concreto que satisfaga una condición no bastan para ese resultado. Si la norma exige expresamente una forma de cumplimiento, se conserva en la conducta, la condición y el anclaje de la Exigencia según corresponda. La manifestación concreta y el criterio de cierre se fijan al abrir el Subítem; el Investigador de Formas de cumplimiento solo aporta referentes para orientar esa decisión.

**Por qué tres de estos campos existen — el fundamento que no debe perderse:**

* **Plazo (desglosado).** Sin el desglose (valor / tipo de día / prórroga), el contraste entre el plazo de treinta días corridos, prorrogable por una vez hasta treinta días corridos, para pronunciarse sobre la solicitud (art. 11 inc. 2), y el plazo de dos días hábiles para responder al requerimiento de bloqueo (art. 11 inc. 6) es invisible. El texto literal del inciso sexto no califica expresamente este último plazo como «no prorrogable»; ese valor no se afirma por inferencia. Confundir corridos con hábiles es **error material** — por eso el Auditor lo verifica como punto aparte.

* **Enumeración contenida.** Es el campo que hace posible la **Regla 5** (discrepancia de alcance, ver §5 etapa Agrupar): si dos Exigencias traen transcrita su lista cerrada y las listas sobre la misma materia no coinciden, la discrepancia se detecta mecánicamente — el caso real: el art. 4° enumera seis derechos del titular y el art. 14 ter letra f) enumera cinco. Si el campo se llena por rutina con «no aplica», la Regla 5 no tiene datos sobre los que computar y la discrepancia vuelve a depender de que alguien la lea y opine. La transcribe el Destilador (desde el literal de la Disposición, sin releer la ley desde cero); el Auditor la verifica contra el literal.

* **Sanción — las dos cosas distintas que se llaman así.** ① El **texto que tipifica** una infracción (arts. 34 bis / 34 ter / 34 quáter) es una Disposición como cualquier otra: el Fragmentador la transcribe y la clasifica con el valor `Sancionadora` del `Tipo de norma` *(minuta 7: antes «valor `Sanción` de la Clasificación deóntica» — la taxonomía en dos ejes lo reclasifica)*. ② La **calificación de una Exigencia** no la dice necesariamente su artículo sustantivo: es una conclusión que conecta una conducta hipotética infractora con los elementos de un tipo sancionador o fundamenta la ausencia de tipificación. El Destilador la desarrolla mediante la skill `calificar-sancion-exigencia` y conserva **todo** su examen en `## Sanción`, incluido el resultado `0` o vacío, sin atribuir una multa a una organización. Una Exigencia puede relacionarse con más de una conducta infractora o tipo; la ficha conserva esas vías y sus presupuestos sin inferir por ello varias multas. Si conductas diferentes de la misma Exigencia tienen calificaciones distintas (`0`, `1`, `2` o `3`) **ya fundadas**, el campo muestra `Calificación variable según la conducta`; cada vía permanece explicada en `## Sanción`. Si el análisis no está concluido, el campo queda vacío con impedimento localizado en esa sección. No se asigna el mayor grado como etiqueta única a una regla variable. La etiqueta permite filtrar; el indicador derivado del Ítem examina además los grados de todas sus vías y su cobertura (ver §6.2). La Disposición de la regla no contiene por sí sola el tipo; la Disposición sancionadora puede tipificar muchas conductas.

**Dónde viven tres vocabularios que esta tabla usa pero no define:** (a) el vocabulario cerrado de `Destinatario` (seis valores) y una glosa por rol vive en el prompt del Destilador de Exigencias; (b) la asignación de `EX-NNN` local y su reserva en el `COBERTURA.md` de la Fuente vive en ese mismo prompt; (c) los slugs YAML canónicos tienen su referencia en `01-Bases-de-Datos-y-Propiedades.md`, sección «Slugs YAML canónicos». Los agentes operativos reciben las instrucciones necesarias en su propio contrato; no necesitan cargar el esquema completo.

### Etapa 5 — Destilada

Orquestador comprueba `INFORME-DESTILACION.md` contra `COBERTURA.md`, las filas únicas de `RESULTADO.md` —incluidas las Disposiciones sin Exigencia propia—, las fichas, sus anclajes y los enlaces reales. Verifica que sus controles tengan evidencia y que los hallazgos o comprobaciones no realizadas no se presenten como ausencia de hallazgos. Mueve la Fuente a `Destilada` solo cuando todas las Disposiciones del alcance tienen resultado cerrado y los pendientes no impeditivos permanecen visibles; una fila `Examen incompleto` impide ese cierre. El informe del productor no sustituye la auditoría independiente.

### Etapa 6 — En auditoría (Auditor de anclaje)

**Por qué interviene un Auditor distinto:** el Fragmentador y el Destilador comprueban sus propios productos, pero ese control no permite detectar independientemente una regla que ninguno de los dos registró. El Auditor contrasta cobertura, fidelidad y posibles omisiones con el PDF primario de la misma Fuente y versión. Su revisión es técnica; no visa Exigencias ni comprueba prácticas de la organización.

**Condición de independencia — dos pases consecutivos:** **Pase 1, mapa independiente:** el Orquestador entrega solo el PDF primario, cuerpo y versión, huella SHA-256 esperada, alcance y destino del mapa. No entrega `FUENTE.md`, `ARBOL.md`, archivos de Disposición ni productos o comentarios de los productores: esos archivos pueden contener análisis previos. El Auditor lee el PDF artículo por artículo y escribe `MAPA-INDEPENDIENTE.md` con localizadores propios del PDF. Este pase puede prepararse durante `En destilación`, sin mover la Fuente, solo si el encargo humano comprende auditoría de esa Fuente; la posibilidad de anticiparlo no amplía un encargo limitado a `Destilada`. El Orquestador comprueba y preserva el mapa. **Pase 2, contraste:** únicamente después de preservar el mapa y comprobar que la Fuente está `Destilada`, entrega los productos completos de fragmentación y destilación; el Auditor verifica identidad y huella, confronta afirmaciones y omisiones con el PDF y el mapa, y escribe revisiones y veredictos. Si cambió el PDF, el mapa anterior no sirve para la nueva huella. El razonamiento del productor es objeto de auditoría, no evidencia suficiente por sí solo. (Mismo modelo ⇒ sesgos comunes posibles; estos pases reducen contaminación, no garantizan ausencia de error.)

**Qué hace:** revisa la cobertura de cada Disposición y las Exigencias existentes, incluidas posibles omisiones que carecen de ficha. Concilia en ambos sentidos: cada artículo y pasaje relevante del PDF y del mapa independiente con `ARBOL.md`, y cada Disposición del árbol con una fila única de destilación. Si un pasaje relevante falta del árbol, registra Fuente, versión, página, localizador y cita breve del PDF como hallazgo «sin Disposición creada»; no inventa identificadores. La coincidencia entre árbol y resultados no acredita por sí sola cobertura del primario. Por Exigencia vuelve a los pasajes exactos del PDF primario y al contexto del artículo; compara con ellos la regla y los anclajes afirmados en la ficha, sin exigir que una interpretación fiel repita literalmente el PDF. Aplica 13 dimensiones (Sí/No/Parcial/No aplica con evidencia): procedencia y anclajes, incluido que el derecho comparado no sustituya el fundamento en la Fuente y versión que se auditan; literal y cita; corte; destinatario; modalidad; conducta y supuesto; condiciones, excepciones y remisiones; plazo; enumeración; determinación; sanción; ámbito temporal; coherencia del conjunto. Una remisión necesaria no examinada queda pendiente; una omisión sin ficha se registra por Disposición cuando existe o por pasaje del PDF cuando aún no se creó, sin inventar Exigencia. Produce `Resultados/<fuente-y-version>/Articulos/<articulo>/REVISION.md` e `INFORME-AUDITORIA.md`, con enlaces al mapa preservado y a las revisiones. Emite `VERIFICADA / CORREGIBLE / ESCALAR A HUMANO`; la falta de acceso o evidencia indispensable queda pendiente sin veredicto. Si falta una ruta local, delimita la unidad y las comprobaciones dependientes, y continúa las independientes; si no puede comprobar identidad, versión o huella del PDF, detiene el contraste. Por cada `ESCALAR A HUMANO` registra en revisión e informe el pasaje decisivo del PDF, Fuente y versión, localizador y página, pregunta jurídica y efecto posible, y devuelve esos datos y rutas al Orquestador; la etiqueta sola no basta. El Auditor no crea por sí solo una Escalada. El Auditor escribe la marca técnica en su informe; **nunca escribe `Visada` ni mueve la Fuente**.

**Tabla ③ Exigencias — propiedades que se escriben aquí:** `Resultado de auditoría vigente` = Pendiente / Verificada / Corregible / Cuestión jurídica escalada / Revisión pendiente por cambio.

### Etapa 7 — Auditoría completada

Orquestador comprueba desde su destino el mapa preservado, las revisiones por artículo, el informe global, los veredictos, las omisiones y las dependencias de corrección. Aplica los estados técnicos de auditoría y cierra la etapa solo si el alcance fue revisado y cada hallazgo tiene resultado o ruta pendiente visible; un impedimento que dejó parte del alcance sin examinar impide declarar completa la auditoría. Un cierre con cuestión jurídica pendiente muestra esa limitación y no equivale a resultado favorable. **Los tres informes globales técnicos** (fragmentación Fragmentador de Fuentes, destilación Destilador de Exigencias, auditoría Auditor de anclaje) permanecen en los productos de sus agentes y se enlazan desde el registro de cierre en `Ejecuciones/`; cuando se trabaje en el espacio de datos, la Bitácora podrá indexar esos cierres sin duplicar los informes. Relator no sustituye ni duplica esos informes.

> Repetido porque es el malentendido más caro: **`Auditoría completada` no significa Exigencias visadas ni cumplimiento.**

### Etapa 8 — Lista para uso en Dominio

Después de `Auditoría completada`, el Orquestador comprueba desde el PDF y la huella
vigentes, el mapa preservado, `ARBOL.md`, `COBERTURA.md`, todas las filas de
`RESULTADO.md`, las fichas activas y el informe de auditoría que: (1) todo el
alcance del primario quedó examinado y conciliado; (2) cada omisión material fue
descartada con evidencia o corregida y reauditorada con sus dependencias; (3)
toda Exigencia activa tiene veredicto técnico vigente `VERIFICADA` y los datos
necesarios para el trabajo de Dominio, incluida una calificación sancionatoria
fundada —variable cuando corresponda— o una conclusión negativa fundada,
están comprobados o fundadamente declarados no aplicables;
y (4) no queda cuestión jurídica, corrección, acceso o revisión por cambio
pendiente que pueda modificar el universo, la regla, sus anclajes o los datos
usados después. Una Fuente sin Exigencias también puede alcanzar esta etapa
si el examen completo acredita ese resultado. Un límite no material permanece
visible, con razón de por qué no afecta el uso.

Registra en `Ejecuciones/` la transición técnica, fecha real, Fuente, versión,
huella, rutas y conteo de fichas activas comprobadas, hallazgos resueltos,
límites no impeditivos y evidencia de cada condición. Si la auditoría ya
cumple la compuerta, registra consecutivamente `Auditoría completada` y
`Lista para uso en Dominio`; no omitas ninguno de los dos asientos. Si una
cuestión jurídica requiere decisión humana, conserva `Auditoría completada`
sin avanzar; tras la decisión y las correcciones necesarias, reaudita el
alcance afectado antes de comprobar de nuevo la compuerta. Al encargar la
reauditoría mueve la Fuente a `En auditoría` y, tras comprobar su cierre,
vuelve a `Auditoría completada`. Si surge un cambio
material después de `Lista`, vuelve la Fuente y versión afectadas a `En
auditoría` para la revisión pertinente y conserva el cierre anterior en el
historial; aplica las autorizaciones humanas del circuito de Revisión por
cambio antes de analizar o corregir los efectos. El Orquestador localiza las
entregas de Dominio que usaron ese cierre, deja provisional la conclusión
afectada y reencarga su examen cuando la Fuente recupere aptitud, sin borrar
el historial. Una nueva versión normativa tiene expediente propio.

`Lista para uso en Dominio` habilita la Fuente como **insumo técnico auditado**,
no decide si es aplicable a un Dominio o período: esa decisión sigue el circuito
humano de `Delimitar`. Tampoco equivale a `Visada` ni autoriza una conclusión
jurídica final sin las decisiones humanas reservadas.

***

## 5. Ciclo de Dominio, etapa por etapa

**Condición de entrada:** `Delimitar` y `Diagnosticar` pueden preparar el Dominio con al menos una Fuente destilada íntegramente (referencia del Laboratorio: la Ley 19.628 consolidada con la reforma 21.719), aunque su auditoría siga abierta. El uso sustantivo de Exigencias en `Investigar` exige al menos una Fuente confirmada aplicable y `Lista para uso en Dominio`. No exige que todas las Fuentes estén listas; las restantes permanecen como advertencias y no se presenta el universo como completo.

**Paso entre etapas:** tras cada entrega de `Delimitar`, `Diagnosticar`,
`Investigar` y `Agrupar`, el Orquestador comprueba los productos y presenta a
la persona el resultado, alcance, límites y decisiones pendientes. Detiene el
despacho del Dominio hasta que la persona autorice expresamente la etapa
siguiente; registra esa autorización con identidad y fecha reales y solo
entonces mueve la etapa. Una instrucción inicial para trabajar en el Dominio
no autoriza de una vez todos los pasos. La autorización de paso es distinta
de las decisiones jurídicas o de hechos reservadas a la persona. Tras
`Decidir`, el Orquestador presenta el cierre y no inicia por continuidad
trabajo de Ítems o Subítems. Los nombres y criterios de hitos intermedios
de cierre quedan pendientes de definición; esta compuerta rige ya entre las
cinco etapas descritas aquí.

**Estructura del home del Dominio:** presentación → kanban compacto (una tarjeta, cinco columnas) → situación de fase → resumen de trabajo y avisos → Ítems con dos pestañas → accesos a pendientes → toggle `Proceso y fundamentos del Dominio` con `Fase - Delimitar / Diagnosticar / Investigar / Agrupar / Decidir` y sus sub-entregas. Los filtros se vinculan al **ID del registro maestro** (base ⑤ Dominios), no a la página.

**Advertencias por condición (el sistema dice cuándo su propia información está incompleta — principio de §1).** Si una Fuente confirmada aplicable al Dominio está sin destilar íntegramente, el home muestra la advertencia: «N Fuente(s) aplicables sin destilar afectan a este Dominio». Si está destilada pero aún no `Lista para uso en Dominio`, muestra por separado «N Fuente(s) aplicables pendientes de habilitación para uso en Dominio» con su etapa y bloqueo concreto. También separa las Fuentes conocidas cuya aplicabilidad sigue pendiente y las no examinadas o inaccesibles; ninguna se cuenta como jurídicamente excluida por falta de análisis. No es decoración: si el Dominio muestra «N Exigencias, M Ítems» con corpus incompleto, alguien podría validar los Ítems sin saber que falta universo. Las advertencias **se generan por condición, no como registro**: desaparecen al cumplirse su condición; la transición queda en `Ejecuciones/` y podrá indexarse en la Bitácora del espacio de datos. El resumen del Dominio muestra además el indicador cuantitativo de alcance de Fuentes definido en Delimitar; una restricción voluntaria o falta de examen mantiene la marca «análisis de alcance limitado» hasta que se amplíe el examen.

### Etapa 1 — Delimitar (Delimitador de Dominio + humano)

**Qué hace Delimitador de Dominio:** propone candidatos de frontera en cinco categorías — probablemente entra 🟢 / pertenece a otro Dominio 🟡 / organizacional 🔵 / fuera de alcance ⚪ / no puede determinarse ❓ — con callouts de orientación y propuesta en `Fase - Delimitar → Delimitación y decisiones`. **El humano confirma, ajusta o rechaza cada frontera.** Delimitador de Dominio nunca decide.

**Alcance de Fuentes del Dominio:** antes de Delimitar, el Orquestador registra el período al que se refiere el análisis del Dominio: fecha de corte o intervalo, según el encargo humano. Entrega al Delimitador el inventario de **todas las Fuentes y versiones conocidas en `planificacion/`**, incluidas las anteriores y los proyectos, con identidad, vigencia declarada, fechas relevantes, estado técnico y acceso al primario. El Delimitador conserva todas las entradas y propone, con fundamento documental, cuáles son candidatas para ese período, cuáles podrían excluirse temporalmente y cuáles requieren aclaración. Para un análisis prospectivo, `Vigente` y `Vigente con vacancia` son candidatas iniciales; la vacancia no demuestra que una regla ya sea exigible. Una versión `Derogada` puede ser pertinente para un período pasado o efectos que perduran. Un `Proyecto` se conserva identificado fuera del universo normativo ordinario, salvo encargo expreso de análisis de escenario. El estado de vigencia por sí solo no decide la aplicabilidad al Dominio. La persona confirma, ajusta o rechaza las exclusiones temporales y las decisiones de aplicabilidad jurídica; hasta esa confirmación, una exclusión propuesta permanece en el universo por examinar como pendiente. El Orquestador registra decisión y fundamento. Por defecto, el Delimitador examina cada entrada del universo temporal y propone si es aplicable, no aplicable o queda pendiente de hechos o de una cuestión jurídica. No se pide a la persona una selección previa de Fuentes. Una Fuente no examinada, inaccesible o sin destilar no se vuelve «no aplicable» ni temporalmente excluida por ese motivo. Si se solicita expresamente un ejercicio restringido, el Delimitador conserva el inventario completo, marca las candidatas omitidas como `No examinada por límite del encargo` y presenta **análisis de alcance limitado**. No se presume que el inventario contenga todo el derecho relevante; las lagunas conocidas se declaran.

**Indicador de alcance de Fuentes.** En el encabezado de cada entrega del ciclo de Dominio y en su resumen se escribe, con cifras reales, `Análisis de alcance completo: se examinaron X/Y Fuentes y versiones del universo temporal` si `X = Y > 0`, o `Análisis de alcance limitado: se examinaron X/Y Fuentes y versiones del universo temporal` si `X < Y`. `Y` cuenta los pares distintos Fuente–versión candidatos para el período registrado, incluidos los de pertinencia temporal pendiente y los que tienen una exclusión temporal propuesta aún no confirmada. Solo se retira de ese universo una exclusión temporal fundada y confirmada por la persona; el par permanece en la tabla completa, con decisión y motivo. Los `Proyecto` verificados se identifican aparte porque todavía no son normas vigentes; si su condición es incierta, no se los retira por mera etiqueta. `X` cuenta los pares de `Y` examinados sustantivamente para determinar su relación con el Dominio. Una Fuente solo inventariada no cuenta en `X`; una examinada y propuesta como no aplicable o pendiente tras el examen sí cuenta. El inventario y el universo temporal se identifican por fecha y ruta; la tabla permite recalcular `X/Y`. Si el inventario está vacío, se declara `Alcance de Fuentes indeterminado: inventario vacío`; si existe inventario pero no hay candidatas para el período, `Alcance de Fuentes indeterminado: ninguna Fuente y versión candidata para el período`. Sin período declarado no se calcula `X/Y` ni se declara alcance completo. Una Fuente, versión o decisión temporal nueva obliga a revisar el denominador y las entregas afectadas. **«Completo» califica únicamente el examen del universo temporal conocido:** no acredita aplicabilidad resuelta, destilación terminada, universo completo de Exigencias ni que el inventario reúna todo el derecho relevante. Los pendientes y advertencias permanecen visibles por separado.

Una aplicabilidad pendiente no impide analizar provisionalmente las Exigencias de las Fuentes ya confirmadas; sí impide presentar ese resultado como universo completo y debe acompañar a `Investigar` hasta su resolución. El cierre de `Delimitar` deja constancia de las decisiones adoptadas y de cada pendiente, sin convertir este último en exclusión.

**Contrato de entrada al trabajo de Dominio:** el Orquestador fecha y conserva en `Ejecuciones/` el inventario de pares Fuente–versión, sus rutas y etapas de fragmentación, destilación, auditoría y aptitud de uso. El Delimitador devuelve cuatro listas separadas: aplicabilidad confirmada por persona, aplicabilidad pendiente, Fuentes no examinadas o inaccesibles y no aplicabilidad confirmada por persona. Una Fuente confirmada aplicable sin destilar o todavía no lista sigue como advertencia; no se le inventan Exigencias ni se la excluye jurídicamente. Para `Investigar`, el Orquestador fija en el registro del encargo una lista identificable de todas las claves completas de **fichas activas** de Fuentes confirmadas aplicables y `Lista para uso en Dominio`, conciliadas con `COBERTURA.md` y el cierre de habilitación; una ficha retirada queda en historial y fuera del universo activo con razón visible. La lista conserva rutas, etapa de Fuente, total y referencia al diagnóstico e indicador de alcance, sin copiar el análisis de cada ficha. Detector y Relator reciben **esa misma lista**, cada uno en su contexto. Las Fuentes aplicables aún no listas se registran como pendientes del universo, con etapa y bloqueo; sus fichas no se incorporan silenciosamente al universo sustantivo. Cuando cambia una premisa del universo, el Orquestador registra el cambio y reencarga el examen afectado; ninguna ficha desaparece en silencio. Sin Fuente confirmada aplicable y lista, no se concluye que el Dominio carezca de Exigencias.

**Tabla ⑤ Dominios — propiedades:** Nombre · Etapa del ciclo · Responsable · Fuentes aplicables · Exigencias (two-way) · contenido 🧾: Qué es / Por qué importa / Qué implica hacerlo.

**La capa de lectura — criterio de escritura.** Los tres campos 🧾 (`Qué es` / `Por qué importa` / `Qué implica hacerlo`, en Dominio, Ítem y Subítem) son contenido del cuerpo de la página (en la fase de archivos: del cuerpo de la ficha) y existen para **quien no conoce la materia** — un DPO recién llegado, un director, alguien de Producto. Si esa persona los lee y sigue sin entender qué está en juego, el campo está mal escrito aunque sea jurídicamente preciso. Contenido obligatorio: «Por qué importa» lleva la consecuencia económica concreta con norma y monto, quién queda expuesto y qué pasa si no se hace; «Qué implica hacerlo» lleva las áreas involucradas, el trabajo previo antes del entregable visible y las decisiones jurídicas pendientes con lo que bloquean — **gestiona la expectativa de esfuerzo**: evita que alguien lea «Política de Privacidad» y piense que son dos días. **Quién los redacta:** los propone el agente de la etapa (con marca ⏳ «propuesta sin visar») y los visa el humano: para el Dominio, el Delimitador de Dominio al cerrar Delimitar; para el Ítem, el Relator al documentar la formulación en Decidir; para el Subítem, quien lo crea al abrirlo.

### Etapa 2 — Diagnosticar (Delimitador de Dominio + Orquestador + humano)

Hechos y evidencias de personas reales mediante cuestionario. El Delimitador prepara por escrito un bloque común de preguntas y las preguntas específicas que nacen de fronteras, Fuentes y versiones todavía inciertas. El Orquestador presenta esas preguntas a la persona, conserva sus respuestas sin completarlas ni reinterpretarlas y devuelve el registro al Delimitador. Este identifica hechos declarados, falta de respuesta, necesidad de comprobación y efecto sobre las propuestas de Delimitar; si una respuesta cambia una frontera o la aplicabilidad de una Fuente, propone reabrir solo esa decisión para confirmación humana antes de Investigar. **Ningún agente inventa ni verifica por mera entrevista la realidad de la organización**: si hace falta inspección o levantamiento, se señala qué debe comprobarse y por quién; solo con **confirmación humana expresa** el Orquestador crea un Ítem de tipo `Levantamiento previo a Agrupación` (excepción canónica «sin Agrupación ni Exigencia ficticias»).

En archivos, `Delimitador-de-Dominio/Resultados/<dominio>/DIAGNOSTICAR.md` conserva el cuestionario antes de preguntar, agrupado por ronda y numerado solo para lectura dentro de ella. Cada pregunta indica hecho buscado, razón, efecto posible y evidencia solicitada. El Orquestador conserva en un mismo registro de `Ejecuciones/` la ronda y las preguntas en el orden presentado, cada una junto a su respuesta literal o ausencia, autor, fecha y evidencia recibida; el Delimitador enlaza ese registro y clasifica cada hecho como declarado, comprobado con evidencia, ausente o pendiente de comprobación. Las preguntas complementarias se añaden en otra ronda sin reemplazar las anteriores. La numeración no crea una entidad con ID estable ni se abre un archivo por pregunta o respuesta.

**Por qué Diagnosticar precede a Investigar (principio general, no atado a corridas pasadas):** una parte sustancial de las Exigencias condiciona su aplicabilidad a hechos de la organización — qué datos se tratan, si pueden intervenir menores, si hay encargados, si los datos salen del país, si hay tratamiento automatizado o perfilamiento. Sin diagnóstico previo, la correspondencia normativa de Investigar se produce sobre aplicabilidad indeterminada: inclusiones y exclusiones que habrá que rehacer cuando los hechos aparezcan. Con él, Investigar trabaja sobre hechos declarados y lagunas explícitas. **El Delimitador es responsable del contenido y del análisis del cuestionario; el Orquestador es la única interfaz con la persona y custodio de las respuestas.** La disciplina vive en sus respectivos `PROMPT.md`, no en el contrato común (ver `02-Gobernanza-y-Context-Engineering.md` §8). Tres propiedades del cuestionario: **definido antes de cada ronda** (bloque común conservado y preguntas adicionales justificadas por pendientes concretos, sin inventar preguntas al transmitirlas); **acumulativo** (lo ya respondido queda registrado y no se pierde entre sesiones); **límite honesto** (una respuesta ausente o no comprobada no se rellena con una suposición y puede exigir inspección técnica). Las preguntas complementarias se redactan y conservan antes de la siguiente ronda, con el motivo que las exige.

### Etapa 3 — Investigar (Detector de concordancias modo 1 + Relator de Agrupación modo 1, en contextos separados)

Dos entregas independientes:

* **Detector de concordancias — Correspondencia normativa**: una fila por Exigencia del universo confirmado y de Fuentes `Lista para uso en Dominio`, con clave completa, inclusión/exclusión/pendiente, razón anclada al diagnóstico, versión normativa y referencia al cierre de aptitud. En el harness escribe `Resultados/<dominio>/INVESTIGAR.md`; el Orquestador lleva la entrega al home `Fase - Investigar → Correspondencia normativa`. Una Fuente confirmada aplicable todavía sin destilar o aún no lista queda como advertencia de cobertura, con bloqueo; una Fuente de aplicabilidad pendiente o sin examen queda como límite distinto del universo. Ninguna se presenta como exclusión ni como cobertura presumida.

* **Relator de Agrupación — Contraste independiente**: primera valoración **preservada antes de conocer el mapa del Detector de concordancias**, en contexto separado → `Fase - Investigar → Contraste independiente`. Usa la misma lista identificable del universo y registra una fila por clave completa antes del contraste; el Orquestador comprueba la preservación y la conciliación de totales.

El universo se recibe con claves completas `<fuente-y-version>/EX-NNN`. Si la ley modificatoria y la ley consolidada contienen fichas parecidas, Investigar conserva ambas y señala una **posible correspondencia** con sus anclajes y vigencias; no excluye una por parecer duplicada. Hasta el contraste de Agrupar, «N fichas de Exigencia» no equivale a «N deberes jurídicos independientes».

«Investigar no cierra con la primera respuesta del Detector de concordancias.»
El Orquestador concilia ambas entregas por clave y conserva las dos lecturas
cuando difieren. Identifica la premisa y el efecto de cada divergencia: un
texto o cotejo faltante vuelve al especialista competente; un hecho de la
organización faltante vuelve al cuestionario del Delimitador y lo presenta
el Orquestador siguiendo el circuito de Diagnosticar. Una
cuestión jurídica que persiste tras el reexamen sigue el circuito de Opciones
y Escalada para decisión humana. El Orquestador no escoge una interpretación.
Una divergencia capaz de cambiar la inclusión o exclusión de una Exigencia
impide presentar `Investigar` como completo hasta resolverla.

### Etapa 4 — Agrupar (Detector de concordancias modo 2 + Relator de Agrupación modo 2)

**Ejecución nueva** del Detector de concordancias (no continuación de la anterior):

1. **Paso 0 — Pase ciego**: en ejecución nueva, el Detector recibe universo, diagnóstico y primarios, sin el mapa interpretativo de Investigar, valoración del Relator ni Agrupaciones/Ítems anteriores. Escribe `Resultados/<dominio>/PASE-CIEGO.md` con afinidades y fecha/hora reales; el Orquestador comprueba y preserva esa primera entrega y registra un solo antecedente de pase en `Ejecuciones/` antes de revelar el contexto excluido. En el espacio de datos, la Bitácora puede indexar ese antecedente. (Heredado del Taller LTDP: técnica anti-sesgo.)
2. **Paso 1 — Selección de comparaciones y seis reglas de concordancia.** Para cada Exigencia, el Detector busca pares o conjuntos pertinentes según materia, destinatario, conducta, objeto, condiciones, excepciones, enumeraciones, remisiones y período; incorpora además las relaciones sugeridas por el pase ciego y las dos entregas de Investigar. Una diferencia en estos datos puede justificar el contraste: no se exige identidad de palabras. `AGRUPAR.md` conserva una fila por clave con otras claves de posible relación pertinente, razón o `Ninguna identificada`, y duda pendiente. Cada par o conjunto seleccionado se examina una vez con las seis reglas, sin exigir una tabla de todos los pares posibles. Cada resultado indica `Aplica / No aplica / No evaluable`, datos decisivos, anclajes y motivo; el cierre de aptitud de las Fuentes se comprueba **aparte** y cualquier Fuente aplicable no lista mantiene limitado el alcance del Dominio. Si un cierre de aptitud del universo deja de estar vigente, se recompone el encargo antes de concluir. Un dato incierto del diagnóstico solo afecta la comparación que lo necesita; ninguna ficha desaparece del universo fijado. Estas pruebas son método del Laboratorio, no conclusión jurídica automática:

   | Regla | Pregunta operativa |
   | --- | --- |
   | 1 Concordancia | ¿Hay reglas compatibles sobre la misma materia, considerando destinatario, conducta, condiciones y tiempo? No fusiona fichas. |
   | 2 Especialidad | ¿Una regla añade un supuesto más estrecho? No presume derogación ni prioridad. |
   | 3 Conflicto | ¿Coinciden conducta, sujetos y tiempo, pero aparecen modalidades o efectos incompatibles? Devuelve la duda jurídica localizada. |
   | 4 Candidatas a Ítem | ¿Las Exigencias podrían trabajarse hacia un mismo resultado del Dominio? Propone Agrupación, no crea Ítem. |
   | 5 Discrepancia de alcance | ¿Difieren listas cerradas, supuestos, destinatarios, condiciones o tiempo sobre la misma materia? Identifica la diferencia exacta. |
   | 6 Acumulación | ¿Deben examinarse juntas dos reglas que no se sustituyen? La base para transferir del art. 27 y la base para tratar son ejemplo, no fórmula universal. |

   Límite honesto: estas reglas no detectan por sí solas tensiones de optimización entre obligaciones concurrentes.
3. **Paso 2 — Contraste global** y Agrupaciones Propuestas en `Resultados/<dominio>/AGRUPAR.md` → `Fase - Agrupar → Entrega de concordancias`. Antes de contrastar, el Orquestador y el Detector comprueban que pase ciego, Investigar y valoración independiente usan el mismo universo de claves de Fuentes listas; si cambió, se reencarga el examen afectado. Una tabla final tiene exactamente una fila por clave completa del universo, con propuesta(s) localizables, `Pendiente` o `Sin agrupación justificada`, motivo, condición vigente de aptitud de la Fuente y acción pendiente. Una Exigencia en varias propuestas conserva una sola fila que explica el solapamiento. `Pendiente` no se disfraza de ausencia justificada de agrupación. El Orquestador concilia claves y total antes de entregar las propuestas al Relator.

Una Agrupación puede reunir Exigencias de Fuentes distintas cuando el contraste de reglas, condiciones, destinatario y tiempo lo respalda. Conserva las fichas y anclajes de cada Fuente; agruparlas no decide por sí solo identidad jurídica ni elimina un deber acumulativo. La decisión de sostener la Agrupación y formular el Ítem sigue su circuito humano en Decidir.

**Relator de Agrupación modo 2 — Relato de Agrupación**: en la ficha de cada Agrupación, evidencia a favor, **en contra** y configuraciones alternativas. «Esta salida reúne evidencia; no constituye un dictamen.» Solicita el paso a `Relatada`; no decide.

En el harness, `Relator-de-Agrupacion/Resultados/<dominio>/AGRUPAR.md` conserva una sección por propuesta del Detector, con todas sus claves de Exigencia, criterio de cohesión, evidencia a favor y en contra, alternativas y pendientes; una ficha maestra autorizada se enlaza sin duplicar el relato. El Relator contrasta además las razones por las que no se identificó un par o conjunto pertinente y examina cada Exigencia `Sin agrupación justificada` o `Pendiente` de la tabla de cobertura, con clave, evidencia y posible relación omitida. Devuelve esa discrepancia al Orquestador para reexamen del Detector; no añade ni sostiene una Agrupación por su cuenta. Una propuesta con premisa decisiva no evaluable se presenta con esa limitación y no como sostenida.

**Tabla ④ Agrupaciones — propiedades:** Nombre · Tipo (Hipótesis inicial / Emergente) · Origen · Dominio · Exigencias · Regla(s) que la produjeron (Regla 1–6 / Pase ciego / Propuesta humana) · Estado · Criterio de cohesión 🧾 · Evidencia a favor / en contra 🧾 · Decisión y fundamento 🧾 (escritura humana) · Visada por · Fecha de visado · Ítem resultante. Plantilla con ficha de decisión: **pregunta primero, evidencia después, decisión humana al final**. Una Agrupación `No sostenida` no se elimina: «es la evidencia de que se consideró y se descartó».

### Etapa 5 — Decidir (humano + Relator)

El humano decide **en conjunto** las Agrupaciones y las formulaciones de Ítems (varias propuestas; una intervención puede resolver varias, con objetos y versiones identificados). «Sostener una Agrupación y aprobar el Ítem son decisiones distintas.»

Antes de cerrar `Decidir`, el Relator concilia todas las claves locales de
Agrupaciones propuestas en `AGRUPAR.md` y toda propuesta humana añadida
durante el ciclo con una fila por propuesta en su
informe: decisión humana y fundamento enlazados, o `Pendiente` con motivo y
responsable. `Dividir` y `Fusionar` enlazan propuestas de origen y destino;
cada propuesta resultante conserva su propia decisión o pendiente;
`Sostener` no crea ni valida un Ítem. Las formulaciones de Ítem se concilian
aparte con su decisión humana y ficha resultante cuando exista. El
Orquestador comprueba claves y rutas desde los productos; si falta una
decisión, presenta una entrega parcial y mantiene `Decidir` como etapa
vigente. Esta conciliación enlaza decisiones existentes y no crea otra base
de datos ni sustituye el fundamento escrito por la persona.

**Relator (Relator)** documenta: formulaciones (en la Agrupación si aún no hay autorización de crear el registro; en la ficha del Ítem si la hay) e informes de creación de Ítem y cierre de Decidir → home `Fase - Decidir → Decisiones y resultado de la fase`. Regla dura del Relator: **no compila resúmenes, vuelve a la evidencia**; y su campo «qué aportó el humano que no estaba en el material» no tiene límite de extensión, porque es el único contenido irreproducible. Segunda razón de ese campo, igual de importante: es **la evidencia auditable de que hubo criterio profesional humano** — ante una fiscalización o una auditoría del proceso, es el campo que responde «¿y esto lo decidió la IA?». Si no hubo aporte de ese tipo, se escribe literalmente «sin aporte de contexto externo»; nunca se inventa. El campo vive dentro del texto del relato en la ficha (contenido de página, Regla 3.0), y su bloque ✍️ de escritura exclusiva viene en la plantilla — ver las tres marcas en §3.3.

***

## 6. Agrupaciones e Ítems: los estados de decisión

### 6.1 Estados de la Agrupación

`Propuesta → Relatada → Decisión → Promoción (cuando procede)`. Decisiones posibles: **sostener / no sostener / dividir / fusionar**. La formulación preliminar del Ítem vive **en la Agrupación** hasta que exista autorización de crear el registro (`Propuesto`) o aprobación expresa de creación y formulación (`Validado`).

### 6.2 Estados de decisión del Ítem (cuatro, no secuenciales)

`Propuesto / Validado / Descartado / Fusionado`. (`Modificado` se retiró por ambiguo.)

* Cambio **editorial**: conserva `Validado`.

* Cambio **material**: conserva la aprobación histórica y envía la formulación revisada a `Propuesto` con la señal «Revisión de Ítem previamente validado».

* Un Ítem sin Subítems muestra `Sin descomponer` — **nunca 100 %**.

* El 100 % de Subítems definidos **desencadena una comprobación** de cobertura, evidencia, dependencias y Escaladas; no acredita automáticamente el cumplimiento.

* Un Ítem no se cierra con Escaladas abiertas. No se eliminan Ítems: se marcan `Descartado` con justificación («eliminar borra la evidencia»).

**Tabla ⑥ Ítems:** dos vistas sobre la misma base — **Decisiones sobre Ítems** (kanban de los cuatro estados) y **Ejecución de Ítems** (tabla: decisión, progreso, siguiente actuación). Ficha: situación/decisión, fundamento visible (Agrupación → Exigencias → Disposiciones → Fuentes/versiones, sin copiar el literal completo) con el párrafo `Severidad y cobertura sancionatoria` dentro del mismo cuerpo, Subítems, Escaladas, toggles `Decisión de creación y antecedentes`, `Cambios y revisiones`, `Resultados y evidencias`.

**Dos reglas de decisión sobre Ítems** (criterios permanentes del canon; la instrucción operativa para quien propone fronteras vive en el `PROMPT.md` del Delimitador de Dominio):

1. **Regla del alcance:** el dominio de un Ítem es **donde vive su artefacto principal**. La Política de Privacidad es un documento publicado en el sitio → Dominio Web; el procedimiento de ejercicio de derechos ARCO corre en el tiempo, en la organización → Organizacional. **El componente organizacional existe en toda implementación LPDP**: la propia ley impone obligaciones a nivel de organización que no pertenecen a ningún dominio (el RAT — Registro de Actividades de Tratamiento — es el ejemplo típico: recibe aportes de todos los dominios y no cierra con ninguno). Que el RAT viva en Organizacional en *esta* organización es una decisión de implementación que se toma una vez en Delimitar, se visa y se registra — no se re-discute por dominio ni se canoniza como lista cerrada.
2. **Test de prerrequisito:** cuando un Ítem necesita algo antes de cerrar (el RAT necesita el mapa de tratamientos de Web), ese algo merece ser Ítem propio solo si cumple **las tres** condiciones: tiene responsable propio distinto del Ítem que lo consume; tiene criterio de cierre verificable sin el consumidor; tiene valor aunque el consumidor no exista. Si falta una, es una tarea dentro del Ítem consumidor, no un Ítem — si no, «implementado» deja de ser verificable. La pertenencia es única; la dependencia se expresa con la relación `aporta a`.

**Severidad máxima del Ítem y cobertura del cálculo.** `Sanción — Calificación` es la etiqueta de cada Exigencia para filtrar vistas: `3 Gravísima`, `2 Grave`, `1 Leve`, `0 No tipificada` o `Calificación variable según la conducta`. Sus prefijos son parte del nombre visible, no una propiedad numérica. El Ítem conserva **Severidad máxima** como indicador derivado de las Exigencias relacionadas. Para obtenerlo, se consideran los grados fundados de las etiquetas simples y, en una Exigencia variable, **todos los grados de su `## Sanción`**; se comunica el máximo como exposición normativa potencial, no como multa aplicable a cada conducta. El indicador no es un campo de texto para advertencias. Si falta calificar una Exigencia o una vía, el **fundamento visible de la ficha del Ítem** identifica la cobertura incompleta y enlaza las fichas afectadas. Si ya existe una vía fundada `3 Gravísima`, el indicador puede mostrar `3` porque ninguna calificación pendiente elevaría ese máximo; si el mayor grado conocido es inferior, deja el indicador sin valor hasta completar el examen y explica en el fundamento el máximo parcial conocido. Antes de crear la ficha del Ítem, la advertencia se escribe en la formulación conservada en la Agrupación o en el informe del Relator. El Relator hace esta comprobación al formular un Ítem en el harness, sin crear otro expediente. Una implementación automática futura deberá convertir las etiquetas y vías fundadas en datos numéricos antes de usar un rollup `Max`; el rollup directo sobre una etiqueta de texto no acredita este resultado. La advertencia en el cuerpo de la ficha no aparece por sí sola en una vista que muestre únicamente propiedades.

### 6.3 Ciclo de Subítem (8 etapas)

`Delimitar → Estándar → Diagnosticar → Comparar → Decidir (si procede) → Preparar → Implementar → Evidenciar`, con estado `Bloqueado por dependencia`.

* **Investigador de Formas de cumplimiento** apoya en Estándar (referentes, jerarquía Chile-primero: ① norma chilena ② instrucción/dictamen de la Agencia ③ estándar técnico/comparado, con advertencia «no vinculante en Chile»).

* **Opciones de resolución y examen de antecedentes** apoya en Decidir.

* **Relator** relata cierres.

* **Regla clave:** «**Otra persona distinta del responsable verifica.** `Implementado` y `Verificado` son resultados diferentes.» La evidencia de ejecución es obligatoria para `Verificado` («no es el documento redactado: es la prueba de que opera»).

**Tabla ⑦ Subítems:** Ítem padre · Exigencia(s) que lo originan · Manifestación concreta · Etapa · Criterio de cierre (**declarado al abrir**) · Bloqueado por (→ Escaladas) · Área responsable · Responsable · Plazo · Formas consultadas · Evidencia de ejecución · **Verificado por (distinto del responsable)** · Requiere validación jurídica. (Su habilitación en la práctica es asunto de testeo: ver `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`.)

**Enrutamiento de la validación jurídica (cuándo se marca `Requiere validación jurídica`).** El problema que esto evita: sin regla se cae en uno de dos extremos — todo pasa por Compliance y Compliance se vuelve el cuello de botella, o todo lo valida el propio responsable y la delegación se vuelve ciega (un Subítem que cierra una Exigencia gravísima podría quedar `Verificado` sin que nadie con criterio jurídico lo mirara, con 20.000 UTM de exposición encima).

| Validación jurídica **obligatoria**                | Basta el responsable                      |
| -------------------------------------------------- | ----------------------------------------- |
| Cierra una Exigencia gravísima                     | Implementación técnica                    |
| Resuelve o depende de una Escalada                 | Redacción operativa sin decisión jurídica |
| Toca datos sensibles o transferencia internacional | Configuración                             |
| Etapa Decidir de cualquier Subítem                 | Etapas Preparar, Implementar, Evidenciar  |

**Más muestreo aleatorio del 20 % sobre el resto**, para que la delegación no se vuelva ciega.

**El estándar de la evidencia tiene fundamento legal:** es el mismo que el art. 14 quinquies inciso final exige para las medidas de seguridad — acreditar existencia **y funcionamiento**. Por eso la evidencia de ejecución «no es el documento redactado: es la prueba de que opera» (para el banner, captura del estado por defecto funcionando; para el canal ARCO, una solicitud de prueba con su respuesta registrada). Quien verifica es una persona distinta del responsable — eso no se delega — pero la forma es AI native: el Orquestador no acepta el cierre de Evidenciar sin el campo de evidencia completo, y el Relator documenta el cierre comprobando que la evidencia es prueba de operación y no solo el entregable.

### 6.4 Escaladas

Estados: `Detectada → Opciones propuestas → Decidida → Superada o desbloqueada`. El modelo ⑧ prevé una sola entidad de Escaladas con vistas por Fuentes, Dominios, decisiones pendientes, bloqueos e historial; su representación actual es la ficha de archivos descrita a continuación.

**Asiento vigente en archivos:** mientras el Laboratorio trabaja en `planificacion/`, el Orquestador crea una ficha por cuestión jurídica distinta en `harness-md-lpdp/Escaladas/ESC-NNNN.md` y la incorpora a `harness-md-lpdp/Escaladas/INDICE.md`. El número es identidad estable del expediente, no versión del archivo; no se reutiliza. Antes de crear, coteja el índice y las fichas para vincular hallazgos de la misma cuestión y evitar duplicados. Un informe conjunto de antecedentes puede servir a varias fichas, cada una con enlace a su apartado; no es la ficha de Escalada. El expediente conserva origen localizado, Fuentes/versiones y Disposiciones, Exigencias si existen, opciones, estado, dependencias, decisión y fundamento humanos, alternativas no elegidas, historial y comprobación de cierre. Si la duda nace antes de una Exigencia, la Disposición es origen suficiente. La ubicación en archivos permite abrir la Escalada durante la destilación; no se espera al cierre de la Fuente ni a otra aplicación. El modelo ⑧ sigue describiendo la entidad, pero no es requisito para registrar ahora el expediente.

* **Tipos:** Laguna / Delegación / Discrepancia de alcance / Conflicto normativo. Disciplina anti-inflación: «si la respuesta está en el texto y solo hay que leerlo bien, no es Escalada: es trabajo pendiente».

* **Opciones de resolución y examen de antecedentes** recibe un hallazgo localizado, sus primarios y versiones, hechos y lagunas; en revisión recibe además la decisión histórica y el mapa de impacto. Antes de crear o vincular una Escalada, relee el texto y busca en `planificacion/` decisiones humanas y Escaladas anteriores, dejando rutas, alcance de búsqueda y coincidencias o diferencias. Separa lectura ya resuelta, antecedente aplicable, dato o acceso faltante y duda jurídica genuina. Para cada cuestión registra en el informe una **matriz fija de control de alternativas**, con una fila por cada lectura material identificada, incluso la descartada, y estas columnas: clave `L1`, `L2`, etc. y lectura con efecto propuesto; anclaje y premisa decisiva; mejor fundamento a favor; objeción más fuerte; respuesta a la objeción o límite; resultado del control (`Permanece defendible / Descartada / No evaluable`); razón y comprobación pendiente. Una lectura es material si cambia destinatario, conducta, tiempo, condición o consecuencia jurídica. Cada columna se completa por lectura; la respuesta enfrenta la objeción concreta. Una lectura descartada o no evaluable no se cuenta como opción defendible. Solo para una duda jurídica genuina produce **mínimo dos opciones defendibles y materialmente distintas**, con anclaje, consecuencia regulatoria, riesgo asumido/evitado y reversibilidad; prohibido «recomiendo», «conviene», «debería» para dirigir la decisión, presentar una sola opción u ordenarlas por preferencia. Si no puede fundamentar dos, devuelve `opciones incompletas` con el impedimento, sin simular `Opciones propuestas`. Su entrega en archivos es `Opciones-de-resolucion-y-examen-de-antecedentes/Resultados/<identificador-del-encargo>/INFORME.md`; el Orquestador comprueba la matriz y las opciones antes de decidir si crea o vincula una Escalada. «El estado máximo producido por tu análisis es Opciones propuestas» significa resultado técnico propuesto, no que el agente pueda mover el estado de la Escalada.

  **Método jurídico visible:** en este rol, `documento primario` es el archivo de entrada del texto normativo de la Fuente y versión encargadas, localizado en `Fuentes-primarias/INDICE.md`; una Disposición fragmentada sirve de localizador y contraste, no lo reemplaza. Esa denominación no acredita por sí sola autenticidad oficial, vigencia ni autoridad. Por cuestión, el agente identifica tenor y vigencia, reconstruye destinatario, modalidad, conducta, supuesto, condiciones y excepciones, contrasta lectura literal con contexto y relaciones normativas justificadas, separa hechos declarados de aplicación jurídica y prueba cada alternativa frente a su objeción más fuerte. La cadena se escribe en el informe antes de formular opciones; no se presume jerarquía visada, derogación, errata ni hechos no acreditados. Las definiciones operativas y pasos completos están en el `PROMPT.md` del agente.

* **Reutilización de decisiones:** modalidades `Sólo antecedente` (valor prudente por defecto), `Reutilización con confirmación`, `Aplicación autorizada bajo condiciones`. El agente registra la modalidad acreditada por la decisión humana anterior, no concede una nueva autorización: la primera forma de reutilización requiere la confirmación prevista; la segunda, condiciones expresas y evidencia de cumplimiento actual. «La similitud semántica por sí sola no confiere esa autorización»; «'No consta' no se convierte en 'cumple'». Si faltan fundamento o condiciones, conserva `Sólo antecedente` y señala la decisión humana necesaria.

* Categoría nueva: **Revisión de decisión por cambio de fundamento**.

* Relaciones: `Nace de → Exigencias`, `Bloquea → Subítems`, `Afecta → Ítems` («"nace de" y "bloquea" no son sinónimos»), más las añadidas por la especificación consolidada: Fuentes de origen, Disposiciones de origen, Subítems de origen, Dominios afectados, Requiere actuación de, Antecedentes relacionados, señal `Criterio requiere revisión`.

* **Toda duda jurídica genuina termina en Escalada, pero quien la detecta no la crea.** El circuito con independencia: el agente que detecta la duda (en cualquier etapa) la registra como **hallazgo localizado en su entrega** (texto, localizador, por qué es duda) y la devuelve al Orquestador; Orquestador encarga el examen de antecedentes a Opciones de resolución y examen de antecedentes — un agente distinto del que detectó — y solo entonces se crea o vincula el expediente. Una duda detectada durante la fragmentación se vincula directamente a su Disposición de origen — no necesita una Exigencia ficticia para existir. Lo que NO es Escalada: un fallo técnico de acceso, una errata sin efecto, o una respuesta que ya está en el texto («eso es trabajo pendiente»).

Justificación de fondo (de la v6): «el DPO futuro hereda decisiones ajenas; si están con su fundamento las revisa, si no las rehace».

***

## 7. Correcciones y cambio normativo

### 7.1 Procedimiento de corrección (9 pasos)

1. Observación → 2. Comprobación inicial (Fragmentador de Fuentes si es literal, Auditor de anclaje si es fidelidad) → 3. **Conservar la versión anterior** (captura/exportación fechada; «una huella detecta cambios, pero no permite reconstruir») → 4. El Orquestador abre o vincula una Revisión por cambio y **pregunta directamente a la persona si autoriza iniciar el análisis de impacto**; una negativa o aplazamiento queda visible, sin mapa ni corrección implícita → 5. Tras autorización, fija el inventario fechado de resultados anteriores y encarga el mapa al Analista si existen productos anteriores o no puede comprobar su ausencia → 6. Presenta el impacto y obtiene autorización humana separada para corregir o revisar las entregas afectadas; asigna cada corrección al autor competente → 7. Corrección con relectura → 8. **Reauditoría independiente por Auditor de anclaje cuando corresponda** → 9. Comprueba cada dependencia como `revisada sin cambio / corregida y revisada / pendiente con responsable` y registra el cierre solo cuando no queden dependencias sin comprobar. El ciclo de Revisión por cambio de §7.3 conserva estos pasos sin duplicar los productos.

### 7.2 Cambio normativo

Tres vías de detección: vigilancia normativa, humano, redestilación. **«La vía humana debe existir siempre y no puede ser subsidiaria.»** Una nueva versión normativa requiere **su propia carpeta de Fuente y versión** en el harness y su propia ficha de versión en Notion; `Superada` es una relación de sustitución, no un borrado. El cambio abre o se vincula a una Revisión por cambio; cada Dominio afectado conserva la etapa anterior y, tras autorización humana del trabajo, vuelve a la primera fase que deba revisarse.

**Los tres escenarios y su propagación — qué le pasa a qué:**

| Escenario                                           | Qué se propaga                                                                                                                                   | Qué NO cambia                                                                      |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Una Exigencia se modifica**                       | Sus Subítems pasan a `Requiere reverificación`; baja el progreso derivado del Ítem                                                               | **El estado del Ítem no cambia**: la decisión de trabajarlo sigue siendo válida    |
| **Aparece una Exigencia nueva**                     | Se destila y se examina su efecto sobre Agrupaciones e Ítems existentes; la persona decide si hace falta un Ítem nuevo. Los Dominios afectados se enlazan a la Revisión por cambio | Las Exigencias e Ítems no afectados                                                |
| **Se deroga la Exigencia que daba sentido al Ítem** | El Ítem pierde su razón de ser → **decisión humana**: `Descartado` o `Fusionado`, con justificación                                              | La decisión no la toma el sistema; `Superada` queda como relación, no como borrado |

### 7.3 Ciclo de Revisión por cambio

**Unidad e identidad.** Una detección fundada de Fuente nueva, versión nueva
o corrección material que pueda afectar resultados anteriores abre o se
vincula a un expediente `Revisiones/REV-NNNN.md`, localizado desde
`Revisiones/INDICE.md`. Es un expediente por cambio comprobable, no por
Dominio ni por dependencia. Conserva Fuente y versión, cambio, evidencia,
origen de la detección, autorizaciones humanas, mapa enlazado, productos y
Dominios afectados, responsables, límites, historial y cierre. El Orquestador
lo mantiene; `Ejecuciones/` registra el trabajo realizado y los productos
permanecen en las carpetas de sus autores. Este ciclo se representa en
archivos durante la fase actual: no crea otra base de datos.

| Estado | Responsable y condición de paso |
|---|---|
| `Detectada` | El agente o la persona comunica un cambio localizado. Si lo detecta el Analista, devuelve una alerta breve, sin mapa. El Orquestador pregunta directamente a la persona si autoriza comenzar el análisis; antes de esa respuesta solo identifica el cambio y si existen productos anteriores, sin examinar dependencias. Registra palabras, identidad y fecha; negativa, aplazamiento o silencio dejan visible el posible impacto y no habilitan el mapa. |
| `En análisis` | Tras autorización expresa para ese cambio, el Orquestador fija el inventario fechado del examen: Fuente y versiones o archivos exactos, cambio localizado, índices, clases y rutas de productos anteriores. Si no existe ningún producto anterior en esas clases y los índices fueron accesibles, documenta esa comprobación sin mapa. Si existe alguno o falta acceso para saberlo, encarga el mapa al Analista. La ausencia de enlaces no prueba ausencia de impacto. |
| `Impacto evaluado` | El Orquestador comprueba el mapa, o el inventario que acreditó ausencia de productos anteriores, y presenta resultados y límites. Solo fundamenta `Cerrada sin impacto` cuando no hay productos anteriores o cuando todas las vías pertinentes del mapa quedaron `Examinada sin dependencia`. `No comprobada` o `Dependencia encontrada` impiden ese cierre. Si hay trabajo afectado, pregunta aparte si la persona autoriza su corrección o revisión. |
| `En revisión` | Requiere autorización humana expresa sobre el alcance de trabajo. El Orquestador asigna correcciones a sus autores y conserva la etapa anterior de cada Dominio. Cada Dominio vuelve a la primera fase afectada y mantiene sus compuertas humanas ordinarias; el mapa no decide aplicabilidad ni sustituye decisiones anteriores. |
| `Comprobada` | El Orquestador verifica desde destino cada resultado y la reauditoría independiente que corresponda. Una dependencia `pendiente con responsable` permanece abierta y no acredita cierre. |
| `Cerrada` | Todas las dependencias tienen resultado comprobado (`revisada sin cambio` o `corregida y revisada`), con rutas; se conservan las versiones y decisiones anteriores. `Cerrada sin impacto` conserva inventario, rutas y conclusión acotada; no se deduce de una mera búsqueda sin enlaces. |

La autorización para **analizar** no autoriza **corregir**. Si la persona ya
autorizó expresamente una de esas acciones para el cambio identificado, el
Orquestador registra esa referencia y no repite la pregunta. Una revisión
abierta no sustituye una Escalada: una duda jurídica genuina conserva su
expediente y decisión propios, enlazados cuando corresponda.

**Límite verificable de «sin impacto».** `Dependencia` significa producto
anterior cuya base, alcance, contenido o decisión documentada podría cambiar
por la Fuente o versión detectada; la posibilidad fundada basta, incluso sin
cita a ella. `Vía pertinente` es el recorrido desde el cambio a un producto
anterior que lo cita directa o indirectamente, o que trata la misma materia,
proceso u obligación aunque no lo cite. El Analista asigna a cada vía
`Examinada sin dependencia` (lectura y razón de ausencia), `Dependencia
encontrada` (posibilidad fundada) o `No comprobada` (impedimento localizado).
El universo comprende fragmentación, destilación, auditorías, entregas de
Dominio, Agrupaciones, Ítems, Subítems, Escaladas, decisiones humanas e
informes o instrucciones anteriores que interpreten o apliquen la Fuente;
el Orquestador deja ruta, fecha de corte y referencia de la
versión consultada de cada índice y producto. Para cerrar sin impacto,
escribe `Sin impacto en los resultados anteriores identificados en [inventario
fechado] tras examinar [vías y productos]`, enlaza la comprobación y no
extiende esa conclusión a otros productos o a los efectos generales de la norma.

**Vigilancia normativa — diseño acordado, ⏳ no implementada todavía.** El módulo de vigilancia (monitoreo periódico de Diario Oficial, sitio de la Agencia y LeyChile/BCN, con Analista de impacto de Fuente y marca «requiere revisión humana») se activará **cuando el sistema esté consolidado y estable** — sobre corpus inestable produce ruido sin valor. Cuando se active, opera bajo estas **reglas no negociables**, ya fijadas aquí para no tener que reconstruirlas: ① el agente **nunca modifica una Exigencia validada** — solo marca posible impacto (la Exigencia visada es el contenido más protegido del sistema: tiene firma humana); ② **nunca crea Exigencias** — si amerita destilación, dispara el ciclo normal de Fuente con su auditoría, nunca un atajo; ③ **toda detección queda registrada, incluidas las que se cierran sin impacto** — si no, en seis meses no se puede distinguir «revisamos y no nos afectó» de «nunca revisamos» (mismo principio que «una relación vacía no distingue "no examinada" de "examinada sin Exigencias"»). **Prioridad de revisión:** ante un pronunciamiento de la Agencia, se revisan primero las Exigencias con `Estado de determinación = Delegada` cuando la atribución expresa se relaciona con ese pronunciamiento (ej.: art. 11 letra a), «de acuerdo con los procedimientos que establezca la Agencia»). Esta prioridad no excluye revisar otras Exigencias que puedan resultar afectadas. Es una regla de diseño para la futura vigilancia, no una función implementada.

***

## 8. Trazabilidad, Ejecuciones, Bitácora y retención

**Trazabilidad triple:**

1. **Bloques sincronizados** para el texto literal: un solo original en la Disposición, espejos en Exigencias/Agrupaciones/Ítems. «El bloque sincronizado propaga el literal mostrado; no reescribe Exigencias, auditorías, Agrupaciones, Ítems ni decisiones humanas.»
2. **`Ejecuciones/` en el harness:** el Orquestador conserva por trabajo significativo el registro de lo ocurrido, los enlaces a productos, los asientos técnicos de etapa (transición o continuidad comprobada) y **qué prompt exacto se usó** (agente, ruta y fecha real del `PROMPT.md`, más huella o versión comprobable de su contenido). La fecha por sí sola no identifica una revisión exacta. Cada especialista conserva su checkpoint en el producto y el Orquestador lo enlaza desde el registro; así se puede reanudar **sin depender de recordar la conversación**. `registros/` queda reservado a versiones anteriores reconstruibles, no a otro historial activo.
3. **Bitácora en el espacio de datos** (base ⑪): cuando se trabaje allí, aporta relaciones y consultas estructuradas sobre esos hechos; puede construirse como índice o proyección de `Ejecuciones/`. No se lleva en el harness un segundo historial editable.

**Bitácora — campos previstos para el espacio de datos:** `Tipo de registro` (Ejecución / Incidencia técnica / Corrección material / Referencia de decisión), `Estado de ejecución` (Abierta / En curso / Interrumpida / Requiere actuación / Cerrada), identidad de encargo, ciclo/etapa, último checkpoint, relaciones a Fuente/Dominio/Escalada. Principio de proporcionalidad: «conservar fundamento y cambios relevantes, evitando registros equivalentes» — no una entrada por Disposición favorable, vista actualizada o mensaje de chat. **Los registros históricos no se borran ni se fusionan retrospectivamente.**

**Retención:** conservar versiones y antecedentes como **contenido estable** (capturas/exportaciones fechadas), no solo enlaces mutables ni huellas. «Se registrará la fecha real de cada hecho» — no retrofechar; si la hora original no se registró, se dice literalmente eso. *(25-09-2026: la regla «no renumerar N.º de ingreso» quedó sin objeto — esa propiedad se eliminó del esquema por decisión de MCF; la identidad inmutable la da el Identificador canónico, que tampoco se reasigna.)*

**Recuperación:** checkpoints por fase; «no se promete restaurar IDs después de borrar objetos; por ello no se borran originales para reconstruirlos». No hay transacción atómica entre archivos y Notion ⇒ escritura coordinada y comprobación antes de reanudar. Concurrencia (declarado débil): «una marca en Notion ayuda a coordinar, pero no reemplaza un mecanismo real de exclusión»; Orquestador concilia al reanudar.

**Documentación navegable:** la trazabilidad también exige que el sistema sea **legible transversalmente por humanos e IA**. Regla canónica: todo índice o documento organizador lleva un **árbol ASCII anotado con orden de lectura por rol y línea de verificación contra disco** — un índice desactualizado es un defecto reportable comprobable mecánicamente. Desarrollo completo e implementación en `02-Gobernanza-y-Context-Engineering.md` §3.1; árboles vigentes en el `README.md` de este paquete y el `INDICE.md` de la carpeta de agentes.

**Memoria operativa entre sesiones:** `MEMORY.md` es opcional y se crea solo si aporta punteros que cambian decisiones futuras y no se recuperan fácilmente desde productos y `Ejecuciones/`. No es canon ni fuente de verdad. Arranque de sesión: contrato común → prompt → memoria, si existe → perfil aplicable, si existe → encargo. Diseño completo en `02-Gobernanza-y-Context-Engineering.md` §5.1.

***

## 9. Dónde están las gates humanas (visado jurídico)

| Momento                                                 | Quién decide                         | Qué firma                                                     |
| ------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------- |
| Nivel de autoridad de una Fuente                        | humano                               | `Visado por` + fecha + `Fundamento del nivel`                 |
| Fronteras del Dominio (Delimitar)                       | humano                               | confirma/ajusta/rechaza candidatos del Delimitador de Dominio |
| Aplicabilidad de cada Fuente y versión al Dominio       | humano                               | confirma/ajusta/rechaza propuesta motivada del Delimitador; pendientes permanecen visibles |
| Exclusión temporal de una Fuente y versión del universo `X/Y` | humano | confirma/ajusta/rechaza propuesta documental del Delimitador para el período declarado; el par permanece en el inventario |
| Ítem de Levantamiento previo                            | humano                               | confirmación expresa                                          |
| `Visada` de una Exigencia                               | humano                               | `Visada por` + fecha                                          |
| Agrupación: sostener / no sostener / dividir / fusionar | humano                               | `Decisión y fundamento` 🧾                                    |
| Ítem: Validado / Descartado / Fusionado                 | humano                               | justificación del estado                                      |
| Escalada: Decidida                                      | humano                               | decisión + fundamento (incluida la opción no elegida)         |
| Subítem: Verificado                                     | persona **distinta** del responsable | `Verificado por` + evidencia                                  |
| Go/no-go de compuertas y corridas                       | humano                               | puede ser un «ok» puro                                        |

Distinción operativa del AGENTS.md: **go/no-go puro** («ábrela» basta) vs. **decisión con contenido jurídico** (exige fundamento humano; si no lo hay, se escribe literalmente `fundamento pendiente de aportar` — «NUNCA lo redactes tú»). Y: «Una decisión que existe solo en la conversación no existe.»

**Verificación de consistencia ≠ visado:** una revisión de consistencia hecha por un agente sobre una decisión humana se permite y se conserva como antecedente, pero se registra con su nombre real — «comprobación de coherencia por [agente]» — y **nunca** como visado ni como complemento del visado. El visado sigue siendo exclusivamente `Visada por` + fecha + fundamento humano. La razón: si una comprobación automática pasara por validación, la cadena de autoridad se invertiría sin que nadie lo notara — la flecha correcta es **humano → revisa → IA**, nunca IA → valida → humano. Una revisión humana del resultado de la IA no es visado por el solo hecho de que «le parezca bien»: el visado es un acto registrado con firma y fundamento, no una mirada.

**Identificación de quien decide:** al registrar una decisión humana, el agente pregunta las **3 iniciales** de la persona que la ejecuta. La primera vez que alguien registra una decisión en el sistema se anota su nombre completo junto a las iniciales; de ahí en adelante basta con las iniciales. Así cada firma es atribuible sin exigir trámites en cada visado.

Nota de honestidad normativa: estas decisiones reservadas son **reglas internas de gobierno del sistema**; no se presentará cada movimiento de tarjeta como una exigencia literal del art. 8° bis.

***

## 10. Estado actual del sistema y pendientes

**Punto de partida observado (25-09-2026):**

* Diseño activo: **p0.11-RC**; implementación: **i0.2**, en modo testeo (el detalle de compuertas y corridas está en `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`).

* Corpus real: Ley 19.628 consolidada completa (165 Disposiciones en Notion; en el harness, 578 unidades + 50 fragmentos, 717 archivos .md), Ley 21.719 (631 archivos) y Decreto 662 (151 archivos), fragmentadas con cotejo mecánico de literales (huellas SHA-256, 0 enlaces rotos). Artículo 14 ter pendiente.

* El paquete de `consolidacion-2026-09-24/` (hoy en el archivo histórico `_NO-USAR-primera-corrida/`) (`00-Especificacion-consolidada.md`, `01-Contratos-de-agentes-propuestos.md`, `02-Plan-de-implementacion-y-comprobaciones.md`, `05-Guia-visual-del-flujo-completo.md`) está armonizado pero **sin activación**. En cambio, `03-Prompts-canonicos-expandidos.json` y `04-Manifiesto-de-la-propuesta.json` **son anteriores a esa armonización** y el propio paquete declara que «no deben utilizarse para despachar estos contratos» hasta regenerarlos; en el JSON de prompts, Fragmentador de Fuentes aún figura con su nombre antiguo, «Investigador de Fuentes».

* En el harness vigente, **los catorce agentes tienen `PROMPT.md`**, incluido el Orquestador en carpeta propia. La presencia de un contrato no demuestra por sí sola que su mecanismo haya sido probado de extremo a extremo; el estado de testeo se registra aparte.

* Versiones sugeridas al avanzar: `p0.12-RC` (diseño) e `i0.3` (implementación); los diez roles con prompt v3 pasarían a v4; Delimitador de Dominio/Investigador de Formas de cumplimiento/Opciones de resolución y examen de antecedentes de v1 a v2 (ver D-07).

**Pendientes mayores (detalle en `/Users/mcfoix/Desktop/Gestion del Caos/informes/04-Diagnosticos-y-Desfases.md`):** ejecutar la pasada de clasificación deóntica sobre el corpus ya fragmentado (el prompt corregido del Fragmentador ya está visado y vive en su `PROMPT.md`, en la carpeta de agentes); crear el siguiente perfil de testeo; regenerar `03-Prompts-canonicos-expandidos.json` y `04-Manifiesto-de-la-propuesta.json` desde la carpeta de agentes (los actuales se conservan como antecedente y contraste — su declaración de «no despachar desde aquí» es del propio paquete); crear por el circuito Orquestador/Opciones de resolución y examen de antecedentes las dos Escaladas pendientes (D-11); y la lista de comprobaciones técnicas de la especificación consolidada (relaciones/rollups, bloques sincronizados al reorganizar, independencia real de contextos, permisos al reubicar bases).

***

## 11. Genealogía del sistema (de dónde salió cada pieza)

* **Propuesta-Spec v6 (13-09-2026):** la columna vertebral — las bases, la lógica deóntica como propiedad del dato, la regla dura de anclaje, campos estrictos vs. semánticos, Escaladas como entidad, Subítems con Implementado/Verificado, el fundamento art. 8° bis / 14 quater.

* **Taller LTDP:** la disciplina de ejecución agéntica — el Orquestador con escritura exclusiva de estados, el contrato común inyectado, la respuesta estructurada, idempotencia, reintentos acotados, checkpoints, «un error técnico no es descarte jurídico», la entidad Agrupación con su ciclo, el pase ciego, `Sin agrupación justificada`, el informe de cierre con conciliación, y el protocolo de mirrors oficiales ante fuentes no scrapeables.

* **Análisis comparativo:** la fusión — «A como columna vertebral de datos y gobernanza; de B, su disciplina de ejecución; el orquestador no es opcional». Eliminación del campo `Resultado en golden set` (calibración externa, a cargo del Equipo Legal).

* **Laboratorio (p0.9 → p0.11, i0.1 → i0.2):** la implementación real en Notion — tres contadores de versión que nunca se cruzan (diseño `p`, implementación `i`, prompts `v`), lotes por artículo completo, contrato común operativo. (Sus compuertas y excepciones de testeo son historia de las corridas: hoy viven en `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md`.)

* **Consolidación del 24-09-2026** (carpeta `consolidacion-2026-09-24`): el canon depurado — ciclo de Fuente de 7 etapas sin `Integrada`, cuatro estados de Ítem sin `Modificado`, inventario de cobertura desde el primario, `Resultado de destilación`, corrección en 9 pasos con reauditoría.

* **Harness-md-lpdp:** el modo de trabajo simple y observable — una instrucción legible por agente, resultados comprobables en archivos, registro breve del Orquestador, límites nítidos, prompts autónomos.

***

## 12. Fundamentación metodológica — de dónde viene cada pieza

Esta sección responde la pregunta «¿esto de dónde salió?» para cualquier lector — interno, auditor o fiscalizador. El diseño no se inventó: una parte viene de literatura especializada revisada, otra de hallazgos del propio material de trabajo, y la distinción importa porque cada origen tiene un modo distinto de defenderlo.

### 12.1 El estado del arte que informó el diseño

| Trabajo                   | Institución                        | Fecha     | Qué aportó al sistema                                                                                         |
| ------------------------- | ---------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| **Chain of Logic**        | Northwestern / Adobe Research      | feb. 2024 | Razonamiento sobre normas con condiciones compuestas; de aquí sale la apertura REGLA / HECHOS / CUESTIÓN      |
| **PrivComp-KG**           | UTEP / Texas A\&M                  | oct. 2024 | Comparación norma vs. política mediante grafo; de aquí sale la lógica «requerido menos cubierto»              |
| **RAGulating Compliance** | MasterControl AI Research          | ago. 2025 | Arquitectura de agentes especializados en cadena; la Exigencia como estructura, no prosa                      |
| **IoT-Reg / GDPR-KG**     | Univ. of Maryland Baltimore County | jul. 2025 | Modelado deóntico: la clasificación deóntica como propiedad del dato, y el escalamiento humano ante conflicto |
| **MSLR**                  | Shanghai Jiao Tong                 | nov. 2025 | Separación extracción/razonamiento; campos estrictos vs. semánticos                                           |
| **ComplianceNLP**         | Univ. de Hong Kong / Stellaris AI  | abr. 2026 | Detección de brechas validada con meses de operación real; tres estados de conformidad                        |

### 12.2 Lo que NO vino de la literatura

Piezas que son hallazgos del material propio de trabajo — y por eso no hay paper que las avale: se defienden con el ejemplo que las originó:

| Pieza                                           | Origen                                                                                                                                  |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Regla 5 — discrepancia de alcance               | Asimetría legislativa detectada en el material propio (listas del mismo derecho con distinto número de letras entre cuerpos normativos) |
| Regla 6 — acumulación                           | Análisis del art. 27 durante el contraste                                                                                               |
| Campo `Estado de determinación` de la Exigencia | La delegación del art. 11 letra a) («podrá ser determinada por el director»)                                                            |
| Desglose del campo Plazo                        | Las dos velocidades del art. 11: 30 días corridos prorrogables por una vez para responder la solicitud vs. 2 días hábiles para responder al requerimiento de bloqueo; no inferir «no prorrogable» de este último |
| Etapa `Delimitada` en el ciclo de Fuente        | La necesidad de registrar qué se dejó fuera, no solo qué entró                                                                          |
| Escaladas como entidad propia                   | La necesidad de saber qué desbloquea cada decisión pendiente                                                                            |

> **El material propio corrigió el diseño derivado de la literatura.** Es la validación del principio adoptado: usar trabajo real para descubrir qué estructura se necesita, en vez de fijarla primero. El detalle completo, con la tabla de origen pieza por pieza, está en la Propuesta-Spec v6, sección de metodología.

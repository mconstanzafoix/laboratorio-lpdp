---
name: calificar-sancion-exigencia
description: Examina para cada Exigencia LPDP las vías de infracción potencial y fundamenta su calificación sancionatoria, incluida No tipificada, calificación variable según conducta o examen pendiente.
---

# Calificar la sanción de una Exigencia

Esta skill se entrega íntegra en **toda ejecución del Destilador**. Se aplica a toda ficha que el agente cree o revise, y a todas las fichas de la Fuente en su cotejo final, **antes de decidir** el valor de `sancion`. Examina vínculos positivos, grados distintos según la conducta, `0 No tipificada` y casos aún pendientes: ningún valor dispensa de razonar. `sancion` es una etiqueta para filtrar, no el número de multas ni una operación aritmética. Su objeto es una **calificación normativa potencial**; no declara una infracción cometida ni calcula una multa para una organización. El `PROMPT.md` del Destilador fija los valores del campo, los archivos de salida y el alcance de Fuentes autorizado.

## Método

1. **Separa la regla y la infracción.** Reconstruye la posición jurídica de la ficha y describe la conducta hipotética que la infringiría. Si la Exigencia expresa un derecho del titular, identifica la conducta correlativa atribuible al responsable que el texto sustenta; el ejercicio del derecho por el titular no es la infracción. Distingue modalidades que podrían tener tipos diferentes: impedir el ejercicio, omitir una respuesta, incumplir una garantía o desobedecer una resolución posterior no son automáticamente la misma conducta.
2. **Identifica los tipos pertinentes.** Lee el texto sancionador de la Fuente y versión encargadas, con sus remisiones expresas relevantes. Para cada candidato, identifica grado, sujeto, verbo, objeto, presupuestos y la conducta que tipifica. Busca el tipo específico y examina también las cláusulas generales o residuales realmente aplicables; no concluyas `0 No tipificada` por no hallar el número del artículo sustantivo en el catálogo. Una norma que fija multas, agravantes o concurso no reemplaza el tipo infraccional.
3. **Haz la subsunción y su contraste.** Compara elemento por elemento la conducta hipotética con el tipo. Explica qué palabras y conexiones normativas permiten o impiden la lectura; distingue interpretación del sentido posible del tipo de analogía que extiende el castigo a una conducta distinta. Si hay dos encuadres defendibles que cambian el grado, formula la tesis, la mejor objeción y el efecto de cada alternativa. No uses una escala numérica de «peso» de indicios, una regla automática de confianza ni un tipo residual por descarte mecánico.
4. **Distingue pluralidad y concurso.** Puede haber tipos alternativos para hechos distintos, dos tipos candidatos para una misma conducta, conductas infractoras independientes relacionadas con la misma Exigencia o una multa con una consecuencia accesoria eventual. Registra cada hipótesis y sus presupuestos sin sumarlas por anticipado. Si una conducta llegara a configurar dos infracciones, examina la regla de concurso aplicable; si son conductas independientes, distínguelas. El número de tipos posibles en abstracto no determina por sí solo el número de sanciones en un caso.
5. **Decide qué afirma la etiqueta.** Registra `3 Gravísima`, `2 Grave` o `1 Leve` solo si el grado afirmado corresponde a las conductas infractoras pertinentes ya examinadas, con tipo y vínculo fundados. Registra `0 No tipificada` solo después de un examen negativo de los tipos pertinentes, incluida una cláusula residual que pudiera cubrir la infracción. Si la misma Exigencia comprende **conductas diferentes cuyas calificaciones distintas (`0`, `1`, `2` o `3`) ya están fundadas**, registra `Calificación variable según la conducta` y conserva en la ficha la correspondencia conducta → tipo o examen negativo → calificación; esa conclusión no queda «pendiente» solo por no caber en un valor único. Si aún falta el cotejo, el texto o una decisión jurídica sobre el encuadre, deja `sancion: ""` e identifica exactamente el examen o decisión pendiente. Comunica al Orquestador una duda material sobre el corte de la Exigencia; no dividas una regla solo para obtener calificaciones distintas.
   **Comprueba a qué Exigencia pertenece cada vía.** Para cada hipótesis, identifica la conducta
   que infringe esta Exigencia, los elementos adicionales del tipo y si esos elementos califican
   esa infracción o una lesión autónoma de otra Exigencia. Si un mismo hecho afecta ambas,
   enlaza la otra ficha y razona la relación y el concurso posible; no traslades su grado
   automáticamente a esta etiqueta. Una resolución o requerimiento posterior con presupuesto
   nuevo tampoco cambia por sí solo la calificación de la infracción originaria. Si dos
   adscripciones defendibles alteran el valor de `sancion`, confronta tesis, objeción y efecto;
   si no puedes resolverlo fundadamente, deja el campo vacío y localiza la duda. Esta prueba
   no predetermina el encuadre de una Exigencia particular.
   Si comparas fichas de una ley modificatoria y de la ley consolidada correspondiente,
   confronta por separado la conducta, el tipo, sus presupuestos y la atribución del grado
   a cada Exigencia. Para el mismo pasaje y período aplica el mismo método a ambas:
   identifica el elemento textual, temporal o contextual que exigiría calificaciones
   distintas. Dos análisis individuales plausibles no resuelven por sí solos esa
   diferencia. Una coincidencia textual no justifica copiar la etiqueta; si la
   diferencia sigue sin fundamento suficiente, deja el pendiente localizado y aplica
   a la ficha que examinas la regla anterior para `sancion: ""`.
6. **Distingue grado y consecuencia.** El grado es la calificación de la conducta tipificada. Multa máxima, agravantes, atenuantes, reincidencia, medidas accesorias, régimen del sujeto y vigencia requieren sus propios presupuestos y textos. Incorpóralos solo cuando estén verificados y sean pertinentes; no conviertas el máximo abstracto en sanción aplicable a un caso. Una resolución de la Agencia o un requerimiento futuro constituye un presupuesto nuevo cuando así lo exige un tipo; no es la sanción automática de la Exigencia originaria.

## Dónde queda el razonamiento

En la **misma ficha de Exigencia**, desarrolla **todo examen sancionatorio en `## Sanción`**, tanto para `3`, `2`, `1`, `0`, `Calificación variable según la conducta` como para `sancion: ""`. **Abre la sección**, antes de la tabla y del análisis extenso, con `**Por qué figura «<valor de sancion>».**` y una síntesis breve: conductas de esta Exigencia y sus grados fundados, presupuesto que modifica el grado y límite de la conclusión. Para `Calificación variable según la conducta`, nombra al menos las conductas que sostienen los grados diferentes; no uses una vía de otra Exigencia o un hecho posterior como segunda calificación propia. Si el campo está vacío, abre con `**Por qué la calificación sigue pendiente.**` y precisa la cuestión y su efecto posible. La síntesis debe concordar con el examen que sigue y no disimular una controversia material.

Después expón: conducta hipotética examinada; tipo y Disposición tipificadora enlazada, con Fuente y versión, o tipos descartados y alcance del examen negativo si asignas `0`; correspondencia de elementos; alternativa material y objeción cuando existan; conclusión sobre el grado o la ausencia fundada de tipificación; consecuencia adicional solo si está comprobada. Si existen varias vías, usa una tabla dentro del mismo apartado: `Conducta hipotética | Tipo candidato y grado, o 0 fundado | Presupuestos | Relación con las demás vías | Conclusión`. Para registrar la calificación variable, cada valor diferente de la tabla debe estar fundado; una vía meramente sugerida no basta. Si el campo queda vacío, deja aquí el cotejo realizado y el punto exacto pendiente; `## Límites del análisis` solo lo señala y remite a esta sección, sin repetir el razonamiento. No sustituyas el examen por una lista de artículos ni abras un informe sancionatorio separado. El `RESULTADO.md` explica el examen y corte de la Disposición sustantiva; la subsunción sancionatoria de la Exigencia vive en su ficha.

## Control de lectura: artículo 8 bis

El artículo reconoce al titular el derecho a oponerse y a no ser objeto de determinadas decisiones automatizadas, sujeto a las excepciones del inciso segundo, y conserva garantías en el inciso final aun cuando opere una excepción. La pregunta sancionatoria no es «¿qué grado tiene el artículo 8 bis?», sino **qué conducta de un responsable** se está calificando. Obstaculizar el ejercicio legítimo de la oposición invita a examinar el artículo 34 ter, letra e; omitir, responder incompletamente o fuera de plazo una solicitud invita a examinar el artículo 34 bis, letra c; incumplir una resolución posterior de la Agencia exige verificar los presupuestos propios del artículo 34 quáter, letra i. La conducta de tomar una decisión prohibida y la omisión de garantías del inciso final requieren análisis propio; ninguno de esos tipos se traslada automáticamente a toda la ficha del derecho. El caso enseña a separar conductas y presupuestos, no predetermina un único valor `sancion` para el artículo 8 bis ni para otras Fuentes.
El inciso final del artículo 8 bis impone al responsable un deber de medidas; el inciso primero
reconoce al titular un derecho de oposición. Si falta una medida y esa falta impide efectivamente
una oposición legítima, pueden resultar afectadas ambas reglas. Examina entonces si el tipo
grave del artículo 34 ter, letra e, califica el incumplimiento del deber de medidas, la lesión
del derecho de oposición o ambas: identifica la conducta y los elementos del tipo que sostienen
cada atribución. La coincidencia del hecho no responde por sí sola la pregunta. Conserva la
objeción defendible y su efecto sobre la etiqueta hasta poder resolverla fundadamente.

# Revisiones por cambio del harness

El Orquestador abre una ficha `REV-NNNN.md` por cambio comprobable que puede
afectar resultados anteriores. Una revisión puede enlazar varias Fuentes,
Dominios y entregas; no se abre otra ficha por cada dependencia. El Analista de
impacto devuelve la detección al Orquestador, que pregunta directamente a la
persona si autoriza analizar y registra su respuesta. Solo tras esa autorización
el Analista produce su mapa en su carpeta. El Orquestador conserva aquí la autorización,
las transiciones y el cierre; `Ejecuciones/` registra cada trabajo realizado.

Estados: `Detectada → En análisis → Impacto evaluado → En revisión →
Comprobada → Cerrada`, con salida `Cerrada sin impacto` desde la evaluación.
`Detectada` espera autorización humana para comenzar el análisis. `En revisión`
requiere una segunda autorización humana sobre el alcance a corregir. Si la
persona no autoriza o aplaza, la ficha permanece `Detectada` o `Impacto
evaluado`, según corresponda, con su respuesta literal; el silencio no mueve
el estado. Ninguna ficha se cierra con dependencias sin comprobar.

`Cerrada sin impacto` exige inventario fechado de productos anteriores e
índices accesibles. Si no había productos, la ficha documenta esa comprobación.
Si los había, enlaza el mapa del Analista y solo cierra cuando cada vía
pertinente está `Examinada sin dependencia`, con ruta y razón. Una
`Dependencia encontrada` o `No comprobada` mantiene la revisión abierta.
El cierre expresa únicamente el alcance de los resultados examinados, no la
ausencia general de efectos de la Fuente.

Cada `REV-NNNN.md` lleva al inicio: identificador; estado vigente; Fuente y
versión; cambio y evidencia localizada; fecha y origen de detección; respuesta
literal de la persona, identidad, fecha y alcance de la autorización para
analizar; mapa enlazado o motivo comprobado de que no se encargó; respuesta
literal y alcance de la autorización para revisar; Fuentes, Dominios y productos
afectados; responsable y resultado comprobado por dependencia; límites,
pendientes, historial de transiciones y fundamento del cierre. El Orquestador
actualiza esa misma ficha y el índice; los informes permanecen en las carpetas
de los agentes que los produjeron.

| ID | Cambio y evidencia | Estado | Fuente o versión | Dominios afectados | Ficha |
|---|---|---|---|---|---|

No hay revisiones abiertas al crear este índice. La primera ficha recibirá
`REV-0001`; el identificador no se reutiliza. Una detección sin impacto
comprobado conserva su ficha y motivo de cierre.

# Revisión de contratos de auditoría y concordancias · 01-10-2026

## Qué se hizo

Se revisaron en paralelo los contratos del Auditor de anclaje, del Detector de
concordancias y las dependencias del campo de confianza. El Orquestador integró
los hallazgos, retiró la escala de confianza de los contratos y documentos
canónicos activos y actualizó las instrucciones de destilación, auditoría,
investigación y agrupación. No se trabajó en Notion ni se ejecutaron los
agentes sobre el corpus.

## Decisiones operativas y motivo

- El Destilador ya no se autoevalúa con `Alta / Media / Baja`. Deja cada
  comprobación no concluida en `Límites del análisis` y en el informe global.
  El Auditor revisa independientemente el resultado; el Detector incluye todas
  las Exigencias del alcance y separa resultados no evaluables de conclusiones
  provisionales.
- `Procedencia del texto` pasó a `Incorporación normativa y vigencia`, apartado
  condicional para razonamientos adicionales sobre el efecto de una instrucción
  modificatoria o la vigencia. El anclaje y la instrucción se identifican
  siempre en `Anclajes y función` cuando corresponden.
- Una calificación `3 Gravísima / 2 Grave / 1 Leve` describe una infracción
  tipificada vinculada a la regla; no una sanción aplicada. `0 No tipificada`
  exige examen negativo fundado; vacío indica calificación pendiente.
- El Auditor trabaja en dos pases: mapa independiente preservado y luego
  contraste con el razonamiento de los productores. El Detector trabaja en
  dos modos del ciclo de Dominio; Agrupar empieza con un pase ciego preservado.
  El Orquestador comprueba ambos hitos antes de entregar los antecedentes
  reservados.

## Resultados

- `AGENTS.md` y `Orquestador/PROMPT.md`: separación de contexto y coordinación.
- `Destilador-de-Exigencias/PROMPT.md`: ficha, límites y salida sin confianza.
- `Auditor-de-anclaje/PROMPT.md`: mapa, checklist de 13 dimensiones, revisiones
  por artículo e informe global.
- `Detector-de-concordancias/PROMPT.md`: correspondencia, pase ciego y seis
  reglas de contraste con universo completo.
- `documentos-canonicos/00-Sistema-LPDP.md`,
  `01-Bases-de-Datos-y-Propiedades.md` y
  `02-Gobernanza-y-Context-Engineering.md`: reglas correspondientes.

## Comprobaciones y pendientes

Se cotejaron mecánicamente las 13 claves YAML del Destilador con las 13
propiedades canónicas que escribe y se buscó el campo de confianza en los
contratos y documentos canónicos activos: no quedaron referencias operativas.
Los registros históricos de `Ejecuciones/` conservan la terminología anterior
como antecedente, sin gobernar ejecuciones nuevas. La prueba de ejecución de
los contratos continúa en espera por instrucción del usuario.

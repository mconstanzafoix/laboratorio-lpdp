# Harness Markdown - Laboratorio LPDP

Índice del harness y fuente vigente de los prompts y skills despachables. `AGENTS.md` contiene las reglas de gobierno y el contrato común que se inyecta íntegro en cada ejecución; cada agente — incluido el Orquestador — tiene su propia carpeta con su `PROMPT.md` (14 agentes). `skills/` contiene los dos procedimientos reutilizables que el prompt del Destilador declara obligatorios; sus rutas y contenidos se cargan expresamente al despacharlo. La antigua carpeta `workspace-lpdp/` es antecedente histórico, sin sincronización bidireccional. Los documentos canónicos 00–02 viven en `../documentos-canonicos/`. Los PDF de entrada están en `Fuentes-primarias/`; `Fragmentador-de-Fuentes/Fuentes/` contiene la fragmentación, `Destilador-de-Exigencias/Resultados/` la destilación, `Escaladas/` los expedientes jurídicos y `Revisiones/` los expedientes por cambio, ambos creados por el Orquestador. **El esquema detallado de cada carpeta y el límite de archivos nuevos están en el `PROMPT.md` correspondiente**; el árbol de abajo muestra solo contenedores de primer nivel y no implica que los resultados futuros ya existan.

```text
harness-md-lpdp/
|-- AGENTS.md                                   # Reglas de gobierno + contrato común inyectable.
|-- skills/                                     # Procedimientos reutilizables cargados por contrato, no por inferencia.
|   |-- examen-intensivo-destilacion/           # Examen intensivo de dudas en destilación.
|   |   |-- SKILL.md                            # Método y condición de uso.
|   |   `-- references/casos-de-control.md     # Ejemplos consultados solo cuando ayudan al caso.
|   `-- calificar-sancion-exigencia/            # Subsunción sancionatoria de cada Exigencia.
|       `-- SKILL.md                            # Método, conclusión y destino en la ficha.
|-- Fuentes-primarias/                          # PDF normativos de entrada, separados por cuerpo y versión.
|   |-- Ley-19628-consolidada-desde-2026-12-01/ # Ley 19.628 con modificaciones incorporadas.
|   |-- Ley-21719-2024/                         # Ley 21.719 como texto modificatorio propio.
|   |-- Decreto-662-2026/                       # Decreto 662 como cuerpo separado.
|   `-- INDICE.md                               # Localización exacta de cada PDF.
|-- Ejecuciones/                                # Registros breves y fechados de ejecución.
|-- Escaladas/                                  # Expedientes de dudas jurídicas y su índice en archivos.
|   `-- INDICE.md                               # Localiza cada ESC-NNNN; no sustituye su ficha.
|-- Revisiones/                                 # Expedientes por cambio, separados de las etapas del Dominio.
|   `-- INDICE.md                               # Localiza cada REV-NNNN; no sustituye su ficha.
|-- registros/                                  # Capturas fechadas para reconstruir versiones previas.
|-- tmp/                                        # Artefactos temporales de verificación (pdfs/).
|-- Orquestador/                                # Dirige encargos, verifica escrituras, mueve etapas.
|   `-- PROMPT.md                               # Rol del Orquestador, separado de AGENTS.md.
|-- Fragmentador-de-Fuentes/                    # Recorre Fuentes artículo por artículo y crea Disposiciones.
|   |-- PROMPT.md                               # Método de inventario, análisis y cierre de fragmentación.
|   `-- Fuentes/                                # Fragmentación producida: un árbol por cuerpo y versión (3 cuerpos).
|-- Destilador-de-Exigencias/                   # Extrae Exigencias desde las Disposiciones.
|   |-- PROMPT.md                               # Extracción por Fuente, identidad EX y cobertura por artículo.
|   `-- Resultados/                             # Expedientes por Fuente y versión.
|-- Delimitador-de-Dominio/                     # Propone alcance y preguntas; analiza hechos aportados en Diagnosticar.
|   |-- PROMPT.md
|   `-- Resultados/                             # DELIMITAR.md y DIAGNOSTICAR.md por Dominio.
|-- Analista-de-impacto-de-Fuente/              # Identifica resultados afectados por cambios de Fuente.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un mapa de impacto por encargo.
|-- Auditor-de-anclaje/                         # Revisa anclajes, fidelidad y omisiones.
|   |-- PROMPT.md
|   `-- Resultados/                             # Mapa, revisiones por artículo e informe por Fuente.
|-- Detector-de-concordancias/                  # Compara Exigencias y propone Agrupaciones.
|   |-- PROMPT.md
|   `-- Resultados/                             # Investigar, pase ciego y Agrupar por Dominio.
|-- Relator-de-Agrupacion/                      # Contrasta correspondencias y relata Agrupaciones.
|   |-- PROMPT.md
|   `-- Resultados/                             # Investigar y Agrupar por Dominio.
|-- Investigador-de-Formas-de-cumplimiento/     # Investiga referentes para orientar el cumplimiento.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un archivo de referentes por encargo.
|-- Opciones-de-resolucion-y-examen-de-antecedentes/ # Examina antecedentes y prepara opciones.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un informe por encargo; no sustituye Escaladas/.
|-- Relator/                                    # Documenta formulaciones, decisiones y cierres.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un informe o remisión a ficha maestra por encargo.
|-- Agente-del-Manual/                          # Mantiene las instrucciones de uso del sistema.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un informe por encargo; Manual en su ruta maestra.
|-- Agente-de-Arquitectura/                     # Especifica y comprueba cambios estructurales.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un informe por encargo; contratos en sus rutas maestras.
|-- Diseno-del-espacio/                         # Construye páginas y vistas legibles del espacio.
|   |-- PROMPT.md
|   `-- Resultados/                             # Un informe por encargo.
`-- INDICE.md                                   # Este mapa del harness.
```

**Orden de lectura:** el Orquestador carga `AGENTS.md` y su `PROMPT.md`; al despachar al Destilador incorpora además íntegros el `PROMPT.md` de ese rol, `skills/examen-intensivo-destilacion/SKILL.md` y `skills/calificar-sancion-exigencia/SKILL.md`. El Destilador lee los casos de control solo si la duda los requiere. Los demás roles no cargan estas skills por rutina.

**Verificación del índice:** 14 carpetas de agente con `PROMPT.md` y 2 carpetas de skill con `SKILL.md` (una con referencia); entradas y rutas anteriores cotejadas contra disco el 02-10-2026. Índice desactualizado = defecto reportable.

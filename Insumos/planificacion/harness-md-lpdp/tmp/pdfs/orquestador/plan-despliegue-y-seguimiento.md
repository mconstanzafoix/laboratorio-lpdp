# Orquestador — fragmentación de tres fuentes

- Encargo humano: fragmentar íntegramente las tres fuentes con tres subagentes en paralelo. Usar Sol por presupuesto y permitir los turnos necesarios.
- Decisión operativa del Orquestador: GPT-6 Sol (`gpt-6-sol`), razonamiento `high`, un agente por PDF, sin límite artificial de artículos ni plazo de ejecución. Mantener avances en disco y reanudar cuando sea necesario.
- Método: `../Fragmentador-de-Fuentes/PROMPT.md`, aplicado al encargo por instrucción humana, sin modificar su estado general de borrador.
- Estado: tres subagentes desplegados en paralelo con GPT-6 Sol y razonamiento alto. Ejecución en curso.
- Agentes: `/root/fragmentador_ley_19628`, `/root/fragmentador_ley_21719` y `/root/fragmentador_decreto_662`.

## Asignaciones y propiedad de archivos

| Agente | Original | Carpeta exclusiva de resultados |
|---|---|---|
| Fragmentador Ley 19.628 | `../Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf` (57 páginas) | `../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/` |
| Fragmentador Ley 21.719 | `../Fuentes-primarias/Ley-21719-2024/Ley-21719_13-DIC-2024.pdf` (56 páginas) | `../Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/` |
| Fragmentador Decreto 662 | `../Fuentes-primarias/Decreto-662-2026/Decreto-662_09-SEP-2026.pdf` (10 páginas) | `../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/` |

## Instrucciones comunes de ejecución

1. Leer `AGENTS.md`, todos los Markdown de instrucciones de `Fragmentador-de-Fuentes/` y el índice de fuentes antes de trabajar. Aplicar íntegramente el prompt de Fragmentación. El usuario encargó la ejecución completa; no detenerse por el rótulo de borrador.
2. Inventariar el PDF completo antes de fragmentar. Crear y mantener `ARBOL.md`, conservando todos los artículos, subdivisiones y transitorios desde el principio. Leer cada artículo íntegro antes de decidir sus cortes. Registrar estados reales de fragmentación.
3. Crear `FUENTE.md` con identificación, versión comprobada en el PDF, original y hash, inventario compacto, método y normalizaciones. Registrar el número de página del PDF en cada unidad. Usar el original asignado sin sustituirlo por otra ley o versión. Los encabezados, notas editoriales y firmas se identifican como contexto; no inventar Disposiciones a partir de ellos.
4. Fragmentar todas las unidades normativas con archivos por artículo y subdivisiones conforme al prompt. Cada Disposición incluye literal exacto, localizador, contexto, análisis específico de su función, condiciones, excepciones y remisiones, y comprobación concreta. Evitar comentarios genéricos que sirvan para cualquier artículo. No extraer Exigencias ni emitir una auditoría independiente.
5. En textos modificatorios, preservar la jerarquía del artículo modificatorio y sus numerales/literales, distinguiéndolos de los artículos insertados o sustituidos. Conservar la instrucción de modificación y sus textos citados. En decretos aprobatorios, distinguir el acto aprobatorio del reglamento aprobado. No confundir numeraciones de distintos niveles.
6. Las herramientas pueden ayudar a extraer, generar archivos y comprobar cobertura, pero la segmentación y el análisis requieren lectura. Comprobar extracción contra páginas renderizadas, en especial columnas de notas, comillas, enumeraciones, límites entre páginas y transitorios. Resolver ambigüedades antes de marcar completo; documentar las que no puedan resolverse.
7. Antes de cerrar cada artículo, reconstruir su texto desde las unidades en orden y contrastarlo con el original. Al cerrar la fuente, comprobar inventario global, enlaces, localizadores y cobertura, e incluir el método y sus límites en `INFORME-FRAGMENTACION.md`. La cantidad de archivos no prueba la cobertura. No declarar reutilización entre fuentes sin contraste concreto.
8. Escribir solo en la carpeta asignada, su carpeta temporal `tmp/pdfs/<fuente>/` y su propio registro en `Ejecuciones/`. No modificar originales, instrucciones ni resultados de otro agente. Mantener un registro breve por fuente, actualizado al reanudar.
9. Persistir hasta completar la fuente; si un turno termina antes, informar exactamente el avance y siguiente tramo para reanudar. No imponer recortes por longitud o tiempo. Informar al Orquestador al terminar el inventario y ante impedimentos o hallazgos relevantes.

## Recursos técnicos

- Python: `/Users/mcfoix/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` (pypdf y bibliotecas del runtime).
- Herramientas auxiliares del runtime: `/Users/mcfoix/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override` y `bin/fallback`.
- Habilidad PDF: `/Users/mcfoix/.codex/plugins/cache/openai-primary-runtime/pdf/26.909.12148/skills/pdf/SKILL.md`. Trabajo de lectura de PDF y producción de Markdown; no se crean ni editan PDFs.
- El PDF de Ley 21.719 declara vigencia diferida a 01-DIC-2026 y última modificación por Ley 21.806 de 05-FEB-2026. El nombre de carpeta de entrada no sustituye esos metadatos.
- El Decreto 662 fue promulgado el 13-JUN-2025 y publicado el 09-SEP-2026. Conservar ambas fechas.

## Cierre de coordinación

Inventarios iniciales comunicados por los agentes: Ley 19.628, 83 artículos permanentes o intercalados y 3 transitorios; Ley 21.719, 3 artículos permanentes propios y 8 transitorios, con 16 numerales en el artículo primero; Decreto 662, fórmula aprobatoria sin artículo único numerado y 20 artículos reglamentarios, sin transitorios. Conteos sujetos a la comprobación final de cada entrega.

Controles del Orquestador: hashes y candidatos a encabezados en `../tmp/pdfs/orquestador/originales.json`; comprobador de existencia de entregables, estados del árbol, enlaces locales y preservación de originales en `../tmp/pdfs/orquestador/comprobar_entregas.py`. Los controles mecánicos no sustituyen la lectura normativa ni acreditan por sí solos la cobertura.

Decreto 662 entregado: [informe](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/INFORME-FRAGMENTACION.md), 20 artículos y fórmula aprobatoria; 127 fragmentos reglamentarios más el acto aprobatorio. Control adicional del Orquestador: los 128 literales aparecen en las páginas indicadas del PDF, normalizando solo espacios (`../tmp/pdfs/orquestador/literales-decreto-662.json`). Duda preservada: remisión del art. 15 inciso tercero al «inciso siguiente», cuyo contenido trata vigencia y renovación; constatada visualmente en p. 8, sin corregir ni declarar error jurídico confirmado.

Ley 21.719 entregada: [informe](../Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/INFORME-FRAGMENTACION.md), 3 artículos permanentes propios, 8 transitorios, 16 numerales modificatorios y 79 artículos reproducidos subordinados; 631 archivos de literal, incluidos contextos identificados. Se reabrió y corrigió la dependencia de dos párrafos de la letra b del artículo 16 reproducido y se actualizó la numeración posterior. El control previo del Orquestador encontró los 631 literales íntegros en las páginas declaradas. Se revisaron también localizadores completos y enlaces a introducciones de listas.

Pendiente: finalizar la Ley 19.628, comprobar entregables finales y consolidar el estado de cierre. Esta revisión de entrega no sustituye al Agente Auditor de anclaje.

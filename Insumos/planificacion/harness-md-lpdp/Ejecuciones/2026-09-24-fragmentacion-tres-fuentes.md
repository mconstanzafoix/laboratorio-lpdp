# Orquestador — fragmentación de tres fuentes

- **Estado:** completado el 24-SEP-2026. Tres subagentes Fragmentadores trabajaron en paralelo, uno por fuente; se reanudaron las revisiones necesarias y se cerraron sus entregas.
- **Decisión humana:** el usuario encargó las tres fuentes, solicitó tres subagentes paralelos y eligió Sol por presupuesto, permitiendo todos los turnos necesarios. No se desplegó ningún subagente con Astra.
- **Decisiones del Orquestador:** GPT-6 Sol (`gpt-6-sol`) con razonamiento alto (`high`); carpetas exclusivas por cuerpo y versión; aplicación del prompt del Fragmentador al encargo sin alterar su condición general de borrador. Inventario completo antes de la producción masiva, revisión temprana de muestras y comprobación final de entregables.

## Resultados

| Fuente | Cobertura | Acceso |
|---|---|---|
| Ley 19.628 consolidada desde 01-DIC-2026 | 83 artículos permanentes/intercalados y 3 transitorios; 578 unidades estructurales, con 50 fragmentos en 18 párrafos. 717 Markdown. | [Fuente](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/FUENTE.md), [árbol](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/ARBOL.md), [informe](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/INFORME-FRAGMENTACION.md) |
| Ley 21.719, versión diferida 01-DIC-2026 del PDF asignado | 3 artículos propios permanentes y 8 transitorios; 16 numerales modificatorios y 79 artículos reproducidos subordinados; 631 archivos de literal, incluidos contextos identificados. 715 Markdown. | [Fuente](../Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/FUENTE.md), [árbol](../Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/ARBOL.md), [informe](../Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/INFORME-FRAGMENTACION.md) |
| Decreto 662, versión única 09-SEP-2026 | Fórmula aprobatoria sin numeración y 20 artículos reglamentarios; 127 fragmentos del reglamento más el acto aprobatorio. 151 Markdown. | [Fuente](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/FUENTE.md), [árbol](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/ARBOL.md), [informe](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/INFORME-FRAGMENTACION.md) |

## Comprobación y correcciones

Los agentes documentaron lectura, reconstrucción y cotejos visuales en sus informes. El Orquestador comprobó los tres originales por SHA-256 (sin cambios), existencia de entregables, rutas de los árboles y enlaces internos: cero faltantes, enlaces rotos o archivos internos fuera del árbol. Todos los estados de fragmentación están completos.

El cotejo adicional de cada literal con las páginas declaradas del original dio cero incidencias finales: 628 textos del consolidado (incluye 18 madres estructurales y sus fragmentos, sin sumarlas como nuevas Disposiciones), 631 de la modificatoria y 128 del decreto. Evidencias: [control de entregas](../tmp/pdfs/orquestador/comprobacion-entregas.json) y controles de literales [Ley 19.628](../tmp/pdfs/orquestador/literales-ley-19628.json), [Ley 21.719](../tmp/pdfs/orquestador/literales-ley-21719.json), [Decreto 662](../tmp/pdfs/orquestador/literales-decreto-662.json). Estos controles mecánicos no sustituyen el análisis normativo ni una auditoría independiente.

Se corrigieron clasificaciones genéricas, denominaciones de artículos, dependencias de párrafos dentro de letras, localizadores de transitorios y dos cruces de página en fragmentos finales del consolidado. La revisión del artículo 50 distinguió confidencialidad, sanción funcionaria y responsabilidad con acción de repetición. Se conservó el texto original en todas esas correcciones. Los registros por fuente detallan sus decisiones.

## Pendientes y límites

No quedan unidades pendientes de fragmentación. Queda para examen posterior la remisión del artículo 15 inciso tercero del Decreto 662 al «inciso siguiente»: en el PDF el inciso cuarto trata vigencia y renovación; el literal se conservó y la duda se localizó, sin afirmar error jurídico confirmado. No se contrastó íntegramente el contenido de remisiones externas ni se declaró reutilización entre fuentes. Las Exigencias y la auditoría independiente corresponden a etapas posteriores.

El [plan y seguimiento de despliegue](../tmp/pdfs/orquestador/plan-despliegue-y-seguimiento.md) se conserva como antecedente operativo.

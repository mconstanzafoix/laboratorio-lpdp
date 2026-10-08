# Informe de fragmentación — Ley 19.628 consolidada desde 01-DIC-2026

## Resultado y alcance

La Fuente quedó fragmentada en 86/86 artículos `[completo]`. Se resolvieron las 69 rutas `[parcial]` identificadas en el informe anterior: 15 madres con hojas existentes se convirtieron en índices y 54 unidades mixtas se cortaron en 125 fragmentos nuevos. También se convirtieron en índices tres madres que antes repetían literal pese a figurar `[completo]`: art. 30 nonies, inc. 1, y art. 39, incs. 1 y 2. Uno de los 125 fragmentos nuevos se afinó como índice anidado con dos hojas más, para distinguir notificación y plazo en el art. 41, inc. 2, lit. f, frag. 3; son 127 archivos de fragmento nuevos, de los cuales 126 son hojas finales. Las 72 rutas preexistentes se conservaron; ninguna se renombró ni eliminó. Los cinco archivos de `articulo-01/` no recibieron escritura y las otras Fuentes quedaron fuera de este encargo.

**Cuerpo y versión:** Ley 19.628 consolidada, vigencia diferida desde 01-DIC-2026. **PDF primario:** `Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf`, 57 páginas; SHA-256 recalculado `ba9c5cb34fdecf2d76e4b8b060a7a3d5da7b1173b049fc5644d5d98ab9cf18b5`. Es el consolidado de trabajo, no la Ley 21.719 modificatoria como cuerpo propio.

## Método y controles

Se leyó el PDF con `pdfplumber` sobre la columna normativa (x=65–445 pt; y=0–750 pt para excluir el pie editorial). El cotejo normalizó sólo espacios y saltos de maquetación. Cada literal de las 126 hojas nuevas finales se localizó en la página indicada en su `control_ingreso`; las 73 concatenaciones de hojas bajo sus índices se localizaron en la secuencia del PDF, incluidas las que cruzan páginas. Antes de sustituir cada tarjeta madre, se verificó que la concatenación de los cortes reprodujera su literal previo sin cambiar palabras ni puntuación.

| Control | Resultado |
|---|---:|
| Artículos con `articulo.md` y estado `[completo]` | 86/86 |
| Unidades estructurales inventariadas | 578 |
| Índices madre conservados en su ruta preexistente | 72 |
| Índice anidado creado al afinar un fragmento | 1 |
| Archivos de fragmento existentes antes de esta ejecución | 50 |
| Archivos de fragmento creados en esta ejecución | 127 |
| Hojas nuevas vigentes al cierre | 126 |
| Archivos de fragmento que son hojas al cierre | 170 |
| Archivos de fragmento que son índices anidados al cierre | 7 |
| Archivos de Disposición con bloque espejo | 682 |
| Disposiciones con siete claves YAML, cinco secciones y campos completos | 682/682 |
| Rutas del `ARBOL.md` existentes | 841/841 |
| Enlaces Markdown internos rotos | 0 |
| Unidades `[parcial]` o `[pendiente]` al cierre | 0 |

Cada `articulo.md` enlaza sus unidades; los índices madre enlazan las hojas sin repetir el bloque espejo. Las hojas conservan la fuerza y función del texto que les corresponde. El campo deóntico `No aplica — norma no regulativa` se usa sólo para tipos no regulativos; `Sin marcador expreso` identifica hojas regulativas sin operador de fuerza explícito. Las condiciones y excepciones están en el bloque literal correspondiente o en las hojas contiguas del mismo índice, vinculadas en el análisis.

## Mapa de las 72 rutas madre

Cada fila es una ruta preexistente que ahora actúa como índice estructural. El número de hojas es inmediato; algunas hojas son, a su vez, índices de un corte más fino. Su lectura en orden reconstruye el literal de la madre.

| Índice conservado | Hojas inmediatas |
|---|---:|
| [articulo-02/inciso-01-letra-i.md](articulo-02/inciso-01-letra-i.md) | 2 |
| [articulo-03/inciso-01-letra-c-parrafo-02.md](articulo-03/inciso-01-letra-c-parrafo-02.md) | 3 |
| [articulo-08/inciso-01-letra-a.md](articulo-08/inciso-01-letra-a.md) | 2 |
| [articulo-10/inciso-05.md](articulo-10/inciso-05.md) | 2 |
| [articulo-11/inciso-01-letra-d.md](articulo-11/inciso-01-letra-d.md) | 3 |
| [articulo-11/inciso-02.md](articulo-11/inciso-02.md) | 2 |
| [articulo-11/inciso-06.md](articulo-11/inciso-06.md) | 5 |
| [articulo-11/inciso-07.md](articulo-11/inciso-07.md) | 2 |
| [articulo-13/inciso-01-letra-d.md](articulo-13/inciso-01-letra-d.md) | 2 |
| [articulo-15/inciso-06.md](articulo-15/inciso-06.md) | 2 |
| [articulo-15-bis/inciso-01.md](articulo-15-bis/inciso-01.md) | 3 |
| [articulo-15-bis/inciso-02.md](articulo-15-bis/inciso-02.md) | 2 |
| [articulo-15-bis/inciso-03-fragmento-04.md](articulo-15-bis/inciso-03-fragmento-04.md) | 2 |
| [articulo-15-bis/inciso-03.md](articulo-15-bis/inciso-03.md) | 5 |
| [articulo-15-bis/inciso-04.md](articulo-15-bis/inciso-04.md) | 3 |
| [articulo-16/inciso-02-letra-b-parrafo-02.md](articulo-16/inciso-02-letra-b-parrafo-02.md) | 2 |
| [articulo-16/inciso-02-letra-c.md](articulo-16/inciso-02-letra-c.md) | 2 |
| [articulo-16-bis/inciso-02-letra-c-fragmento-02.md](articulo-16-bis/inciso-02-letra-c-fragmento-02.md) | 2 |
| [articulo-16-bis/inciso-02-letra-c.md](articulo-16-bis/inciso-02-letra-c.md) | 2 |
| [articulo-16-quinquies/inciso-01.md](articulo-16-quinquies/inciso-01.md) | 2 |
| [articulo-16-quinquies/inciso-02.md](articulo-16-quinquies/inciso-02.md) | 3 |
| [articulo-16-quinquies/inciso-03.md](articulo-16-quinquies/inciso-03.md) | 2 |
| [articulo-17/inciso-02-fragmento-01.md](articulo-17/inciso-02-fragmento-01.md) | 2 |
| [articulo-17/inciso-02.md](articulo-17/inciso-02.md) | 2 |
| [articulo-19/inciso-02.md](articulo-19/inciso-02.md) | 3 |
| [articulo-22/inciso-01.md](articulo-22/inciso-01.md) | 3 |
| [articulo-22/inciso-03.md](articulo-22/inciso-03.md) | 3 |
| [articulo-25/inciso-03-fragmento-01.md](articulo-25/inciso-03-fragmento-01.md) | 2 |
| [articulo-25/inciso-03.md](articulo-25/inciso-03.md) | 3 |
| [articulo-25/inciso-05.md](articulo-25/inciso-05.md) | 2 |
| [articulo-28/inciso-01.md](articulo-28/inciso-01.md) | 2 |
| [articulo-28/inciso-02.md](articulo-28/inciso-02.md) | 3 |
| [articulo-28/inciso-04.md](articulo-28/inciso-04.md) | 3 |
| [articulo-30-bis/inciso-01-letra-a.md](articulo-30-bis/inciso-01-letra-a.md) | 2 |
| [articulo-30-bis/inciso-01-letra-k.md](articulo-30-bis/inciso-01-letra-k.md) | 2 |
| [articulo-30-nonies/inciso-01.md](articulo-30-nonies/inciso-01.md) | 2 |
| [articulo-30-quáter/inciso-04.md](articulo-30-quáter/inciso-04.md) | 2 |
| [articulo-30-quáter/inciso-05.md](articulo-30-quáter/inciso-05.md) | 3 |
| [articulo-30-quáter/inciso-08.md](articulo-30-quáter/inciso-08.md) | 3 |
| [articulo-32/inciso-02.md](articulo-32/inciso-02.md) | 2 |
| [articulo-32-bis/inciso-01-letra-c.md](articulo-32-bis/inciso-01-letra-c.md) | 2 |
| [articulo-32-bis/inciso-01-letra-d.md](articulo-32-bis/inciso-01-letra-d.md) | 3 |
| [articulo-35/inciso-02.md](articulo-35/inciso-02.md) | 3 |
| [articulo-36/inciso-01-numeral-4.md](articulo-36/inciso-01-numeral-4.md) | 2 |
| [articulo-39/inciso-01.md](articulo-39/inciso-01.md) | 2 |
| [articulo-39/inciso-02.md](articulo-39/inciso-02.md) | 2 |
| [articulo-41/inciso-02-letra-b.md](articulo-41/inciso-02-letra-b.md) | 2 |
| [articulo-41/inciso-02-letra-c.md](articulo-41/inciso-02-letra-c.md) | 2 |
| [articulo-41/inciso-02-letra-d.md](articulo-41/inciso-02-letra-d.md) | 3 |
| [articulo-41/inciso-02-letra-f.md](articulo-41/inciso-02-letra-f.md) | 4 |
| [articulo-41/inciso-02-letra-g.md](articulo-41/inciso-02-letra-g.md) | 4 |
| [articulo-41/inciso-02-letra-h.md](articulo-41/inciso-02-letra-h.md) | 2 |
| [articulo-42/inciso-01-letra-b.md](articulo-42/inciso-01-letra-b.md) | 3 |
| [articulo-42/inciso-01-letra-e.md](articulo-42/inciso-01-letra-e.md) | 3 |
| [articulo-42/inciso-01-letra-j.md](articulo-42/inciso-01-letra-j.md) | 2 |
| [articulo-42/inciso-01-letra-k.md](articulo-42/inciso-01-letra-k.md) | 2 |
| [articulo-42/inciso-01-letra-l.md](articulo-42/inciso-01-letra-l.md) | 2 |
| [articulo-43/inciso-01.md](articulo-43/inciso-01.md) | 2 |
| [articulo-44/inciso-03.md](articulo-44/inciso-03.md) | 2 |
| [articulo-44/inciso-07.md](articulo-44/inciso-07.md) | 2 |
| [articulo-45/inciso-01.md](articulo-45/inciso-01.md) | 2 |
| [articulo-46/inciso-01.md](articulo-46/inciso-01.md) | 2 |
| [articulo-47/inciso-02.md](articulo-47/inciso-02.md) | 2 |
| [articulo-50/inciso-02.md](articulo-50/inciso-02.md) | 2 |
| [articulo-50/inciso-03.md](articulo-50/inciso-03.md) | 2 |
| [articulo-50/inciso-04.md](articulo-50/inciso-04.md) | 2 |
| [articulo-50/inciso-08-fragmento-03.md](articulo-50/inciso-08-fragmento-03.md) | 2 |
| [articulo-50/inciso-08.md](articulo-50/inciso-08.md) | 3 |
| [articulo-53/inciso-02.md](articulo-53/inciso-02.md) | 2 |
| [articulo-54/inciso-01-fragmento-03.md](articulo-54/inciso-01-fragmento-03.md) | 2 |
| [articulo-54/inciso-01.md](articulo-54/inciso-01.md) | 3 |
| [articulo-54/inciso-02.md](articulo-54/inciso-02.md) | 3 |

**Índice anidado creado durante la revisión:** [art. 41, inc. 2, lit. f, frag. 3](articulo-41/inciso-02-letra-f-fragmento-03.md), con dos hojas. Está subordinado al índice preexistente de la letra f y no se suma a las 72 rutas originales de la tabla.

## Remisiones, observaciones y límites

Se conservaron las remisiones y excepciones del literal: entre otras, las del art. 10, inc. 5, al art. 28, inc. 4; las de los arts. 16 y 16 bis sobre datos sensibles; las de los arts. 27 y 28 sobre transferencias; y las de los arts. 41 a 43 sobre tutela, sanción y reclamo. No se cotejó el contenido de los cuerpos externos mencionados por la ley ni se extrajeron Exigencias.

Se mantiene como **observación textual**, sin resolverla jurídicamente, que el art. 16 quáter, inc. 5, usa «mayores de catorce y menores de dieciocho»; el alcance preciso de la frontera de catorce años requiere examen humano si llega a ser relevante para una decisión. El art. 3° transitorio conserva la puntuación final anómala del PDF. Ninguna de estas observaciones impide localizar o fragmentar el texto. No se convirtió un fallo de acceso en descarte jurídico.

El informe anterior, cerrado el 01-OCT-2026 a las 00:08:27 -03, registraba 69 clasificaciones parciales en 32 artículos; la presente ejecución resolvió su representación sin cambiar de cuerpo ni versión. Esta entrega es una propuesta de fragmentación, no un visado jurídico ni una auditoría independiente.

🤖 **Generado por Agente Fragmentador de Fuentes v[s. f.]** (`Fragmentador-de-Fuentes/PROMPT.md`, copia sin fecha de versión).

⏳ **Estado de propuesta:** pendiente de revisión humana; no equivale a los estados jurídicos reservados.

✍️ **Escritura exclusiva del validador:** ____________________

Cierre documental: 01-OCT-2026, 00:48:40 -03.

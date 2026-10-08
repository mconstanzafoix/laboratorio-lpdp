# Escaladas del harness

Registro maestro en archivos durante la fase de trabajo en `planificacion/`.
El Orquestador es el único agente que crea las fichas y mantiene sus datos
técnicos. Registra una decisión jurídica solo si la persona la aportó con
identidad, fecha y fundamento; nunca la decide por cuenta propia.
Una duda jurídica distinta conserva una ficha `ESC-NNNN.md`; varios hallazgos
pueden vincularse a la misma ficha si plantean la misma cuestión. El informe
del agente de Opciones es antecedente de análisis, no sustituye esta ficha.

| ID | Cuestión | Estado | Origen principal | Ficha |
| --- | --- | --- | --- | --- |
| ESC-0001 | Alcance de la excepción de cobro remitida al artículo 28 inciso cuarto | Detectada | [Ley 19.628 art. 10 inc. 5, frag. 2](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-10/inciso-05-fragmento-02.md) | [ESC-0001](ESC-0001.md) |
| ESC-0002 | Destino del registro citado por el artículo 15 inciso tercero del Decreto 662 | Opciones propuestas | [Art. 15 inc. 3](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/articulo-15/inciso-3.md) | [ESC-0002](ESC-0002.md) |
| ESC-0003 | Relación entre las vías contractual y reglamentaria del programa de cumplimiento | Opciones propuestas | [Ley 19.628 art. 49 inc. 3](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-49/inciso-03.md) | [ESC-0003](ESC-0003.md) |
| ESC-0004 | Nexo de la resolución judicial ejecutoriada con el término de certificación | Opciones propuestas | [Art. 16 enunciado](../Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09/articulo-16/enunciado.md) | [ESC-0004](ESC-0004.md) |
| ESC-0005 | Régimen del artículo 16 quáter para quien tiene exactamente catorce años | Opciones propuestas | [Ley 19.628 art. 16 quáter completo](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-16-quáter/articulo.md) | [ESC-0005](ESC-0005.md) |
| ESC-0006 | Excepción de comunicación tras rectificación entre artículos 6 y 11 | Opciones propuestas | [Ley 19.628 art. 11 inc. 7 frag. 2](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-11/inciso-07-fragmento-02.md) | [ESC-0006](ESC-0006.md) |

**Identidad:** el Orquestador usa el siguiente `ESC-NNNN` libre, empezando en
`ESC-0001`; no renumera ni reutiliza un ID. Comprueba este índice y los
archivos antes de asignarlo y serializa la creación. El ID nombra la entidad,
no una versión del archivo. Al reanudar, concilia índice y fichas; una fila
sin ficha o una ficha sin fila es un pendiente técnico, nunca un descarte de
la cuestión jurídica.

**Contenido mínimo de cada ficha:** ID y enunciado preciso; tipo y estado;
fecha real de apertura; hallazgo y localizador de origen; Fuente(s) y
versión(es), Disposición(es) y Exigencia(s) si existen; informe de antecedentes
y opciones con sección pertinente; relaciones `Nace de`, `Bloquea`, `Afecta`,
Dominios y responsables de actuación cuando existan; límites y pendientes;
espacio de decisión humana (opción, autor, fecha, fundamento y razón sobre
alternativas no elegidas); condiciones de reutilización; historial de cambios;
y evidencia de cierre o desbloqueo. Si una relación aún no existe, escribe
`No consta` o `No aplica` con motivo, sin crear objetos ficticios. El estado
inicial es `Detectada`; el Orquestador aplica `Opciones propuestas` solo tras
comprobar el informe. `Decidida` exige decisión humana registrada; `Superada
o desbloqueada` exige comprobar los efectos y dependencias afectados.

El procedimiento y las reservas de decisión están en
`../Orquestador/PROMPT.md` y `../../documentos-canonicos/00-Sistema-LPDP.md`
§6.4. Este índice localiza expedientes; no duplica sus fundamentos.

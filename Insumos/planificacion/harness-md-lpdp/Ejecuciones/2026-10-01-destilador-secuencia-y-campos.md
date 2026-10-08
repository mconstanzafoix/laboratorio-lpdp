# Destilador · secuencia y campos · 01-10-2026

## Qué se hizo

Se revisó el contrato del Destilador de Exigencias por autosuficiencia y orden
de ejecución. Se definieron anclaje y remisión dentro del prompt; se sustituyó
«remisión estática» por la distinción operativa entre referencia a contenido
ya fijado y atribución expresa para concretarlo. La extracción quedó ordenada
por artículo en cinco pasos. Las trece claves YAML se explican por separado.

## Decisiones operativas

- Un anclaje identifica una Disposición concreta, su cuerpo, versión,
  identificador, localizador, archivo y función para la regla. El principal
  expresa la regla en la Fuente encargada. La remisión externa sin ficha de
  Disposición comprobada se cita como contexto, sin fingir una relación.
- La lectura y reconstrucción preceden al corte; la escritura de fichas y filas
  ocurre una sola vez después de determinarlo. El control de integridad por
  artículo y Fuente sigue en la sección de comprobación.
- El método conserva juntos los componentes de una posición normativa,
  separa conductas o efectos autónomos, evita duplicar derechos y deberes
  estrictamente correlativos y localiza los cortes discutibles.
- La Fuente modificatoria y la consolidada mantienen fichas independientes
  aunque compartan texto.

## Resultados

- `Destilador-de-Exigencias/PROMPT.md`.
- `documentos-canonicos/00-Sistema-LPDP.md`.
- `documentos-canonicos/01-Bases-de-Datos-y-Propiedades.md`.

## Comprobación y pendiente

Se verificó que las trece claves YAML coinciden con las trece explicaciones
individuales y con los slugs canónicos. No se ejecutó el agente sobre una
Fuente, de acuerdo con la pausa de pruebas indicada por el usuario.
La semántica cerrada del campo heredado `caracter`
(`Obligatoria / Condicional / Transversal`), en especial para permisos y
derechos, requiere una decisión canónica separada antes de afirmarlo como
clasificación jurídica determinista.

## Continuación · procedencia del artículo y relaciones entre artículos

Se aclaró que el artículo recorrido procede del `ARBOL.md` de la Fuente y versión
encargadas, en la carpeta del Fragmentador; `articulo.md` orienta sobre la
estructura y los archivos de Disposición conservan el texto literal. La
comprobación inicial revisa existencia y estructura; la lectura jurídica se
hace una vez durante la extracción.

La unidad de recorrido es el artículo, pero una Exigencia puede integrar
Disposiciones de varios artículos de la **misma Fuente**. Durante la destilación,
un artículo posterior puede completar la ficha anterior sin generar otra
Exigencia; se actualizan las filas pertinentes. Tras recorrer la Fuente, el
Destilador hace un cotejo transversal de las fichas existentes. El informe
global solo concilia y enlaza esos resultados: no crea un segundo catálogo ni
Agrupaciones del ciclo de Dominio. Un cambio material posterior al cierre de
la destilación vuelve al Orquestador para revisar dependencias.

Se armonizaron el prompt del Orquestador y los documentos canónicos
`00-Sistema-LPDP.md` y `01-Bases-de-Datos-y-Propiedades.md`. No se ejecutó la
destilación sobre una Fuente.

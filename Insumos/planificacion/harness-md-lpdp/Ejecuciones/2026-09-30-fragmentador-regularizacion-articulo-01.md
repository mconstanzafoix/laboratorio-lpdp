# Fragmentador de Fuentes — regularización piloto del artículo 1°

- **Tarea y alcance:** regularizar solo los cuatro archivos de Disposición de `Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01/` al `PROMPT.md` vigente. El artículo, el árbol, la ficha de Fuente y el informe global quedaron intactos.
- **Qué hizo:** sustituyó los metadatos y el análisis anteriores por las siete claves YAML y las cinco secciones vigentes. Conservó byte a byte la línea de texto literal de cada archivo, su ruta y la división de cuatro incisos.
- **Decisión operativa del agente:** asignó un tipo y una clasificación deóntica por inciso según sus marcadores expresos. El inciso segundo contiene el mandato «debe respetar» y una declaración de sujeción al régimen; se clasificó `Regulativa / Obligación` por ese mandato, sin cambiar la división fijada para el piloto. Esta clasificación es del agente, no una decisión humana.

| Unidad procesada | Tipo de norma | Clasificación deóntica |
|---|---|---|
| [inciso-01.md](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01/inciso-01.md) | Declarativa | No aplica — norma no regulativa |
| [inciso-02.md](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01/inciso-02.md) | Regulativa | Obligación |
| [inciso-03.md](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01/inciso-03.md) | Delimitadora de aplicación | No aplica — norma no regulativa |
| [inciso-04.md](../Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01/inciso-04.md) | Delimitadora de aplicación | No aplica — norma no regulativa |

- **Comprobaciones efectuadas en esta ejecución:** se leyó el artículo completo en la página 1 del PDF primario de la Ley 19.628 consolidada; se cotejó cada literal contra su columna normativa extraída con pdfplumber y se verificó el orden y el localizador. La concatenación de los cuatro literales coincidió exactamente con el artículo entre su encabezado y el inicio del artículo 1° bis, tras normalizar solo espacios (1.159 caracteres). Se releyeron los cuatro archivos escritos: siete claves previstas, cinco títulos de sección vigentes y enlaces internos existentes.
- **Hallazgos y dudas:** no se detectó duda de transcripción, localizador o clasificación que requiera examen jurídico. El inciso tercero remite al artículo 19, N° 12, de la Constitución y a las leyes que menciona, sin identificar esas leyes; no se suplió ese destino con una norma supuesta.
- **Pendiente:** revisión humana de este piloto antes de cualquier regularización de otros artículos. No se registra visado ni decisión humana sobre el contenido.

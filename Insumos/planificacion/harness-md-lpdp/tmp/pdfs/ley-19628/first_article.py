import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01/articulo-01'
PDF = 'Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
a = json.loads((Path(__file__).parent/'segments.json').read_text())[0]
OUT.mkdir(parents=True, exist_ok=True)
descs = [
    ('Delimitación del objeto', 'Define el objeto regulatorio: las condiciones de tratamiento y protección de datos personales de personas naturales. Vincula ese objeto con el artículo 19 N° 4 de la Constitución. Es una regla de alcance, no una autorización concreta para tratar datos.', 'El objeto se limita a datos personales de personas naturales; la referencia constitucional encuadra la protección.'),
    ('Regla de sujeción', 'Somete a la ley todo tratamiento de datos personales realizado por personas naturales, jurídicas u órganos públicos e impone respeto de derechos y libertades de las personas.', 'La universalidad de la sujeción depende de que haya tratamiento de datos personales; los órganos públicos quedan expresamente incluidos.'),
    ('Exclusión de ámbito con sujeción expresa de otros tratamientos de los medios', 'Excluye del régimen el tratamiento efectuado en ejercicio de las libertades de emitir opinión e informar reguladas por las leyes a que remite la Constitución. Mantiene sujetos a la ley a los medios cuando tratan datos con una finalidad distinta.', 'La exclusión depende de la finalidad y del ejercicio de esas libertades; no cubre todo tratamiento que realice un medio de comunicación.'),
    ('Exclusión de ámbito por actividades personales', 'Excluye el tratamiento efectuado por personas naturales en relación con sus actividades personales.', 'El límite depende del carácter personal de la actividad y de que el tratamiento lo haga una persona natural.'),
]
for i,(name,analysis,scope) in enumerate(descs,1):
    b=a['blocks'][i-1]
    txt=f'''# Artículo 1°, inciso {i} — {name}

- **Fuente:** Ley 19.628, texto consolidado BCN con vigencia diferida desde 01-DIC-2026; última modificación indicada: Ley 21.719 (13-DIC-2024).
- **Localizador:** artículo 1°, inciso {i}; [artículo](articulo.md) y [unidad anterior]({f'inciso-{i-1:02}.md' if i>1 else 'articulo.md'}) / [unidad siguiente]({f'inciso-{i+1:02}.md' if i<4 else 'articulo.md'}).
- **Original:** `{PDF}`, página 1 del PDF.

## Texto literal

> {b['text']}

Se normalizaron únicamente los espacios y saltos de línea propios de la maquetación del PDF; palabras y puntuación se conservaron.

## Análisis normativo

**Función propuesta:** {name.lower()}. {analysis}

**Condiciones, excepciones y alcance:** {scope}

**Remisiones:** {'artículo 19 N° 4 de la Constitución Política de la República.' if i==1 else 'Artículo 19 N° 12 de la Constitución Política de la República y las leyes que regulan las libertades allí referidas.' if i==3 else 'No contiene remisión expresa.'}

## Comprobación

Se contrastó este inciso con el artículo 1° íntegro de la página 1 y con los incisos contiguos. La exclusión del inciso tercero y la del cuarto se mantuvieron separadas por sus supuestos distintos. No se observó duda de transcripción en esta unidad. Esta comprobación es de fragmentación, no una auditoría independiente ni extracción de Exigencias.
'''
    (OUT/f'inciso-{i:02}.md').write_text(txt,encoding='utf-8')
header='''# Artículo 1° — Objeto y ámbito de aplicación

- **Fuente y versión:** Ley 19.628, texto consolidado BCN con vigencia diferida desde 01-DIC-2026; última modificación indicada: 13-DIC-2024, Ley 21.719.
- **Original:** `'''+PDF+'''`, página 1 del PDF.
- **Ubicación sistemática:** Título Preliminar, Disposiciones generales.

El artículo fija el objeto y la sujeción general de los tratamientos, y delimita dos exclusiones: el ejercicio de las libertades de opinión e información y las actividades personales de personas naturales. La segunda oración del inciso tercero devuelve al régimen los tratamientos de los medios con finalidad distinta de opinar e informar; debe leerse junto con la exclusión que la precede.

## Estructura y unidades

1. [Inciso primero](inciso-01.md): objeto y referencia constitucional.
2. [Inciso segundo](inciso-02.md): sujeción general, incluidos órganos públicos.
3. [Inciso tercero](inciso-03.md): libertades de opinión e información, con regla particular para medios.
4. [Inciso cuarto](inciso-04.md): actividades personales de personas naturales.

**Control de cobertura:** cuatro incisos en el mismo orden del original; todos tienen archivo y página. Se cotejó el comienzo del artículo siguiente para fijar el límite. Sin pendiente de fragmentación.
'''
(OUT/'articulo.md').write_text(header,encoding='utf-8')

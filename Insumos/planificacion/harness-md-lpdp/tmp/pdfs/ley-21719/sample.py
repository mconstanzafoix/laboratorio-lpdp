import json
from pathlib import Path
b=json.load(open('tmp/pdfs/ley-21719/blocks.json'))
root=Path('Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01/articulo-primero')
orig='Fuentes-primarias/Ley-21719-2024/Ley-21719_13-DIC-2024.pdf'

def write(rel, title, idx, local, analysis, context, conditions, refs):
 x=b[idx]; p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
 pages=', '.join(map(str,x['pages']))
 p.write_text(f'''# {title}

- **Fuente:** Ley N° 21.719, versión con vigencia diferida desde 01-DIC-2026, modificada por Ley N° 21.806 el 05-FEB-2026.
- **Localizador:** {local}.
- **Documento primario:** `{orig}`, página(s) PDF {pages}.
- **Contexto jerárquico:** {context}

## Texto literal

> {x['text']}

Se normalizaron únicamente los espacios y saltos de renglón de la maquetación. Se conservaron palabras, puntuación y comillas visibles.

## Análisis de fragmentación

{analysis}

- **Condiciones y excepciones:** {conditions}
- **Remisiones:** {refs}

## Comprobación

El literal se cotejó con el bloque íntegro del artículo reproducido y con las páginas PDF indicadas; su posición se conserva en la secuencia del numeral. La valoración independiente de anclaje y la extracción de Exigencias quedan fuera de esta etapa.
''',encoding='utf-8')
write('instruccion-general.md','Artículo primero: instrucción general',0,'artículo primero, encabezamiento','Mandato legislativo introductorio: abre las modificaciones a la Ley N° 19.628. Su efecto depende de los dieciséis numerales posteriores; no constituye el texto de un artículo insertado de esa ley.','Artículo primero permanente de la Ley N° 21.719; precede a los numerales 1 a 16.','Los cambios concretos se especifican en cada numeral.','Ley N° 19.628, sobre protección de la vida privada.')
write('numeral-01/instruccion.md','Numeral 1: sustitución del nombre de la ley',1,'artículo primero, numeral 1','Modificación textual del nombre de la Ley N° 19.628: sustituye exactamente «LA VIDA PRIVADA» por «LOS DATOS PERSONALES». El numeral opera sobre el título, no añade una regla de tratamiento al articulado.','Artículo primero permanente, numeral 1.','Se limita a la frase identificada del nombre de la ley.','Nombre de la Ley N° 19.628.')
write('numeral-02/instruccion.md','Numeral 2: reemplazo del artículo 1°',2,'artículo primero, numeral 2','Instrucción modificatoria de sustitución integral del artículo 1° de la Ley N° 19.628. Los cuatro párrafos del texto nuevo siguen en archivos propios bajo este numeral; la instrucción no se confunde con ese artículo reproducido.','Artículo primero permanente, numeral 2; el texto reproducido pertenece a la Ley N° 19.628.','El alcance es el reemplazo completo del artículo 1°, no sólo un inciso.','Artículo 1° de la Ley N° 19.628.')
analyses=[
('Objeto y ámbito inicial','Define el objeto del régimen de tratamiento y protección de datos personales de personas naturales y lo vincula con la garantía constitucional indicada. Es el inciso primero del artículo 1° que el numeral 2 reemplaza.','El objeto se formula para datos de personas naturales y conforme a la garantía constitucional.','Artículo 19, N° 4, de la Constitución Política de la República.'),
('Sujeción general al régimen','Impone a quienes tratan datos personales, incluidos los órganos públicos, respetar derechos y libertades y someterse a esta ley. La amplitud del sujeto está expresada en «persona natural o jurídica».','Se activa ante todo tratamiento de datos personales por los sujetos señalados.','Esta ley (Ley N° 19.628 en su texto reemplazado).'),
('Excepción relativa a opinión e información','Excluye del régimen el tratamiento realizado en ejercicio de las libertades de opinar e informar, pero somete a los medios de comunicación cuando tratan datos para otra finalidad. Ambas cláusulas deben leerse juntas para no extender la excepción a tratamientos ajenos a esas libertades.','Excepción condicionada a la finalidad de opinar o informar; hay aplicación de la ley si la finalidad del medio es distinta.','Artículo 19, N° 12, de la Constitución Política de la República y leyes que regulan esas libertades.'),
('Excepción de actividades personales','Excluye el tratamiento efectuado por personas naturales en relación con sus actividades personales. La condición subjetiva y la finalidad personal delimitan esta excepción.','Debe tratarse de una persona natural actuando en relación con sus actividades personales.','Normas de la Ley N° 19.628 reemplazada.')]
for j,idx in enumerate(range(3,7),1):
 name,an,cond,refs=analyses[j-1]
 write(f'numeral-02/articulo-reproducido-01/inciso-{j:02}.md',f'Artículo 1° reproducido, inciso {j}: {name}',idx,f'artículo primero, numeral 2, artículo 1° reproducido, inciso {j}',an,'Texto completo del artículo 1° sustituido por el numeral 2; este inciso se lee junto a los otros tres. '+('La comilla inicial abre el texto reproducido.' if j==1 else 'La comilla final cierra el texto reproducido.' if j==4 else ''),cond,refs)
(root/'articulo.md').write_text('''# Artículo primero permanente de la Ley N° 21.719

Modifica la Ley N° 19.628 mediante dieciséis numerales. La [instrucción general](instruccion-general.md) abre la serie. Cada numeral conserva su mandato de cambio y, cuando lo hay, el texto reproducido de la ley modificada en una jerarquía separada.

- [Numeral 1](numeral-01/instruccion.md): sustituye una frase del nombre de la ley.
- [Numeral 2](numeral-02/instruccion.md): reemplaza el artículo 1°; [texto reproducido, incisos 1 a 4](numeral-02/articulo-reproducido-01/articulo.md).
- Numerales 3 a 16: véase `ARBOL.md`; se completan en esta intervención.
''',encoding='utf-8')
(root/'numeral-02/articulo-reproducido-01/articulo.md').write_text('''# Artículo 1° de la Ley N° 19.628, reproducido por el numeral 2

El [numeral 2](../instruccion.md) ordena el reemplazo íntegro de este artículo. No es un artículo propio de la Ley N° 21.719. El texto contiene objeto y ámbito de aplicación, sujeción general, excepción de opinión e información y excepción de actividades personales.

- [Inciso 1](inciso-01.md)
- [Inciso 2](inciso-02.md)
- [Inciso 3](inciso-03.md)
- [Inciso 4](inciso-04.md)
''',encoding='utf-8')
print('sample files',sum(1 for _ in root.rglob('*.md')))

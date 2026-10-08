import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEST = ROOT / 'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01'
PDF = ROOT / 'Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
ART_RE = re.compile(r'^Artículo\s+\d+[°º]?(?:\s+(?:bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?\.-\s*')
LETTER = re.compile(r'^([a-zñ])\)\s+')
NUMERAL = re.compile(r'^(\d+)\.\s+')
ROMAN = re.compile(r'^([ivx]+)\.\s+')

arts = json.loads((HERE/'segments.json').read_text(encoding='utf-8'))

def art_slug(a):
    return ('transitorio-' if a['transitory'] else 'articulo-') + f"{a['num']:02}" + (('-'+a['suffix']) if a['suffix'] else '')

def art_label(a):
    printed = re.match(r'^(Artículo\s+[^.]+)\.-',a['blocks'][0]['text']).group(1)
    return printed + (' transitorio' if a['transitory'] else '')

def kind(text):
    if LETTER.match(text): return 'letra', LETTER.match(text).group(1)
    if ROMAN.match(text): return 'ordinal', ROMAN.match(text).group(1)
    if NUMERAL.match(text): return 'numeral', NUMERAL.match(text).group(1)
    return None, None

def next_explicit(blocks, index):
    for b in blocks[index+1:]:
        k, v = kind(b['text'])
        if k: return k, v
    return None, None

def sequential(prev, nxt):
    if prev is None or nxt is None: return False
    pk,pv = prev; nk,nv = nxt
    if pk != nk: return False
    if pk == 'letra':
        alphabet = 'abcdefghijklmnñopqrstuvwxyz'
        return alphabet.index(nv) == alphabet.index(pv)+1
    if pk == 'numeral': return int(nv) == int(pv)+1
    romans = ['i','ii','iii','iv','v','vi','vii','viii','ix','x']
    return romans.index(nv) == romans.index(pv)+1

for a in arts:
    blocks=a['blocks']
    inc=0
    prev_enum=None
    para_count={}
    for i,b in enumerate(blocks):
        k,v=kind(b['text'])
        if i == 0:
            inc=1; b['label']='inciso primero'; b['name']='inciso-01'; b['depth']=1
        elif k:
            prefix={'letra':'letra','ordinal':'ordinal','numeral':'numeral'}[k]
            b['label']=f'{prefix} {v} del inciso {inc}'
            b['name']=f'inciso-{inc:02}-{prefix}-{v}'
            b['depth']=2
            prev_enum=(k,v)
            para_count[b['name']]=1
        elif prev_enum and sequential(prev_enum,next_explicit(blocks,i)):
            enum_name=f"inciso-{inc:02}-{prev_enum[0]}-{prev_enum[1]}"
            para_count[enum_name]=para_count.get(enum_name,1)+1
            b['label']=f'párrafo {para_count[enum_name]} de {prev_enum[0]} {prev_enum[1]}'
            b['name']=f'{enum_name}-parrafo-{para_count[enum_name]:02}'
            b['depth']=3
        else:
            inc+=1; b['label']=f'inciso {inc}'; b['name']=f'inciso-{inc:02}'; b['depth']=1
            prev_enum=None
        b['path']=art_slug(a)+'/'+b['name']+'.md'

# El artículo 16 contiene ordinales subordinados específicamente a la letra b),
# seguidos por dos párrafos que concluyen esa misma letra antes de la letra c).
for a in arts:
    if a['num']==16 and not a['suffix'] and not a['transitory']:
        for b in a['blocks']:
            if b['text'].startswith(('i. ','ii. ','iii. ','iv. ','v. ')):
                ordinal=b['text'].split('.',1)[0]
                b['label']=f'ordinal {ordinal} de la letra b del inciso 2'
                b['name']=f'inciso-02-letra-b-ordinal-{ordinal}'
                b['depth']=3
            elif b['text'].startswith('Cumpliéndose estas condiciones,'):
                b['label']='párrafo 2 de la letra b del inciso 2'
                b['name']='inciso-02-letra-b-parrafo-02'
                b['depth']=3
            elif b['text'].startswith('Cuando un integrante de la persona jurídica'):
                b['label']='párrafo 3 de la letra b del inciso 2'
                b['name']='inciso-02-letra-b-parrafo-03'
                b['depth']=3
            elif b['text'].startswith(('c) ','d) ','e) ','f) ')):
                letter=b['text'][0]
                b['label']=f'letra {letter} del inciso 2'
                b['name']=f'inciso-02-letra-{letter}'
                b['depth']=2
            elif b['text'].startswith('Las excepciones para tratar datos sin consentimiento,'):
                b['label']='inciso 3'
                b['name']='inciso-03'
                b['depth']=1
            b['path']=art_slug(a)+'/'+b['name']+'.md'

(HERE/'inventory.json').write_text(json.dumps(arts,ensure_ascii=False,indent=2),encoding='utf-8')

def section(a):
    n=a['num']; suf=a['suffix']
    if a['transitory']: return 'Disposiciones transitorias'
    if n<=3: return 'Título Preliminar — Disposiciones generales'
    if n<=11: return 'Título I — De los derechos del titular de datos personales'
    if n<=16:
        title='Título II — Del tratamiento de los datos personales y de las categorías especiales de datos'
        if n<=15: return title+' / Párrafo Primero — Del consentimiento del titular, de las obligaciones y deberes del responsable y del tratamiento de datos en general.'
        if suf in ('quáter','quinquies','sexies'): return title+' / Párrafo Tercero — Del tratamiento de categorías especiales de datos personales'
        return title+' / Párrafo Segundo — Del tratamiento de los datos personales sensibles'
    if n<=19: return 'Título III — De la utilización de datos personales relativos a obligaciones de carácter económico, financiero, bancario o comercial'
    if n<=26: return 'Título IV — Del tratamiento de datos personales por los órganos públicos'
    if n<=29: return 'Título V — De la transferencia internacional de datos personales'
    if n<=32: return 'Título VI — Autoridad de Control en materia de Protección de Datos Personales'
    if n==33: return 'Título VII — De las infracciones y sus sanciones, de los procedimientos y de las responsabilidades'
    if n<=40: return 'Título VII, Párrafo Primero — De la responsabilidad, las infracciones y las sanciones aplicables a las personas naturales o jurídicas de derecho privado'
    if n<=42: return 'Título VII, Párrafo Segundo — De los procedimientos administrativos'
    if n==43: return 'Título VII, Párrafo Tercero — Del procedimiento de reclamación judicial'
    if n<=46: return 'Título VII, Párrafo Cuarto — De la responsabilidad de los órganos públicos, de la autoridad o jefe superior del órgano y de sus funcionarios'
    if n<=53: return 'Título VII, Párrafo Quinto — De la responsabilidad civil'
    return 'Título VIII — Del tratamiento de datos personales por el Congreso Nacional, el Poder Judicial y organismos públicos dotados de autonomía constitucional'

tree=['# Árbol de la Ley 19.628 consolidada desde 01-DIC-2026','',
      f'Original: `{PDF.relative_to(ROOT)}`. El árbol enumera los 83 artículos permanentes o intercalados y los 3 artículos transitorios del PDF. Los rótulos de incisos identifican párrafos tipográficos; las letras, ordinales y numerales conservan sus marcas impresas. Los encabezados sistemáticos son contexto.','',
      'Estados: `[pendiente]`, `[parcial]`, `[completo]` describen únicamente la fragmentación. En esta primera materialización, solo el artículo 1° está comprobado.','',
      '```text', 'Ley 19.628 — consolidado BCN con vigencia diferida desde 01-DIC-2026']
old_section=None
for a in arts:
    sec=section(a)
    if sec != old_section:
        tree.append(f'|-- {sec} [contexto]')
        old_section=sec
    state='completo' if a['num']==1 and not a['suffix'] and not a['transitory'] else 'pendiente'
    label=art_label(a)
    path=art_slug(a)+'/articulo.md'
    tree.append(f'|   |-- {label} [{state}] -> {path}')
    for b in a['blocks']:
        frag=b['text']
        frag=ART_RE.sub('',frag) if b is a['blocks'][0] else frag
        frag=frag[:82]+('…' if len(frag)>82 else '')
        indentation='|   |   ' if b['depth']==1 else '|   |       ' if b['depth']==2 else '|   |           '
        tree.append(f"{indentation}|-- {b['label']} [{state}] -> {b['path']}  # {frag}")
tree += ['```','',
         'Las remisiones internas se conservan en cada literal. La jerarquía de párrafos dentro de letras se indica cuando el mismo literal continúa antes de la letra siguiente. Los rótulos de inciso se refieren a la secuencia de párrafos principales usada para localizar las unidades; no alteran la numeración impresa. El artículo 1° transitorio y los demás transitorios tienen rutas distintas de los artículos ordinarios homónimos.']
DEST.mkdir(parents=True,exist_ok=True)
(DEST/'ARBOL.md').write_text('\n'.join(tree)+'\n',encoding='utf-8')

compact=[]
for a in arts:
    compact.append(f"[{art_label(a)}]({art_slug(a)}/articulo.md) ({a['blocks'][0]['pages'][0]}–{a['blocks'][-1]['pages'][-1]})")
meta=f'''# Fuente — Ley 19.628 consolidada desde 01-DIC-2026

- **Cuerpo:** Ley 19.628, sobre protección de los datos personales.
- **Original exacto:** `{PDF.relative_to(ROOT)}`.
- **SHA-256 del PDF:** `{hashlib.sha256(PDF.read_bytes()).hexdigest()}`.
- **Edición:** Biblioteca del Congreso Nacional de Chile, documento generado el 22-SEP-2026, 57 páginas. Portada: publicación 28-AGO-1999, promulgación 18-AGO-1999, «Versión: Con Vigencia Diferida por Fecha De : 01-DIC-2026», última modificación 13-DIC-2024, Ley 21719.
- **Separación de fuentes:** este es el texto consolidado de Ley 19.628. La Ley 21.719 modificatoria constituye otra fuente y no se ha sustituido por ella.
- **Inventario:** 83 artículos permanentes o intercalados y 3 transitorios, 86 en total; 578 párrafos o literales preliminares localizados. [Árbol completo](ARBOL.md).

## Inventario compacto

{'; '.join(compact)}.

## Método y alcance

Se extrajo el texto de las páginas del PDF conservando únicamente la columna normativa (coordenadas horizontales 65–445 pt) y se cotejó con páginas renderizadas. Se normalizan espacios y saltos de línea de maquetación, sin reescribir palabras ni puntuación. Las notas marginales de modificación de la BCN, encabezados, pies de página, nota editorial de la página 56, promulgación y certificado del Tribunal Constitucional se documentan como contexto y quedan fuera de las unidades de la ley. Cada archivo de unidad señala la página del PDF y su contexto normativo.

**Estado actual:** inventario íntegro localizado; fragmentación en curso. La condición «completo» se asignará a cada artículo sólo tras reconstruir y contrastar sus unidades con el original. No se han extraído Exigencias ni realizado auditoría independiente.
'''
(DEST/'FUENTE.md').write_text(meta,encoding='utf-8')
print('written',len(arts),'articles',sum(len(a['blocks']) for a in arts),'units')

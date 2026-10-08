import json,re
from pathlib import Path
B=json.load(open('tmp/pdfs/ley-21719/blocks.json',encoding='utf-8'))
root=Path('Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01')
top={0:('Artículo primero permanente','articulo-primero'),617:('Artículo segundo permanente','articulo-segundo'),618:('Artículo tercero permanente','articulo-tercero'),620:('Artículo primero transitorio','articulo-transitorio-primero'),621:('Artículo segundo transitorio','articulo-transitorio-segundo'),622:('Artículo tercero transitorio','articulo-transitorio-tercero'),623:('Artículo cuarto transitorio','articulo-transitorio-cuarto'),628:('Artículo quinto transitorio','articulo-transitorio-quinto'),629:('Artículo sexto transitorio','articulo-transitorio-sexto'),630:('Artículo séptimo transitorio','articulo-transitorio-septimo'),631:('Artículo octavo transitorio','articulo-transitorio-octavo')}
numeral_starts={int(re.match(r'^(\d+)\)',b['text']).group(1)):b['i'] for b in B[1:617] if re.match(r'^(\d+)\)',b['text'])}
assert set(numeral_starts)==set(range(1,17)),numeral_starts
numeral_by_i={v:k for k,v in numeral_starts.items()}
article_re=re.compile(r'^"?Artículo\s+(\d+)(?:[°º])?(?:\s+(bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?\.-',re.I)
letter_re=re.compile(r'^"?([a-zñ])\)')
roman_re=re.compile(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x)\.')
sub_re=re.compile(r'^(uno|dos|tres|cuatro|cinco)\)')
heading_re=re.compile(r'^"?(Título\s+[IVX]+|Párrafo\s+\w+)$',re.I)
node=[]; current_top=None; current_num=None; current_sub=None; current_emb=None; current_letter=None;para_count={};letter_count={}
for b in B:
 i=b['i'];t=b['text'];pages=b['pages'];kind='';label='';level=0;path=None;parent=None
 if i in top:
  current_top=top[i];current_num=None;current_sub=None;current_emb=None;current_letter=None
  kind='top';label=current_top[0];level=0
 elif i==619:
  kind='trans-heading';label='Disposiciones transitorias (encabezado)';level=0
 elif i in numeral_by_i:
  current_num=numeral_by_i[i];current_sub=None;current_emb=None;current_letter=None
  kind='numeral';label=f'Numeral {current_num}: '+t[3:];level=1
 elif current_top and current_top[1]=='articulo-primero':
  sub=sub_re.match(t) if current_num==5 else None
  em=article_re.match(t)
  let=letter_re.match(t)
  rom=roman_re.match(t)
  ordn=re.match(r'^(\d+)\.',t)
  head=heading_re.match(t)
  if sub:
   current_sub=sub.group(1);current_emb=None;current_letter=None
   kind='subnumeral';label=f'Subnumeral {current_sub}: '+t[len(current_sub)+2:];level=2
  elif em:
   n,suf=em.groups();current_emb=n+(('-'+suf.lower()) if suf else '')
   current_letter=None
   kind='embedded-article';label=f'Artículo {n}'+(f' {suf}' if suf else '')+' reproducido';level=2
   para_count.setdefault((current_num,current_emb),0)
  elif head:
   current_emb=None;current_letter=None
   kind='heading';label=t.strip('"');level=2
  elif let:
   current_letter=let.group(1)
   kind='letter';label=f'Letra {current_letter}: '+t[let.end():].strip()[:115]
   level=3 if current_emb or current_sub else 2
  elif rom:
   kind='roman';label=f'Numeral romano {rom.group(1)}: '+t[rom.end():].strip()[:115]
   level=4 if current_emb else 3
  elif ordn and current_emb:
   kind='ordinal';label=f'Ordinal {ordn.group(1)}: '+t[ordn.end():].strip()[:115];level=3
  elif i in (219,220) and current_emb=='16':
   kind='letter-continuation';label=('Letra b, párrafo segundo: efecto del cumplimiento de condiciones' if i==219 else 'Letra b, párrafo tercero: salida de integrante');level=4
  elif current_emb:
   k=(current_num,current_emb);para_count[k]+=1
   kind='paragraph';label=f'Párrafo {para_count[k]+1}: '+t[:115];level=3
   current_letter=None
  elif current_sub:
   kind='sub-content';label='Párrafo complementario: '+t[:115];level=3
  else:
   kind='rubro';label='Rúbrica: '+t[:115];level=2
 elif current_top:
  kind='trans-paragraph';label='Párrafo complementario: '+t[:115];level=1
 else:
  raise ValueError((i,t[:50]))
 if i==0:path='articulo-primero/instruccion-general.md'
 elif i in top: path=f'{top[i][1]}/articulo.md'
 elif i==0:path='articulo-primero/instruccion-general.md'
 elif i in numeral_by_i:path=f'articulo-primero/numeral-{current_num:02}/instruccion.md'
 elif i in (3,4,5,6):path=f'articulo-primero/numeral-02/articulo-reproducido-01/inciso-{i-2:02}.md'
 node.append({**b,'kind':kind,'label':label,'level':level,'path':path,'top':current_top[1] if current_top else None,'numeral':current_num,'subnumeral':current_sub,'embedded':current_emb})
 if i in (219,220):node[-1]['parent_index']=213;node[-1]['continuation_ordinal']=2 if i==219 else 3
# Continuaciones comprobadas por lectura de la secuencia y disposición visual del PDF.
for idx,parent,kind,label in [
 (19,18,'letter-continuation','Letra f, párrafo segundo: criterio de identificabilidad'),
 (37,36,'letter-continuation','Letra u, párrafo segundo: transmisión directa de datos'),
 (47,46,'letter-continuation','Letra a, párrafo segundo: acreditación de licitud'),
 (49,48,'letter-continuation','Letra b, párrafo segundo: cambio de finalidad'),
 (51,50,'letter-continuation','Letra c, párrafo segundo: plazo de conservación'),
 (56,55,'letter-continuation','Letra g, párrafo segundo: facilitar información'),
 (260,259,'roman-inserted-text','Romano i, texto de epígrafe insertado'),
 (263,262,'letter-inserted-text','Letra c, texto del inciso octavo incorporado'),
]:
 node[idx]['kind']=kind;node[idx]['label']=label;node[idx]['level']=node[parent]['level']+1;node[idx]['parent_index']=parent
Path('tmp/pdfs/ley-21719/structure.json').write_text(json.dumps(node,ensure_ascii=False,indent=2),encoding='utf-8')
pathfile=Path('tmp/pdfs/ley-21719/paths.json')
if pathfile.exists():
 allpaths=json.loads(pathfile.read_text(encoding='utf-8'))
 for z in node:
  if str(z['i']) in allpaths:z['path']=allpaths[str(z['i'])]
lines=['# Árbol de la Ley N° 21.719 — versión con vigencia diferida desde 01-DIC-2026','','Inventario íntegro de los artículos propios y del texto modificatorio reproducido, en el orden del PDF. `Artículo ... reproducido` designa un artículo de la Ley N° 19.628 dentro del numeral modificatorio, no un artículo propio de la Ley N° 21.719. Los títulos y párrafos rubricados son contexto estructural, no Disposiciones. Estados de fragmentación: `[pendiente]`, `[parcial]`, `[completo]`. Páginas son ordinales del PDF de 56 páginas.','','```text','Ley 21.719 (PDF BCN generado 22-SEP-2026) [completo]']
for n in node:
 if n['i']==619:status='completo'
 else:status='completo' if n['path'] and (root/n['path']).exists() else 'pendiente'
 page='p. '+(', '.join(map(str,n['pages'])))
 label=n['label'].replace('`','’')
 if len(label)>135:label=label[:132]+'...'
 link=f' -> {n["path"]}' if n['path'] and (root/n['path']).exists() else ''
 if n['kind']=='embedded-article':
  em=n['embedded'].replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','ny'); em=re.sub(r'^\d+',lambda m:m.group(0).zfill(2),em)
  card=f'articulo-primero/numeral-{n["numeral"]:02}/articulo-reproducido-{em}/articulo.md'
  link=f' -> {card}' if (root/card).exists() else ''
 if n['i']==0:
  link=' -> articulo-primero/articulo.md'
 if n['i']==623:
  link=' -> articulo-transitorio-cuarto/articulo.md'
 lines.append('|   '*n['level']+'|-- '+label+f' [{status}; {page}]'+link)
 if n['i']==0:
  lines.append('|   |-- Instrucción general modificatoria [completo; p. 1] -> articulo-primero/instruccion-general.md')
 if n['i']==623:
  lines.append('|   |-- Inciso primero: '+n['text'][:100]+f' [{status}; {page}] -> articulo-transitorio-cuarto/inciso-01.md')
 if n['kind']=='embedded-article':
  firstpath=n['path'] or f'articulo-primero/numeral-{n["numeral"]:02}/articulo-reproducido-{n["embedded"]}/inciso-01.md'
  lines.append('|   '*(n['level']+1)+'|-- Inciso primero: '+n['text'][:100]+f' [{status}; {page}]'+(f' -> {firstpath}' if (root/firstpath).exists() else ''))
lines.append('```')
(root/'ARBOL.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('nodes',len(node),'tree lines',len(lines),'top articles',len(top),'numerals',len(numeral_starts))

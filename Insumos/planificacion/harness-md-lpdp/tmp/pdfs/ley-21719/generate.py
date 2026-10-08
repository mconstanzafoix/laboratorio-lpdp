import json,re,os,collections
from overrides import ARTICLE,PASSAGE
from pathlib import Path
N=json.load(open('tmp/pdfs/ley-21719/structure.json',encoding='utf-8'))
root=Path('Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01')
orig='Fuentes-primarias/Ley-21719-2024/Ley-21719_13-DIC-2024.pdf'
version='Ley N° 21.719, versión con vigencia diferida desde 01-DIC-2026; última modificación impresa: Ley N° 21.806, 05-FEB-2026'
article_re=re.compile(r'^"?Artículo\s+(\d+)(?:[°º])?(?:\s+(bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?\.-',re.I)
letter_re=re.compile(r'^"?([a-zñ])\)')
roman_re=re.compile(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x)\.')
sub_re=re.compile(r'^(uno|dos|tres|cuatro|cinco)\)')
rem_re=re.compile(r'\b(?:artículos?\s+[0-9]+(?:[°º])?(?:\s+(?:bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?(?:\s*,\s*[0-9]+(?:[°º])?)?|ley\s+N[°º]\s*[0-9.]+|decreto\s+N[°º]\s*[0-9.]+|Constitución Política de la República)\b',re.I)
cond_re=re.compile(r'\b(cuando|siempre que|si\s+|en caso|salvo|excepto|sin perjuicio|sólo|únicamente|a menos que|no procederá|no se aplicará|con independencia)\b',re.I)
verb_order=[('modificación legislativa',r'\b(sustitúyese|reemplázase|incorpórase|agrégase|intercálase|derógase|elimínase|suprímese|introdúcense|sustitúyense|reemplázanse|incorpóranse|agréganse|elimínanse|intercálanse)\b'),('catálogo de infracciones',r'\binfracciones (leves|graves|gravísimas)\b'),('sanción',r'\b(sanci[oó]n|multa|amonestaci[oó]n|suspensi[oó]n|revoca[cr])\b'),('definición',r'\b(se entiende|se entenderá|son datos|es un registro|tendr[áa]n esta condici[oó]n|consiste en|significa|se consideran)\b'),('prohibición o límite',r'\b(no podr[áa]n?|se proh[ií]be|no proceder[áa]|no se aplicará|no tendr[áa])\b'),('deber',r'\b(deber[áa]n?|est[áa] obligado|estar[áa] obligado|obligaci[oó]n|deber de)\b'),('derecho del titular',r'\b(tiene derecho|tendr[áa] derecho|podr[áa] solicitar|derecho a)\b'),('facultad o permiso condicionado',r'\b(podr[áa]n?|pueden|se podr[áa]|est[áa]n facultados)\b'),('regla de licitud o aplicación',r'\b(es l[ií]cito|se aplicar[áa]|se sujetar[áa]|quedar[áa] sujeto)\b'),('regla de organización o competencia',r'\b(cr[eé]ase|estar[áa] formado|tendr[áa] las siguientes funciones|ser[áa] nombrad|corresponder[áa])\b')]
num_instr={n['numeral']:n['text'] for n in N if n['kind']=='numeral'}
embedded_heads={}
for n in N:
 if n['kind']=='embedded-article':embedded_heads[(n['numeral'],n['embedded'])]=n['text']

def excerpt(t, limit=180):
 return t if len(t)<=limit else t[:limit].rsplit(' ',1)[0]+'…'

def first_sentence(t):
 s=re.sub(r'^"?(?:Artículo\s+[^.]*?\.-\s*|[a-zñ]\)\s*|(?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\.\s*|\d+[.)]\s*|(?:uno|dos|tres|cuatro|cinco)\)\s*)','',t,flags=re.I)
 matches=list(re.finditer(r'(?<=[.;])\s',s))
 if matches:
  end=matches[0].start()+1
  if end<90 and len(matches)>1:end=matches[1].start()+1
  elif end<90:end=len(s)
  core=s[:end]
 else:core=s
 return core[:240]+('…' if len(core)>240 else '')

def type_and_reason(n):
 t=n['text'];kind=n['kind']
 if n['i'] in PASSAGE:return PASSAGE[n['i']]
 if kind=='embedded-article' and n['embedded'] in ARTICLE:return ARTICLE[n['embedded']]
 if kind=='ordinal':
  return ('circunstancia atenuante','El ordinal identifica una atenuante específica para graduar responsabilidad.') if n['embedded']=='36' else ('criterio de determinación de multa','El ordinal fija un factor específico que la Agencia debe ponderar al fijar la multa.')
 if kind in ('heading','rubro','trans-heading') or (kind=='content' and re.match(r'^(De|Del|Autoridad|Protecci[oó]n)',t)):
  return 'contexto estructural','Es una rúbrica que organiza el texto reproducido; su ubicación da contexto, sin crear una Disposición normativa independiente.'
 if kind in ('numeral','subnumeral'):
  v=re.search(r'\b(Sustitúyese|Reemplázase|Incorpórase|Agrégase|Intercálase|Derógase|Elimínase|Suprímese|Introdúcense|Sustitúyense|Reemplázanse|Incorpóranse|Agréganse|Elimínanse|Intercálanse)\b',t,re.I)
  action=v.group(1) if v else 'la operación expresada'
  return 'modificación legislativa',f'El verbo «{action}» dirige una operación sobre el texto legal identificado; la regla modificatoria conserva entidad propia frente al texto insertado o sustituido.'
 if kind=='letter' and n['numeral']==5 and not n['embedded']:
  return 'definición legal','El literal fija el contenido de un concepto del artículo 2° modificado; su alcance se completa con la instrucción del subnumeral que lo introduce.'
 if kind=='letter' and n['embedded']:
  letter_functions={
   '1-bis':('supuesto de aplicación territorial','Precisa una circunstancia que activa la aplicación territorial de la ley.'),
   '3':('principio de tratamiento','Formula uno de los principios que rigen el tratamiento de datos personales.'),
   '5':('contenido del derecho de acceso','Identifica información que el responsable debe entregar al ejercer el titular su derecho de acceso.'),
   '7':('supuesto de supresión','Describe un caso que permite al titular pedir la eliminación de sus datos.'),
   '8':('supuesto de oposición','Describe un caso en que el titular puede oponerse al tratamiento.'),
   '8-bis':('excepción a la regla sobre decisiones automatizadas','Delimita un caso en que no se aplica la prohibición o derecho de oposición del inciso anterior, sujeto a sus salvaguardas.'),
   '9':('requisito de portabilidad','Fija una condición de ejercicio del derecho de portabilidad junto con las demás letras del artículo.'),
   '11':('contenido de la solicitud','Precisa los antecedentes que debe aportar el titular en su solicitud al responsable.'),
   '13':('base de licitud','Enuncia una circunstancia que habilita el tratamiento sin recurrir al consentimiento como fundamento.'),
   '14':('obligación del responsable','Es una conducta que el artículo 14 impone al responsable de datos.'),
   '14-ter':('contenido del deber de información','Precisa información que el responsable debe facilitar o mantener disponible para el titular.'),
   '14-quinquies':('medida de seguridad','Concreta una capacidad o medida técnica u organizativa dentro del deber de seguridad.'),
   '15-ter':('supuesto de evaluación de impacto','Identifica una operación que exige considerar la evaluación de impacto según el encabezado del artículo.'),
   '16':('excepción para datos sensibles','Precisa un fundamento que permite tratar datos sensibles sin el consentimiento ordinario, con sus condiciones expresas.'),
   '16-bis':('excepción para datos de salud','Precisa un supuesto de tratamiento de datos de salud o del perfil biológico bajo el régimen especial del artículo.'),
   '16-ter':('información sobre biometría','Es información específica que debe comunicarse al titular antes o durante el tratamiento biométrico.'),
   '23':('límite al ejercicio de derechos','Describe una causal específica de limitación de los derechos del titular frente a órganos públicos.'),
   '24':('régimen especial','Identifica un tratamiento sometido al régimen particular descrito en el artículo.'),
   '25':('regla por clase de infracción','Distingue el tratamiento o publicidad de datos según la clase de infracción indicada.'),
   '27':('condición de transferencia internacional','Identifica una vía o supuesto de transferencia internacional bajo las condiciones del artículo.'),
   '28':('criterio de adecuación','Aporta un factor para determinar la suficiencia de protección del país u organización de destino.'),
   '30-bis':('atribución de la Agencia','Asigna una función específica a la Agencia dentro de su catálogo legal.'),
   '30-ter':('atribución del Consejo Directivo','Asigna al Consejo Directivo una función de dirección de la Agencia.'),
   '30-quinquies':('inhabilidad o incompatibilidad','Señala una circunstancia que impide o limita ejercer el cargo de consejero.'),
   '30-sexies':('causal de cesación','Identifica una causa de término del cargo de consejero.'),
   '30-nonies':('atribución de la presidencia','Asigna una función al presidente del Consejo Directivo.'),
   '32-bis':('componente patrimonial','Identifica una fuente de recursos o bienes del patrimonio de la Agencia.'),
   '34-bis':('infracción leve','Tipifica una conducta dentro del catálogo de infracciones leves.'),
   '34-ter':('infracción grave','Tipifica una conducta dentro del catálogo de infracciones graves.'),
   '34-quáter':('infracción gravísima','Tipifica una conducta dentro del catálogo de infracciones gravísimas.'),
   '35':('consecuencia sancionatoria','Asocia una categoría infraccional con su escala de sanción.'),
   '36':('circunstancia modificativa de responsabilidad','Identifica una atenuante o agravante para valorar la responsabilidad, según el encabezado de la enumeración.'),
   '41':('regla del procedimiento de tutela','Precisa un paso, plazo, requisito o efecto del procedimiento administrativo de tutela.'),
   '42':('regla del procedimiento sancionatorio','Precisa un paso, plazo, requisito o efecto del procedimiento administrativo por infracción.'),
   '43':('regla del reclamo judicial','Precisa un paso, plazo, requisito o efecto del procedimiento de reclamación judicial.'),
   '49':('elemento del modelo preventivo','Identifica un componente que debe contemplar el modelo de prevención de infracciones.'),
   '50':('atribución del delegado','Asigna una función al delegado de protección de datos.'),
   '52':('causal de término de certificado','Identifica una causal de cese de vigencia del certificado.'),
  }
  if n['embedded'] in letter_functions:return letter_functions[n['embedded']]
 if kind=='roman' and n['numeral'] in (9,11) and not n['embedded']:
  return 'modificación legislativa','Este subnumeral precisa la operación textual que ordena la letra modificatoria superior.'
 if n['top'] in ('articulo-segundo','articulo-tercero'):
  return 'modificación legislativa','Suprime exactamente la unidad identificada de otra ley; el objeto de la supresión es parte de la regla.'
 if n['top'] and n['top'].startswith('articulo-transitorio'):
  if 'entrarán en vigencia' in t:return 'regla de vigencia','Fija la entrada en vigencia de las modificaciones permanentes enumeradas, con referencia temporal a la publicación de esta ley.'
  if 'deberán' in t or 'deberá' in t:return 'deber transitorio','Establece una actuación exigida durante la implementación y fija su sujeto o plazo en el propio texto.'
  if 'podrá' in t:return 'facultad transitoria condicionada','Autoriza una actuación temporal bajo las condiciones de plazo y destinatario expresas.'
  return 'regla transitoria','Ordena la transición o su financiamiento conforme a los hitos y sujetos descritos.'
 for name,pat in verb_order:
  m=re.search(pat,t,re.I)
  if m:
   phrase=m.group(0)
   reason={
    'modificación legislativa':'Opera directamente sobre una frase, inciso o artículo de la ley indicada.',
    'catálogo de infracciones':'Identifica una conducta o supuesto dentro de la categoría infraccional encabezada por el artículo reproducido.',
    'sanción':'Determina una consecuencia sancionatoria o una condición para imponerla.',
    'definición':'Fija el significado o los elementos de una categoría jurídica mediante la expresión citada.',
    'prohibición o límite':'Restringe el tratamiento, una facultad o el ejercicio de una regla general.',
    'deber':'Impone al sujeto indicado la conducta o medida descrita.',
    'derecho del titular':'Atribuye al titular una facultad exigible en el contexto del artículo reproducido.',
    'facultad o permiso condicionado':'Habilita la actuación señalada; sus condiciones deben leerse en esta unidad y en el inciso introductorio cuando exista.',
    'regla de licitud o aplicación':'Delimita cuándo se aplica o es lícito el tratamiento previsto.',
    'regla de organización o competencia':'Define la creación, integración o competencia institucional expresada.'
   }[name]
   return name,f'La expresión «{phrase}» {reason[0].lower()+reason[1:]}'
 if kind in ('letter','roman'):
  return 'elemento enumerado de una regla','Concreta uno de los supuestos, requisitos, contenidos o efectos de la enumeración que introduce el bloque precedente.'
 return 'regla normativa o contexto de aplicación','El pasaje completa el alcance, efecto o excepción del artículo reproducido; su lectura requiere el encabezado y los incisos vecinos.'

def limiters(t):
 clauses=[]
 for s in re.split(r'(?<=[.;])\s+',t):
  if cond_re.search(s):clauses.append(s[:300]+('…' if len(s)>300 else ''))
 if len(clauses)>3:clauses=clauses[:3]+[f'Hay {len(clauses)-3} cláusulas adicionales en el literal completo.']
 return ' | '.join(clauses) if clauses else 'No se separó una excepción autónoma adicional; las condiciones visibles permanecen en el literal y, para listas, en la introducción enlazada.'

def remissions(t):
 found=[]
 for m in rem_re.finditer(t):
  q=m.group(0)
  if q not in found:found.append(q)
 generic=[
  (r'\bcuando la ley (?:así )?(?:lo permita|lo señale|lo disponga|autorice|establezca)', 'Habilitación legal genérica; el literal no identifica la ley'),
  (r'\bsalvo que la ley (?:expresamente )?(?:autorice|permita|disponga)', 'Excepción remitida a autorización legal expresa'),
  (r'\b(?:inciso anterior|inciso siguiente|artículo siguiente|presente artículo)\b', 'Remisión interna al artículo o inciso indicado'),
  (r'\b(?:derecho internacional|legislación nacional)\b', 'Remisión al ordenamiento indicado sin norma concreta'),
  (r'\b(?:el reglamento|un reglamento|al reglamento)\b', 'Remisión reglamentaria sin número de decreto en este literal'),
 ]
 for pat,desc in generic:
  if re.search(pat,t,re.I) and desc not in found:found.append(desc)
 return '; '.join(found[:10])+(' (y otras remisiones visibles en el literal)' if len(found)>10 else '') if found else 'No se identificó una remisión a otra unidad normativa en este literal.'

def slug(t):
 s=t.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','ny').replace('°','').replace('º','')
 return re.sub(r'^\d+',lambda m:m.group(0).zfill(2),s)

paths={};names=collections.Counter();current_intro={};last_block={};embedded_count=collections.Counter()
for n in N:
 i=n['i'];kind=n['kind'];num=n['numeral'];top=n['top'];sub=n['subnumeral'];emb=n['embedded'];t=n['text']
 if i==619:continue
 if i in (0,1,2,3,4,5,6):
  paths[i]=n['path'];continue
 if kind=='top':
  if top=='articulo-primero':paths[i]='articulo-primero/instruccion-general.md'
  elif top=='articulo-transitorio-cuarto':paths[i]=f'{top}/inciso-01.md'
  else:paths[i]=f'{top}/articulo.md'
  continue
 if kind=='trans-paragraph':
  base=top;names[(base,'inciso')]+=1;paths[i]=f'{base}/inciso-{names[(base,"inciso")]+1:02}.md';continue
 if kind=='numeral':paths[i]=f'articulo-primero/numeral-{num:02}/instruccion.md';continue
 base=f'articulo-primero/numeral-{num:02}'
 if kind=='subnumeral':paths[i]=f'{base}/subnumeral-{sub}/instruccion.md';continue
 if kind=='embedded-article':
  edir=f'{base}/articulo-reproducido-{slug(emb)}'
  paths[i]=f'{edir}/inciso-01.md';names[(edir,'inciso')]=1;continue
 if emb:base+=f'/articulo-reproducido-{slug(emb)}'
 elif sub:base+=f'/subnumeral-{sub}'
 if kind in ('letter-continuation','roman-inserted-text','letter-inserted-text'):
  parent=N[n['parent_index']]
  mark=(letter_re.match(parent['text']).group(1) if kind!='roman-inserted-text' else roman_re.match(parent['text']).group(1))
  filename=(f'letra-{slug(mark)}-inciso-{n.get("continuation_ordinal",2):02}.md' if kind=='letter-continuation' else f'romano-{mark}-texto-insertado.md' if kind=='roman-inserted-text' else f'letra-{slug(mark)}-texto-insertado.md')
 elif kind=='ordinal':
  mark=re.match(r'^(\d+)\.',t).group(1);filename=f'ordinal-{mark}.md'
 elif kind=='paragraph':
  names[(base,'inciso')]+=1;filename=f'inciso-{names[(base,"inciso")]:02}.md'
 elif kind=='letter':
  mark=letter_re.match(t).group(1);names[(base,'letra',mark)]+=1;k=names[(base,'letra',mark)];filename=f'letra-{slug(mark)}'+(f'-{k:02}' if k>1 else '')+'.md'
 elif kind=='roman':
  mark=roman_re.match(t).group(1);names[(base,'romano',mark)]+=1;k=names[(base,'romano',mark)];filename=f'romano-{mark}'+(f'-{k:02}' if k>1 else '')+'.md'
 elif kind=='heading':filename=f'encabezado-{i:03}.md'
 elif kind=='rubro':filename=f'rubro-{i:03}.md'
 else:filename=f'unidad-{i:03}.md'
 paths[i]=f'{base}/{filename}'

for q,c in collections.Counter(paths.values()).items():
 if c>1:print('DUP',q,[i for i,p in paths.items() if p==q])
assert len(paths)==631 and len(set(paths.values()))==631,(len(paths),len(set(paths.values())))
for n in N:
 i=n['i']
 if i==619:continue
 p=root/paths[i]
 if i in range(0,7):continue
 p.parent.mkdir(parents=True,exist_ok=True)
 t=n['text'];kind=n['kind'];num=n['numeral'];emb=n['embedded'];pages=', '.join(map(str,n['pages']))
 typ,reason=type_and_reason(n)
 if n['top']=='articulo-primero':
  loc='artículo primero permanente'
  if num:loc+=f', numeral {num}'
  if n['subnumeral']:loc+=f', subnumeral {n["subnumeral"]}'
  if emb:loc+=f', artículo {emb.replace("-"," ")} reproducido de la Ley N° 19.628'
  if kind=='letter':loc+=f', letra {letter_re.match(t).group(1)}'
  if kind=='ordinal':loc+=f", ordinal {re.match(r'^(\d+)\.',t).group(1)}"
  if kind=='roman':loc+=f', romano {roman_re.match(t).group(1)}'
  if kind=='paragraph':loc+=f', inciso {int(Path(paths[i]).stem.replace("inciso-",""))}'
  if kind=='letter-continuation':loc+=f', letra {letter_re.match(N[n["parent_index"]]["text"]).group(1)}, párrafo {"segundo" if n.get("continuation_ordinal",2)==2 else "tercero"}'
  if kind=='roman-inserted-text':loc+=f', romano {roman_re.match(N[n["parent_index"]]["text"]).group(1)}, texto de epígrafe insertado'
  if kind=='letter-inserted-text':loc+=f', letra {letter_re.match(N[n["parent_index"]]["text"]).group(1)}, texto del inciso incorporado'
  if kind=='heading':loc+=', encabezado estructural'
  if kind=='rubro':loc+=f', rúbrica estructural secuencia {i}'
 else:
  bits=n['top'].split('-');own='artículo '+(bits[2]+' transitorio' if bits[1]=='transitorio' else bits[1]+' permanente')
  if kind=='trans-paragraph':loc=own+f', inciso {int(Path(paths[i]).stem.replace("inciso-",""))}'
  elif n['top']=='articulo-transitorio-cuarto':loc=own+', inciso 1'
  else:loc=own
 if kind in ('letter-continuation','roman-inserted-text','letter-inserted-text'):
  context=f'Continuación subordinada a «{N[n["parent_index"]]["text"][:190]}…»; se mantiene separada para conservar el párrafo o texto incorporado con localizador propio.'
 elif kind=='embedded-article':
  context='Texto de la Ley N° 19.628 reproducido por la instrucción modificatoria del numeral; no es un artículo autónomo de la Ley N° 21.719.'
 elif emb:
  head=embedded_heads[(num,emb)]
  subject=head.split('.-',1)[1].strip().split('.',1)[0] if '.-' in head else head
  context=f'Artículo {emb.replace("-"," ")} reproducido en el numeral {num}; materia: «{subject}». La instrucción modificatoria y los demás párrafos o listas del artículo dan el alcance completo.'
 elif n['top']=='articulo-primero' and num:
  context=f'Numeral {num} del artículo primero, cuya instrucción dispone «{excerpt(first_sentence(num_instr[num]),160)}». El artículo primero modifica la Ley N° 19.628.'
 else:context='Artículo propio de la Ley N° 21.719; se lee en la secuencia de permanentes o transitorios que indica el árbol.'
 intro_link=''
 if kind in ('letter','roman','ordinal'):
  basekey=str(p.parent)
  intro=current_intro.get(basekey)
  if intro:
   intro_text,intro_index=intro
   context+=' Introducción de la lista: «'+excerpt(intro_text,170)+'»; literal íntegro en la unidad enlazada.'
   intro_path=root/paths[intro_index]
   intro_link=f'; [introducción íntegra de la lista]({os.path.relpath(intro_path,p.parent)})'
 if t.endswith(':'):
  current_intro[str(p.parent)]=(t,i)
 nucleus=first_sentence(t)
 if kind in ('heading','rubro'):
  analysis=reason
 elif kind in ('embedded-article','ordinal'):
  analysis=f'**Función propuesta: {typ}.** {reason}'
 else:
  analysis=f'**Función propuesta: {typ}.** {reason} Núcleo textual: «{nucleus}».'
 if kind in ('heading','rubro','trans-heading'):
  limits='No corresponde: encabezado de contexto.';refs='No corresponde a una Disposición autónoma.'
 else:
  limits=limiters(t);refs=remissions(t[article_re.match(t).end():] if kind=='embedded-article' and article_re.match(t) else t)
 relart=os.path.relpath(root/'articulo-primero/articulo.md',p.parent) if n['top']=='articulo-primero' else os.path.relpath(root/n['top']/'articulo.md',p.parent)
 links=f'[artículo propio de la Ley N° 21.719]({relart})'
 if kind in ('letter-continuation','roman-inserted-text','letter-inserted-text'):
  parentpath=root/paths[n['parent_index']]
  links+=f'; [unidad superior]({os.path.relpath(parentpath,p.parent)})'
 if emb:
  embeddedcard=p.parent/'articulo.md'
  links+=f'; [artículo reproducido]({os.path.relpath(embeddedcard,p.parent)})'
  instr=root/f'articulo-primero/numeral-{num:02}/instruccion.md'
  links+=f'; [instrucción modificatoria]({os.path.relpath(instr,p.parent)})'
 elif num and kind not in ('numeral',):
  instr=root/f'articulo-primero/numeral-{num:02}/instruccion.md'
  links+=f'; [instrucción del numeral]({os.path.relpath(instr,p.parent)})'
 links+=intro_link
 if i==219:
  links+='; condiciones de la letra b: '+', '.join(f'[romano {q}](romano-{q}.md)' for q in ('i','ii','iii','iv','v'))
  context+=' La expresión «estas condiciones» remite conjuntamente a los romanos i a v de la letra b.'
 if i==220:
  links+='; [efecto del cumplimiento de condiciones](letra-b-inciso-02.md)'
  context+=' La anonimización o supresión opera al cesar la pertenencia a la persona jurídica de la letra b.'
 title=n['label'].split(':')[0]
 if kind=='trans-paragraph':title=loc
 p.write_text(f'''# {title}

- **Fuente y versión:** {version}.
- **Localizador:** {loc}.
- **Original y localización:** `{orig}`, página(s) PDF {pages}.
- **Vínculos de contexto:** {links}.
- **Jerarquía:** {context}

## Texto literal

> {t}

Se normalizaron únicamente los espacios y saltos de renglón de la maquetación. Se conservaron palabras, puntuación y comillas visibles.

## Análisis de fragmentación

{analysis}

- **Condiciones y excepciones:** {limits}
- **Remisiones expresas:** {refs}

## Comprobación

La unidad se localizó en la página PDF indicada y se conservó en el orden del artículo completo registrado en `ARBOL.md`. La reconstrucción y el contraste global de cobertura se documentan en `INFORME-FRAGMENTACION.md`.
''',encoding='utf-8')

# Structural cards for embedded articles.
for (num,emb),head in embedded_heads.items():
 edir=root/f'articulo-primero/numeral-{num:02}/articulo-reproducido-{slug(emb)}'
 card=edir/'articulo.md'
 if card.exists() and (num,emb)==(2,'1'):continue
 ids=[x['i'] for x in N if x['numeral']==num and x['embedded']==emb and x['kind'] not in ('heading',)]
 ps=sorted({p for x in N if x['i'] in ids for p in x['pages']})
 links='\n'.join(f'- [{N[i]["label"].split(":")[0]}]({Path(paths[i]).name})' for i in ids if i in paths)
 card.parent.mkdir(parents=True,exist_ok=True)
 card.write_text(f'''# Artículo {emb.replace('-',' ')} de la Ley N° 19.628 reproducido

- **Fuente del literal:** {version}.
- **Original:** `{orig}`, páginas PDF {min(ps)}–{max(ps)}.
- **Jerarquía:** [artículo primero permanente](../../articulo.md) > [numeral {num}](../instruccion.md) > texto de la Ley N° 19.628 reproducido. No es artículo propio de la Ley N° 21.719.
- **Función conjunta:** {first_sentence(head)} Los archivos siguientes conservan los párrafos y enumeraciones en orden; el mandato legislativo de incorporación o sustitución está en el numeral.

## Unidades

{links}
''',encoding='utf-8')

# Summary cards for top-level articles; preserve human written first article.
for n in N:
 if n['kind']!='top':continue
 top=n['top'];card=root/top/'articulo.md'
 if card.exists() and (num,emb)==(2,'1'):continue
 ids=[x['i'] for x in N if x['top']==top and x['i']!=n['i'] and x['kind']!='trans-heading']
 if not ids:continue
 ps=sorted({p for x in N if x['i'] in [n['i']]+ids for p in x['pages']})
 links='\n'.join(f'- [{N[i]["label"].split(":")[0]}]({os.path.relpath(root/paths[i],card.parent)})' for i in ids if i in paths)
 card.parent.mkdir(parents=True,exist_ok=True)
 card.write_text(f'''# {n['label']}

- **Fuente y versión:** {version}.
- **Original:** `{orig}`, páginas PDF {min(ps)}–{max(ps)}.
- **Localizador:** {n['label']}.
- **Función conjunta:** {first_sentence(n['text'])}

## Unidades

{links}
''',encoding='utf-8')
Path('tmp/pdfs/ley-21719/paths.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2),encoding='utf-8')
print('block files',len(paths),'actual markdown',len(list(root.rglob('*.md'))),'embedded cards',len(embedded_heads))

import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DEST=ROOT/'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01'
SOURCE='Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
ART_RE=re.compile(r'^(Artículo\s+[^.]+)\.-')
SENT=re.compile(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])')
COND=re.compile(r'\b(?:cuando|siempre que|salvo|excepto|con excepción de|sin perjuicio de|en caso de|si\s|sólo si)\b[^.;:]*',re.I)
REF=re.compile(r'\b(?:artículos?\s+\d+[°º]?(?:\s+(?:bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?|inciso\s+(?:primero|segundo|tercero|anterior|siguiente)|Título\s+[IVX]+|ley\s+N[°º]\s*\d+[\.\d]*|Código\s+(?:Penal|Civil|de Procedimiento Civil)|reglamento)\b',re.I)
BODY={}
for page in range(1,57):
    BODY[page]=' '.join((HERE/f'body-{page:02}.txt').read_text(encoding='utf-8').split())

def fragment_pages(part,candidates):
    # Locate the complete literal in the joined body columns. A first/last-word
    # probe misses a page when either probe itself straddles a page break.
    pieces=[BODY[p] for p in candidates]
    joined=' '.join(pieces)
    literal=' '.join(re.sub(r'^Artículo\s+[^.]+\.-\s*','',part).split())
    start=joined.find(literal)
    if start<0 or joined.find(literal,start+1)>=0:
        raise ValueError(f'Fragment not uniquely located in parent pages: {part[:80]}')
    hits=[]
    offset=0
    for page,piece in zip(candidates,pieces):
        end=offset+len(piece)
        if start<end and start+len(literal)>offset:
            hits.append(page)
        offset=end+1
    return hits

# These paragraphs contain separable normative effects. The parent file keeps the
# complete source paragraph as a structural carrier; only the child files are
# proposed as the atomic dispositions for the respective paragraph.
DEFS={
 (2,'',11): [
  ([1],'definición','Define las fuentes de acceso público por su consulta lícita abierta a cualquiera.'),
  ([2],'regla de sujeción','Somete a esta ley el tratamiento de datos obtenido de fuentes públicas; la fuente abierta no libera al responsable del régimen.'),
 ],
 (11,'',10): [
  ([1],'derecho de bloqueo','Permite pedir bloqueo mientras se tramitan rectificación, supresión u oposición.'),
  ([2],'requisito y plazo','Exige fundamentar la solicitud de bloqueo y responderla dentro de dos días hábiles.'),
  ([3,4],'efecto provisional','Suspende el tratamiento de datos requeridos mientras se decide bloqueo, preservando su almacenamiento.'),
  ([5],'deber de motivación y comunicación','Si rechaza bloqueo, el responsable debe motivar y comunicar electrónicamente a la Agencia.'),
  ([6],'reclamación','Permite al titular reclamar rechazo de bloqueo ante la Agencia según el artículo 41.'),
 ],
 (13,'',5): [
  ([1],'base de licitud condicionada','Permite interés legítimo como base sin consentimiento solo si no afecta derechos y libertades del titular.'),
  ([2],'derecho de información','Conserva al titular el derecho a saber qué tratamiento lo afecta y qué interés legítimo se invoca.'),
 ],
 (15,'bis',3): [
  ([1],'instrumento del encargo','Somete el tratamiento por encargado a contrato con el responsable.'),
  ([2],'contenido contractual obligatorio','Exige especificar objeto, duración, fines, datos, titulares, derechos y obligaciones de las partes.'),
  ([3],'límite a la delegación','Prohíbe subdelegar sin autorización escrita y específica del responsable.'),
  ([4],'responsabilidad solidaria','Mantiene responsable solidario al encargado que subdelega, sin exoneración por el hecho de delegar.'),
  ([5],'deber de publicación institucional','Obliga a la Agencia a ofrecer modelos tipo de contratos de encargo.'),
 ],
 (15,'bis',4): [
  ([1],'deber del encargado','Extiende confidencialidad y seguridad de los artículos 14 bis y 14 quinquies al encargado.'),
  ([2],'estándar diferenciado','Aplica al encargado la graduación de estándares del artículo 14 septies.'),
  ([3],'reporte de vulneración','Obliga al encargado a reportar al responsable las vulneraciones de seguridad.'),
 ],
 (16,'bis',5): [
  ([1],'excepción para investigación sanitaria','Permite tratar datos de salud sin consentimiento para investigación o desarrollo de interés público o beneficio humano bajo las finalidades indicadas.'),
  ([2,3],'publicación condicionada','Permite publicar resultados científicos, pero exige anonimizar previamente los datos divulgados.'),
 ],
 (16,'quinquies',2): [
  ([1],'deber de calidad y seguridad','Exige adoptar y acreditar medidas que mantengan el uso de datos solo en fines históricos, estadísticos o científicos.'),
  ([2],'protección reforzada de datos sensibles','Exige identificar y reducir riesgos cuando el tratamiento incluye datos sensibles.'),
  ([3],'efecto de cumplimiento','Permite conservar y utilizar datos por tiempo indeterminado solo tras cumplir las condiciones previas.'),
 ],
 (17,'',2): [
  ([1],'habilitación reglamentaria condicionada','Permite comunicar otras obligaciones de dinero designadas por decreto supremo si constan en instrumento válido con consentimiento y vencimiento.'),
  ([2],'exclusiones de comunicación','Prohíbe comunicar las categorías de deudas de servicios, educación, salud y autopistas que enumera el texto.'),
 ],
 (25,'',3): [
  ([1],'prohibición temporal','Impide publicar o comunicar datos de infracciones tras prescripción o cumplimiento de pena o sanción constatados por autoridad.'),
  ([2],'excepción registral','Permite conservar y consultar registros públicos creados por ley durante el plazo y forma que esa ley determine.'),
  ([3],'deber de reserva','Impone secreto a funcionarios y carácter reservado a esta información.'),
 ],
 (28,'',6): [
  ([1],'definición de garantía adecuada','Exige instrumentos que otorguen protección comparable, derechos exigibles y acciones efectivas a titulares.'),
  ([2],'facultad de aprobación','Permite a la Agencia aprobar cláusulas modelo con garantías suficientes y publicarlas.'),
  ([3],'efecto de aprobación','Dispensa garantías y autorizaciones adicionales a instrumentos aprobados por la Agencia.'),
 ],
 (30,'bis',2): [
  ([1],'potestad normativa','Atribuye a la Agencia dictar instrucciones generales obligatorias sobre tratamiento conforme a los principios legales.'),
  ([2],'consulta y límite de competencia','Condiciona las normas generales a consulta pública web y a necesidad para cumplir esta ley.'),
 ],
 (30,'nonies',1): [
  ([1,2],'jefatura y representación','Designa al presidente del Consejo como jefe de servicio y representante judicial y extrajudicial.'),
  ([3],'dirección administrativa','Le asigna organización, administración y control jerárquico del personal.'),
 ],
 (39,'',1): [
  ([1,2],'creación institucional','Crea el Registro Nacional de Sanciones y Cumplimiento y asigna su administración a la Agencia.'),
  ([3,4],'publicidad y soporte','Establece acceso público y gratuito y soporte electrónico del registro.'),
 ],
 (39,'',2): [
  ([1,2,3],'contenido sancionatorio','Exige inscribir sancionados, gravedad, conducta, circunstancias y sanción.'),
  ([4],'contenido de cumplimiento','También inscribe responsables con modelos preventivos certificados vigentes.'),
 ],
 (41,'',9): [
  ([1],'facultad probatoria','Faculta a la Agencia a pedir antecedentes o informes útiles para resolver.'),
  ([2],'facultad conciliatoria','Permite convocar audiencia y promover acuerdo entre partes.'),
  ([3],'continuidad del conocimiento','Impide que opiniones de funcionarios en audiencia los inhabiliten si fracasa el acuerdo.'),
  ([4],'archivo por acuerdo','Ordena archivar los antecedentes cuando las partes logran acuerdo.'),
 ],
 (46,'',1): [
  ([1,2],'secreto y prohibición de desvío','Obliga a funcionarios a guardar secreto y no usar datos fuera de funciones públicas ni en beneficio propio o ajeno.'),
  ([3],'calificación disciplinaria','Califica la infracción de ese deber como vulneración grave de probidad administrativa, sin excluir otras sanciones.'),
 ],
 (50,'',8): [
  ([1],'secreto del delegado','Impone confidencialidad al delegado respecto de datos conocidos por su cargo.'),
  ([2],'consecuencia penal funcionaria','Remite al Código Penal la sanción de funcionarios públicos delegados que violan el secreto.'),
  ([3],'responsabilidad del responsable','Hace responder al responsable por infracciones de secreto del delegado, con eventual acción de repetición.'),
 ],
 (54,'',1): [
  ([1,2],'base de licitud especial','Permite a órganos constitucionales y autónomos enumerados tratar datos para funciones legales bajo sus leyes orgánicas y excepciones expresas.'),
  ([3],'secreto funcionario','Impone secreto a funcionarios de estos organismos sobre los datos tratados.'),
  ([4],'calidad de responsable y consentimiento','Califica a esos órganos como responsables y dispensa consentimiento dentro de las condiciones del mismo inciso.'),
 ],
}

arts=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'))
tree_path=DEST/'ARBOL.md'
tree=tree_path.read_text(encoding='utf-8').splitlines()
extra_count=0
for (num,suf,index),defs in DEFS.items():
    a=next(a for a in arts if a['num']==num and a['suffix']==suf and not a['transitory'])
    block=a['blocks'][index-1]
    original=block['text']
    sentences=SENT.split(original)
    used=[k for group,_,_ in defs for k in group]
    assert used==list(range(1,len(sentences)+1)),(num,suf,index,used,len(sentences))
    assert ' '.join(sentences)==original,(num,suf,index)
    folder=DEST/('articulo-'+f'{num:02}'+(('-'+suf) if suf else ''))
    label=ART_RE.match(a['blocks'][0]['text']).group(1)
    parent=folder/(block['name']+'.md')
    parent_text=parent.read_text(encoding='utf-8')
    anchor='## Análisis normativo\n'
    note='Este archivo conserva el párrafo íntegro como **unidad estructural**. Por reunir efectos normativos distintos, las Disposiciones propuestas son los fragmentos enlazados abajo.\n\n'
    assert anchor in parent_text
    parent_text=parent_text.replace(anchor,note+anchor,1)
    frag_links=[]
    for j,(group,classification,analysis) in enumerate(defs,1):
        part=' '.join(sentences[k-1] for k in group)
        filename=block['name']+f'-fragmento-{j:02}.md'
        actual_pages=fragment_pages(part,block['pages'])
        page=', '.join(str(p) for p in actual_pages)
        conds=list(dict.fromkeys(m.group(0).strip() for m in COND.finditer(part)))
        cond='; '.join('«'+x+'»' for x in conds) if conds else 'No añade condición o excepción expresa diferente de las del párrafo y artículo introductor.'
        refs=list(dict.fromkeys(m.group(0) for m in REF.finditer(re.sub(r'^Artículo\s+[^.]+\.-\s*','',part))))
        rem='; '.join(refs) if refs else 'Sin remisión expresa propia; conserva las remisiones del párrafo y artículo introductores.'
        if (num,suf,index,j)==(50,'',8,2):
            rem='artículos 246 a 247 bis del Código Penal.'
        if (num,suf,index,j)==(50,'',8,3):
            cond='La salvedad preserva las acciones de repetición del responsable contra el encargado o delegado; no exceptúa el deber de secreto ni elimina la responsabilidad inicial del responsable.'
        context=f'Forma parte de [{block["label"]}]({block["name"]}.md); se lee con las condiciones y excepciones de ese párrafo y del artículo, que se conservan íntegros en el archivo estructural.'
        if (num,suf,index,j)==(50,'',8,1):
            context=f'Forma parte de [{block["label"]}]({block["name"]}.md). La acción de repetición prevista en el fragmento 3 no limita este deber de secreto.'
        frag=f'''# {label} — {block['label']}, fragmento {j}

- **Fuente y versión:** Ley 19.628 consolidada BCN, vigencia diferida desde 01-DIC-2026; última modificación indicada: Ley 21.719 de 13-DIC-2024.
- **Localizador:** {label}, {block['label']}, fragmento {j}; [párrafo íntegro]({block['name']}.md) y [artículo](articulo.md).
- **Original:** `{SOURCE}`, página{'s' if len(actual_pages)>1 else ''} {page} del PDF.

## Texto literal

> {part}

Se normalizaron únicamente espacios y saltos de maquetación. El fragmento es una secuencia continua del párrafo original y conserva su puntuación.

## Análisis normativo

**Función propuesta:** {classification}. {analysis}

**Contexto y alcance:** {context}

**Condiciones o excepciones:** {cond}

**Remisiones expresas:** {rem}

## Comprobación de fragmentación

Se comparó este fragmento con las otras partes del mismo párrafo. La concatenación de los fragmentos en orden reproduce exactamente el texto normalizado de la unidad estructural. No se extrae una Exigencia ni se afirma auditoría independiente.
'''
        (folder/filename).write_text(frag,encoding='utf-8')
        frag_links.append(f'[{classification}]({filename})')
        extra_count+=1
    parent_text += '\n## Fragmentos con sentido normativo propio\n\n'+ '\n'.join(f'{j}. {link}' for j,link in enumerate(frag_links,1))+'\n'
    parent.write_text(parent_text,encoding='utf-8')
    article_file=folder/'articulo.md'
    art_text=article_file.read_text(encoding='utf-8')
    art_text += '\n**Fragmentación interna de '+block['label']+':** '+', '.join(frag_links)+'. El archivo del párrafo íntegro es contexto estructural para estos fragmentos.\n'
    article_file.write_text(art_text,encoding='utf-8')
    needle='-> '+block['path']+' '
    pos=next(i for i,line in enumerate(tree) if needle in line)
    parentline=tree[pos]
    indent=parentline.split('|--',1)[0]
    children=[]
    for j,(_,classification,_) in enumerate(defs,1):
        path=block['path'][:-3]+f'-fragmento-{j:02}.md'
        children.append(f'{indent}|   |-- fragmento {j}: {classification} [pendiente] -> {path}')
    tree[pos+1:pos+1]=children

tree_path.write_text('\n'.join(tree)+'\n',encoding='utf-8')
print('fragmented',len(DEFS),'structural blocks into',extra_count,'atomic files')

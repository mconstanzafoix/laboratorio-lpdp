from pathlib import Path
import json,re,hashlib
blocks=json.loads(Path('tmp/pdfs/decreto-662/blocks.json').read_text())
root=Path('Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09')
root.mkdir(parents=True,exist_ok=True)
source='Fuentes-primarias/Decreto-662-2026/Decreto-662_09-SEP-2026.pdf'
raw=Path(source).read_bytes(); sha=hashlib.sha256(raw).hexdigest()
# Se identifica cada bloque impreso, antes de cualquier corte por oración.
arts={}
current=None
for i,b in enumerate(blocks):
 m=re.match(r'Artículo (\d+)\.- (.+)',b['text'])
 if m:
  current=int(m.group(1));arts[current]=[]
 if current and i<=100 and not b['text'].startswith(('Título II','De los programas de cumplimiento','Párrafo 1','Elementos y publicidad','Párrafo II','Párrafo III','El Delegado de Protección','De la aprobación')):
  arts[current].append(i)
assert sorted(arts)==list(range(1,21))
assert [len(arts[n]) for n in arts]==[3,1,26,1,2,1,2,4,3,3,3,1,14,2,4,8,3,1,3,4]
# Se separan oraciones cuando cambian el efecto, destinatario o modalidad de la regla.
split={7,12,16,27,29,32,33,36,38,39,43,44,46,47,52,56,61,62,66,69,71,72,73,79,87,88,90,95,97,99}
# Nota operativa: los marcadores romanos con punto nunca se tratan como oración.
def split_sentences(text):
 m=re.match(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi)\. ',text)
 pre=''
 if m: pre=m.group(0);text=text[len(pre):]
 pieces=re.split(r'(?<=\.)\s+(?=[A-ZÁÉÍÓÚÑ])',text)
 if pre: pieces[0]=pre+pieces[0]
 return pieces
article_titles={}
for n,ids in arts.items():
 m=re.match(r'Artículo \d+\.- ([^.]+)\. (.*)',blocks[ids[0]]['text'])
 assert m,(n,blocks[ids[0]]['text'][:100])
 article_titles[n]=m.group(1)
 blocks[ids[0]]['body']=m.group(2)
for i,b in enumerate(blocks): b.setdefault('body',b['text'])
# Etiquetas y jerarquía según la impresión, sin convertir títulos ni rúbricas en disposiciones.
roman={17:'i',18:'ii',19:'iii',20:'iv',21:'v',22:'vi',23:'vii',24:'viii',25:'ix',26:'x',27:'xi'}
letter3={13:'a',14:'b',15:'c',16:'d',29:'e',30:'f',32:'g',34:'h',36:'i',37:'j'}
letter13={61:'a',62:'b',63:'c',64:'d',65:'e',66:'f',67:'g',68:'h',69:'i',70:'j',72:'k'}
letter16={83:'a',84:'b',85:'c',86:'d',87:'e'}
extra3={28:'letra-d-parrafo-final',31:'letra-f-parrafo-2',33:'letra-g-parrafo-2',35:'letra-h-parrafo-2'}
def label(n,i,k):
 if n==3:
  if i==12:return 'enunciado'
  if i in letter3:return 'letra-'+letter3[i]
  if i in roman:return 'letra-d-numeral-'+roman[i]
  return extra3[i]
 if n==13:
  if i==60:return 'enunciado'
  if i in letter13:return 'letra-'+letter13[i]
  if i==71:return 'letra-j-parrafo-2'
  return 'inciso-final'
 if n==16:
  if i==82:return 'enunciado'
  if i in letter16:return 'letra-'+letter16[i]
  return {88:'inciso-2',89:'inciso-3'}[i]
 return 'inciso-'+str(k)
# Análisis propio por bloque, tras leer el artículo íntegro. Los textos de una letra conservan el encabezado común.
notes={
1:'Acto aprobatorio: confiere aprobación al reglamento que sigue y delimita su materia por remisión al artículo 49 incorporado por la Ley 21.719. No se numera como artículo reglamentario.',
4:'Fija el objeto del reglamento: requisitos, modalidades y procedimientos de implementación, certificación, registro y supervisión del modelo.',
5:'Habilita la adopción voluntaria del modelo por responsables naturales o jurídicos, públicos o privados; el programa debe ajustarse a la Ley 19.628 y al reglamento.',
6:'Aclara que la adopción del programa no desplaza el deber general de prevenir infracciones y cumplir la Ley 19.628.',
7:'Incorpora las definiciones del artículo 2° de la Ley 19.628 y aplica supletoriamente la Ley 19.880 a actos y procedimientos de la Agencia, salvo disposición legal contraria.',
12:'Define el programa como modelo instrumental de prevención y establece el contenido mínimo de la enumeración a) a j); el carácter mínimo permite componentes adicionales.',
13:'Exige identificar al responsable y, si existe, a su representante legal.',
14:'Exige designar delegado de protección de datos conforme al artículo 8 reglamentario.',
15:'Exige definir medios y facultades del delegado conforme al Párrafo II del Título II.',
16:'Exige caracterizar datos, categorías, bases y operaciones de tratamiento; introduce la información mínima detallada en los numerales i a xi.',
17:'La caracterización debe precisar tipos de datos e identificar los sensibles o de categorías especiales cuando existan.',
18:'La caracterización debe indicar el ámbito territorial del tratamiento conforme al artículo 1° bis de la Ley 19.628.',
19:'La caracterización debe identificar las clases o tipos de bases de datos administradas.',
20:'La caracterización debe describir las categorías de titulares cuyos datos se tratan.',
21:'La caracterización debe consignar los fines de las operaciones de tratamiento.',
22:'La caracterización debe consignar el origen de los datos y, cuando proceda, su carácter de fuente de acceso público.',
23:'La caracterización debe consignar base de licitud e interés legítimo si invoca el literal d) del artículo 13 de la Ley 19.628.',
24:'La caracterización debe identificar categorías de destinatarios previstos, incluidos destinatarios extranjeros u organizaciones internacionales.',
25:'La caracterización debe identificar transferencias internacionales, destino y medios de cumplimiento del artículo 27 de la Ley 19.628.',
26:'La caracterización debe consignar plazos o condiciones de supresión por categoría de datos.',
27:'La caracterización debe declarar decisiones automatizadas y perfiles; si se realizan, debe informar lógica aplicada y consecuencias previstas para el titular.',
28:'Permite utilizar un registro de actividades de tratamiento como soporte de la caracterización; no releva del contenido mínimo.',
29:'Exige identificar actividades con riesgo de infracción, seleccionar las de mayor riesgo para la matriz y graduar la matriz considerando sanciones legales.',
30:'Exige protocolos, reglas y procedimientos preventivos para quienes intervienen en las operaciones o procesos de la entidad.',
31:'Fija criterios de proporcionalidad para esos instrumentos: operaciones, cantidad y tipo de datos, riesgos, tamaño y capacidad económica.',
32:'Exige mecanismos internos de reporte, acceso expedito y permanente; permite integrarlos en canales existentes si cumplen ley y reglamento.',
33:'Exige mecanismos de reporte a autoridad o titulares, otras comunicaciones y autodenuncia; faculta a la Agencia a fijar el mecanismo por instrucción, con salvedad para órganos públicos.',
34:'Exige incluir sanciones internas y procedimientos por incumplimiento de reglas de datos o del programa.',
35:'Para organismos públicos, exige indicar las sanciones legales aplicables a funcionarios o dependientes.',
36:'Exige canal de denuncia ante delegado, reserva de identidad a solicitud del denunciante y prohibición de represalias por denunciar.',
37:'Cláusula de contenido adicional útil o necesario para cumplir normas de protección, ajustado a las operaciones del responsable.',
38:'Exige incorporar la regulación interna contractual y, cuando corresponda, en reglamento interno laboral; en este último caso se aplican medidas de publicidad del Código del Trabajo.',
39:'Exige difundir el programa a trabajadores, empleados y prestadores y extender esa difusión a sus cambios.',
40:'Limita la publicidad de una certificación a la referencia directa, pura y simple al Registro Nacional de Sanciones y Cumplimiento.',
43:'La designación de delegado es facultativa en general y obligatoria al adoptar y certificar un programa; entonces sus atribuciones cubren todas las operaciones del responsable.',
44:'Permite delegado dependiente o contratado; si el proveedor es persona jurídica debe identificar persona natural; admite un delegado para varios responsables si cumple requisitos.',
45:'Para órganos públicos que creen esta función, exige designar funcionario de la dotación vigente.',
46:'Exige designación por la máxima autoridad y define a quién se considera tal según la entidad.',
47:'Exige autonomía del delegado en materias de la ley y rendición de cuenta directa ante quien lo designó.',
48:'Permite al dueño o máxima autoridad de micro, pequeña o mediana empresa asumir personalmente la función.',
49:'Permite delegado único en grupo empresarial, empresas relacionadas o bajo controlador común solo con estándares comunes y accesibilidad equivalente.',
50:'Exige al responsable recursos y facultades suficientes para el delegado, ponderados según tamaño, capacidad, operaciones, datos, riesgos y funciones.',
51:'Permite otras funciones al delegado con resguardo de independencia frente a supervisión y tiempo disponible.',
52:'Exige prevenir conflictos de interés; prohíbe al delegado realizar actividades sujetas a su supervisión o asesoría, con salvedad legal para mipymes.',
53:'La designación debe atender a conocimientos especializados, experiencia y habilidades profesionales del delegado.',
54:'Exige actualización permanente en normas, decisiones e instrucciones de la Agencia y jurisprudencia relevante.',
55:'Exige al responsable demostrar idoneidad y requisitos del delegado en certificación del modelo.',
56:'Exige publicar medios de contacto del delegado para titulares; para órganos públicos conserva la regla especial del decreto 181.',
57:'Los medios publicados deben permitir comunicación expedita y directa entre titulares y delegado.',
58:'Exige informar nombre y contacto del delegado a Agencia, dependientes, organización y encargados cuando corresponda.',
59:'Impone secreto, reserva o confidencialidad al delegado sobre datos e información conocidos por o con ocasión de su función.',
60:'Enuncia funciones mínimas del delegado; la lista a) a k) debe leerse como piso de atribuciones.',
61:'Deber de informar y asesorar a responsable, encargados y dependientes sobre normas y decisiones de la Agencia aplicables al tratamiento.',
62:'Asesoría del delegado en programa y correlativo deber del responsable de asegurar participación oportuna y entregar información.',
63:'Delegado promueve difusión y cumplimiento de política y programa, y supervisa disponibilidad permanente para destinatarios pertinentes.',
64:'Delegado supervisa cumplimiento de ley, instrucciones e interpretaciones de autoridades competentes respecto de tratamientos del responsable.',
65:'Delegado comunica infracciones directamente a la autoridad ante la que rinde cuenta para activar medidas preventivas, correctivas o disciplinarias.',
66:'Delegado se ocupa de formación permanente; puede recomendar periodicidad y contenidos concretos.',
67:'Delegado asesora la identificación de riesgos y medidas de resguardo, especialmente respecto de caracterización y matriz del artículo 3.',
68:'Delegado asesora cumplimiento de evaluación de impacto del artículo 15 ter de la Ley 19.628.',
69:'Delegado desarrolla plan anual, rinde resultados al menos cada año ante autoridad designante y difunde ambos internamente.',
70:'Delegado responde directamente consultas y solicitudes de titulares dentro de atribuciones legales.',
71:'Para esa función, delegado mantiene contacto público actualizado y procura respuesta oportuna.',
72:'Delegado coopera y actúa como punto de contacto con la Agencia y entrega información requerida de modo íntegro y oportuno.',
73:'Responsable identifica nombre y contacto directo del delegado ante la Agencia y comunica cambios de designación o contacto.',
76:'Reconoce potestades legales de certificación, registro, supervisión, revocación y sanción de la Agencia.',
77:'La Agencia certifica modelos que cumplan requisitos legales y reglamentarios.',
78:'Define objeto de la certificación: verificar requisitos y elementos del modelo según ley y reglamento.',
79:'Inicio del procedimiento a solicitud de interesado; tramitación bajo Ley 19.880 e instrucciones de Agencia; contratación de terceros para estudiar antecedentes bajo Ley 19.886.',
80:'La Agencia resuelve solicitud y, si concede, ordena incorporación del modelo al registro.',
81:'El certificado dura tres años y admite renovación solicitada por interesado mediante el mismo procedimiento.',
82:'Introduce las causales de pérdida de efecto del certificado enumeradas en letras a) a e).',
83:'La revocación de la Agencia deja sin efecto la certificación.',
84:'El fallecimiento extingue certificación de responsable persona natural.',
85:'La disolución de persona jurídica extingue su certificación.',
86:'Una resolución judicial ejecutoriada constituye causal de término.',
87:'El cese voluntario de la actividad certificada extingue la certificación y debe avisarse en treinta días.',
88:'El término es inoponible a terceros hasta cancelación registral; Agencia ordena eliminación con revocación o dentro de cinco días hábiles de conocer otra causal.',
89:'Responsable revocado que vuelve a pedir certificación debe acreditar subsanación fehaciente.',
90:'Agencia incorpora certificados vigentes con identidad de responsable/representante, regla de jefe de servicio y fechas de incorporación y vencimiento.',
91:'El registro permite acceso público a certificados emitidos.',
92:'A petición del responsable o representante, Agencia expide constancia de certificación y registro con datos del inciso primero.',
93:'Cada responsable implementa su propio modelo; puede iniciar antes de la inscripción, sujeto a ley, reglamento y normas administrativas.',
94:'Faculta a Agencia a supervisar modelos certificados y cumplimiento de reglas legales y reglamentarias aplicables.',
95:'Faculta requerimiento de información; delegado debe entregarla íntegra y oportunamente; excepción del responsable exige secreto o confidencialidad acreditados.',
96:'Remite a sanciones de la Ley 19.628 por no entregar, o entregar información falsa, incompleta o manifiestamente errónea.',
97:'Revocación fundada por incumplimiento de requisitos o por sanción de infracción de artículos 34 bis a quáter con infracción del artículo 48.',
98:'Procedimiento de revocación de oficio o a petición, sujeto a Ley 19.880 e instrucciones de la Agencia.',
99:'Responsable revocado puede solicitar otra certificación al cumplir requisitos, acreditar subsanación y aportar medidas para impedir reiteración.',
100:'En la nueva decisión, Agencia debe pronunciarse especialmente sobre las medidas de prevención aportadas.'}
assert all(i in notes for ids in arts.values() for i in ids)
article_summaries={
1:'Delimita el objeto reglamentario, habilita la adopción voluntaria del programa y conserva el deber general de cumplimiento de todos los responsables.',
2:'Incorpora definiciones de la Ley 19.628 y fija la aplicación supletoria de la Ley 19.880, salvo disposición legal contraria.',
3:'Define el programa, enumera contenido mínimo de identificación, delegado, caracterización, riesgos, protocolos, reportes, sanciones y denuncias, y permite un registro para caracterizar tratamientos.',
4:'Integra la regulación interna del programa en contratos y, cuando corresponde, en reglamento interno sujeto a publicidad laboral.',
5:'Ordena difundir programa y modificaciones; restringe la forma de informar públicamente la certificación.',
6:'Permite designar delegado en general, vuelve obligatoria la designación al adoptar y certificar un programa y extiende sus funciones a todos los tratamientos del responsable.',
7:'Determina posibles vínculos laborales o de servicios del delegado, contratación mediante persona jurídica, pluralidad de responsables y designación de funcionario en órganos públicos.',
8:'Regula autoridad designante, autonomía, rendición de cuentas y supuestos de delegado asumido por dueños de mipymes o compartido en grupos empresariales.',
9:'Exige medios suficientes al delegado y disciplina la compatibilidad de otras funciones con independencia y ausencia de conflictos de interés.',
10:'Fija criterios de idoneidad inicial y actualización del delegado y exige demostrarla al certificar el modelo.',
11:'Regula publicación y comunicación de identidad y contacto del delegado para titulares, Agencia, organización y encargados.',
12:'Impone al delegado secreto, reserva o confidencialidad sobre datos e información conocidos por su función.',
13:'Enumera funciones mínimas del delegado y exige al responsable identificarlo y comunicar cambios ante la Agencia.',
14:'Reconoce potestades de la Agencia y vincula la certificación al cumplimiento de requisitos legales y reglamentarios.',
15:'Regula objeto, inicio, tramitación, decisión, inscripción, vigencia y renovación de la certificación.',
16:'Enumera causas de término, exige aviso de cese, regula oponibilidad y eliminación registral y condiciona nueva solicitud tras revocación.',
17:'Regula incorporación y datos del Registro, publicidad de certificados y constancia a petición.',
18:'Permite implementar el modelo antes de la inscripción, a cargo de cada responsable y con plena sujeción normativa.',
19:'Regula supervisión, solicitud y entrega de información, excepción por secreto acreditado y sanción por incumplimiento informativo.',
20:'Regula causales y procedimiento de revocación, nueva solicitud tras subsanación y examen especial de las medidas correctivas.'}
fragment_notes={
(7,1):'Adopta para el reglamento las definiciones del artículo 2° de la Ley 19.628.',(7,2):'Aplica Ley 19.880 a actos y procedimientos de la Agencia, excepto cuando otra ley disponga lo contrario.',
(12,1):'Define el programa como conjunto instrumental de prevención que puede adoptar un responsable natural o jurídico.',(12,2):'Impone al programa el contenido mínimo detallado en las letras a) a j).',
(16,1):'Exige caracterizar datos, categorías, bases y operaciones de tratamiento.',(16,2):'Introduce la información mínima obligatoria detallada en los numerales i a xi de la letra d).',
(27,1):'Exige consignar si existen decisiones automatizadas, incluida elaboración de perfiles.',(27,2):'Si existen esas operaciones, obliga a informar lógica aplicada y consecuencias previstas para el titular.',
(29,1):'Exige identificar operaciones habituales o esporádicas que generan o incrementan riesgo de infracciones tipificadas.',(29,2):'Exige seleccionar las operaciones de mayor riesgo e incorporarlas a matriz de riesgos.',(29,3):'Exige construir la matriz según graduación de sanciones legales.',
(32,1):'Incluye mecanismos de reporte interno entre los elementos del programa.',(32,2):'Exige vías de reporte expeditas y permanentemente accesibles a miembros de la organización.',(32,3):'Permite aprovechar canales ya existentes si satisfacen ley y reglamento.',
(33,1):'Exige mecanismos de reporte a autoridad o titulares y de autodenuncia según los supuestos legales citados.',(33,2):'Faculta a la Agencia a definir esas comunicaciones por instrucción general y conserva regla especial de órganos públicos.',
(36,1):'Incluye un canal de denuncia interna ante delegado.',(36,2):'Exige que el canal permita solicitar y asegurar reserva de identidad.',(36,3):'Prohíbe represalias desfavorables a causa de la denuncia.',
(38,1):'Exige incorporar la regulación interna del programa como obligación contractual para trabajadores y prestadores, incluso directivos.',(38,2):'Cuando corresponda, exige incorporarla además al reglamento interno laboral.',(38,3):'En ese supuesto exige publicidad del artículo 156 del Código del Trabajo.',
(39,1):'Exige divulgar la existencia del programa a trabajadores, empleados y prestadores.',(39,2):'Extiende la misma divulgación a modificaciones y actualizaciones.',
(43,1):'Permite designación general de delegado, pero la exige al adoptar y certificar programa.',(43,2):'En ese supuesto asigna al delegado atribuciones legales y reglamentarias para todas las operaciones del responsable.',
(44,1):'Permite delegado dependiente o vinculado por contrato de servicios.',(44,2):'Si contrata persona jurídica, el contrato debe identificar a la persona natural delegada.',(44,3):'Permite a una persona natural ser delegada de varios responsables si cumple requisitos.',
(46,1):'Exige que la designación emane de la máxima autoridad directiva o administrativa.',(46,2):'Define cuáles cargos pueden constituir esa autoridad según la entidad.',
(47,1):'Exige autonomía del delegado en materias relacionadas con la ley.',(47,2):'Exige rendición de cuentas directa ante la autoridad designante.',
(52,1):'El responsable debe evitar conflicto de intereses y proteger la independencia del delegado con independencia de su vínculo.',(52,2):'Prohíbe al delegado ejecutar actividades que deberá supervisar o asesorar, con salvedad legal para mipymes.',
(56,1):'Exige al responsable publicar contacto del delegado para ejercicio de derechos y consultas de titulares.',(56,2):'En órganos públicos mantiene aplicable la regla especial del decreto supremo 181.',
(61,1):'Delegado informa y asesora sobre normas de protección de datos a responsable, encargados y dependientes.',(61,2):'Extiende esa asesoría a instrucciones y decisiones de la Agencia y otras normas aplicables.',
(62,1):'Delegado asesora la revisión, modificación y nuevo programa.',(62,2):'Responsable debe incorporar al delegado oportunamente en todas las etapas del programa.',(62,3):'Responsable debe proveer información necesaria sobre sus tratamientos.',
(66,1):'Delegado se ocupa de formación y capacitación permanentes de quienes tratan datos.',(66,2):'Puede recomendar periodicidad y materias de esa formación.',
(69,1):'Delegado planifica anualmente y rinde resultados al menos cada año ante quien lo designó.',(69,2):'Delegado difunde internamente tanto el plan como sus resultados.',
(71,1):'Delegado supervisa que datos y medio de contacto estén actualizados y públicos.',(71,2):'Delegado procura respuesta oportuna a consultas y solicitudes de titulares.',
(72,1):'Delegado coopera con Agencia y actúa como punto de contacto.',(72,2):'Delegado colabora en requerimientos de Agencia y dispone información íntegra y oportunamente.',
(73,1):'Responsable individualiza delegado ante Agencia con nombre completo y contacto directo.',(73,2):'Responsable comunica a Agencia cambios de designación o contacto.',
(79,1):'Inicia certificación a solicitud y aplica Ley 19.880 e instrucciones generales.',(79,2):'Permite a Agencia contratar terceros para estudiar solicitudes bajo Ley 19.886.',
(87,1):'Cese voluntario de actividad certificada extingue la certificación.',(87,2):'Responsable avisa cese a la Agencia dentro de treinta días.',
(88,1):'El término de la certificación no puede oponerse a terceros mientras no se elimine del registro.',(88,2):'Agencia ordena eliminación con revocación o dentro de cinco días hábiles de conocer otra causal.',
(90,1):'Agencia registra responsables con certificación vigente e identifica responsable y representante cuando corresponda.',(90,2):'En servicios centralizados el representante registral es el jefe de servicio.',(90,3):'Agencia registra fecha de incorporación y vencimiento.',
(95,1):'Faculta a la Agencia para exigir información necesaria a la supervisión.',(95,2):'Delegado debe entregar información requerida íntegra y oportunamente dentro de su función.',(95,3):'Responsable puede exceptuarse solo por secreto o confidencialidad con norma identificada y causal acreditada.',
(97,1):'Permite revocación fundada si se infringen o incumplen requisitos de certificación.',(97,2):'Permite revocación si hay sanción por infracciones de artículos 34 bis a quáter con infracción del artículo 48.',
(99,1):'Permite nueva solicitud tras revocación si se cumplen requisitos y se acredita subsanación.',(99,2):'Exige aportar antecedentes sobre medidas adoptadas para prevenir reiteración.'}
def typ(i,j):
 if i==1:return 'acto aprobatorio'
 if i==4:return 'delimitación del objeto'
 if i==5:return 'permiso expreso de adopción voluntaria'
 if i==6:return 'conservación del deber general de cumplimiento'
 if i==7:return 'remisión normativa'+(' supletoria' if j==2 else ' de definiciones')
 if i==12:return 'definición del programa' if j==1 else 'obligación de contenido mínimo'
 if i==33 and j==2:return 'facultad normativa de la Agencia'
 if i==44 and j==2:return 'obligación de individualizar al delegado'
 if i==66 and j==2:return 'facultad de recomendación del delegado'
 if i==81:return 'plazo de vigencia y renovación a petición'
 if i==91:return 'publicidad registral'
 if i==99 and j==2:return 'deber de aportar antecedentes'
 if i in (28,32,44,48,49,51,93,99):return 'permiso condicionado' if i not in (32,) or j==3 else 'contenido mínimo del programa'
 if i in (76,79,94,95,97,98):return 'atribución de la Agencia' if not (i==95 and j==2) else 'deber del delegado'
 if i==88 and j==1:return 'inoponibilidad frente a terceros'
 if i==90 and j==2:return 'definición del representante registral'
 if i in (77,78,80,88,90,92,100):return 'deber o decisión de la Agencia'
 if i in (82,83,84,85,86,87):return 'causal de término de certificación' if i!=87 or j==1 else 'deber de aviso'
 if i in (40,52,96):return 'límite, prohibición o consecuencia sancionatoria'
 if i in (60,61,63,64,65,66,67,68,69,70,71,72):return 'función mínima del delegado'
 if i==43:return 'permiso de designación con deber condicionado' if j==1 else 'alcance funcional del delegado'
 if i==46 and j==2:return 'definición de autoridad designante'
 if i==95 and j==3:return 'excepción acreditada al deber de informar'
 return 'obligación de contenido, actuación o procedimiento'
# Condiciones, excepciones y remisiones se extraen también de cada literal; anotamos dónde inciden.
cond={5:'Adopción voluntaria; cualquier responsable; ajuste a ley y reglamento.',7:'Supletoriedad solo salvo disposición legal en contrario.',13:'Representante legal solo si corresponde.',17:'Datos sensibles o especiales cuando se traten.',22:'Fuente de acceso público solo si procede.',23:'Interés legítimo si la base es artículo 13 letra d).',27:'Detalle de lógica y consecuencias si existen estas operaciones.',28:'Registro de actividades como medio posible, no obligatorio.',29:'Actividades habituales o esporádicas; mayor riesgo y graduación sancionatoria.',31:'Adecuación al tipo y escala del responsable.',32:'Canal existente solo si cumple ley y reglamento.',33:'Reportes a titulares o autoridad según corresponda; órganos públicos conservan regla especial.',35:'Solo organismos públicos.',36:'Reserva a solicitud del denunciante; ninguna medida desfavorable por denuncia.',38:'Incorporación al reglamento interno y publicidad cuando corresponde.',43:'Obligatoria solo dentro de adopción y certificación del programa.',44:'Proveedor persona jurídica y delegado plural sujetos a requisitos expresos.',45:'Órganos públicos que establezcan la función.',48:'Micro, pequeñas y medianas empresas.',49:'Estándares y políticas comunes; acceso equivalente.',50:'Suficiencia ponderada según características de entidad y tratamientos.',52:'Salvedad del artículo 50 inciso tercero para mipymes.',56:'Órganos públicos: sin perjuicio de decreto 181.',57:'Expedita y directa.',59:'Información conocida en ejercicio o con ocasión del cargo.',62:'En elaboración, revisión o modificación del programa.',68:'Evaluación de impacto del artículo 15 ter.',71:'En ejercicio de atención de consultas y solicitudes.',72:'Respecto de la atribución del artículo 30 bis letra c).',79:'A solicitud; Ley 19.880; terceros sujetos a Ley 19.886.',80:'Incorporación al registro si certifica.',81:'Tres años; renovación a solicitud.',84:'Responsable persona natural.',87:'Treinta días desde el cese.',88:'Inoponibilidad hasta cancelación; plazo de cinco días hábiles en los casos descritos.',89:'Nueva solicitud tras revocación.',92:'A petición del responsable o representante.',93:'Inicio anterior a registro con plena sujeción normativa.',95:'Excepción exige norma de secreto o confidencialidad y acreditación.',97:'Revocación fundada; causales alternativas.',98:'De oficio o a petición.',99:'Nueva solicitud solo tras subsanación acreditada.'}
cond.update({14:'Designación conforme al artículo 8 del reglamento.',15:'Medios y facultades conforme al Párrafo II del Título II.',18:'Ámbito territorial según artículo 1° bis de la Ley 19.628.',46:'Autoridad determinada según la forma de organización del responsable.',47:'Rendición ante la autoridad que efectuó la designación.',58:'Terceros encargados solo cuando corresponda.',63:'Disponibilidad para miembros, mandatarios y titulares según corresponda.',64:'Otras autoridades dentro de su competencia.',65:'Medidas disciplinarias y sanción solo si corresponden.',77:'Solo modelos que cumplen requisitos legales y reglamentarios.',90:'Entidad con certificación vigente; representante legal cuando corresponda; servicio centralizado como supuesto especial.',100:'Nueva resolución sobre solicitud posterior a revocación.'})
fragment_conditions={
 (7,1):'Definiciones de la Ley 19.628; no se expresa excepción adicional.',(7,2):'Ley 19.880 salvo disposición legal en contrario.',
 (27,1):'Indicar existencia de decisiones automatizadas y perfiles.',(27,2):'Información adicional solo si realiza esas operaciones.',
 (29,1):'Actividades habituales o esporádicas con riesgo de infracción.',(29,2):'Seleccionar actividades identificadas de mayor riesgo.',(29,3):'Graduación de sanciones legales para desarrollar matriz.',
 (32,1):'Mecanismo referido al cumplimiento o infracciones de datos.',(32,2):'Acceso expedito y permanente para miembros de la organización.',(32,3):'Integración a canal existente solo si satisface ley y reglamento.',
 (33,1):'Reportes a autoridad o titulares según proceda y en supuestos legales citados.',(33,2):'Instrucción general posible; para órganos públicos rige la salvedad del decreto 181.',
 (36,1):'Denuncias de infracciones de tratamiento ante delegado.',(36,2):'Reserva de identidad a solicitud del denunciante.',(36,3):'Prohibición de medidas desfavorables causadas por la denuncia.',
 (38,1):'Regulación interna surgida al implementar el programa, si existe.',(38,2):'Incorporación al reglamento interno en los casos que corresponda.',(38,3):'Publicidad solo en este último caso.',
 (39,1):'Difusión a trabajadores, empleados y prestadores.',(39,2):'Misma difusión al modificar o actualizar programa.',
 (43,1):'Designación obligatoria dentro de adopción y certificación del programa.',(43,2):'Todas las operaciones del responsable que designa delegado en ese supuesto.',
 (44,1):'Delegado dependiente o contratado.',(44,2):'Proveedor persona jurídica debe identificar persona natural.',(44,3):'Una persona para varios responsables solo si cumple requisitos.',
 (46,1):'Designación por máxima autoridad.',(46,2):'Cargo aplicable según la entidad.',
 (47,1):'Autonomía en materias relacionadas con la ley.',(47,2):'Cuenta directa ante quien lo designó.',
 (52,1):'Independencia exigida cualquiera sea el vínculo del delegado.',(52,2):'Excepción legal para mipymes del artículo 50 inciso tercero.',
 (56,1):'Publicación para contacto de titulares y ejercicio de sus derechos.',(56,2):'Salvedad para órganos públicos del artículo 47 del decreto 181.',
 (62,1):'Programa revisado, modificado o nuevo, según el caso.',(62,2):'Participación oportuna en todas las etapas.',(62,3):'Información que necesite respecto de tratamientos del responsable.',
 (66,1):'Personas de la organización que participan en tratamiento.',(66,2):'Recomendación facultativa de periodicidad y materias.',
 (69,1):'Cuenta de resultados al menos anual ante autoridad designante.',(69,2):'Difusión del plan y resultados al interior de la organización.',
 (71,1):'Información y contacto permanentemente actualizados y disponibles.',(71,2):'Respuesta oportuna a titulares.',
 (72,1):'Punto de contacto con la Agencia.',(72,2):'Colaboración en atribución del artículo 30 bis letra c).',
 (73,1):'Nombre completo y medio directo y expedito.',(73,2):'Cualquier cambio de designación o contacto.',
 (79,1):'Inicio a solicitud; Ley 19.880 e instrucción general.',(79,2):'Contratación de terceros conforme a Ley 19.886.',
 (87,1):'Cese voluntario de actividad objeto del modelo.',(87,2):'Aviso dentro de treinta días siguientes al cese.',
 (88,1):'Término inoponible hasta eliminar asiento del registro.',(88,2):'Eliminación con revocación o dentro de cinco días hábiles de conocimiento de otra causal.',
 (90,1):'Entidad con certificación vigente; representante legal cuando corresponda.',(90,2):'Solo servicios centralizados.',(90,3):'Fecha de incorporación y vencimiento del certificado.',
 (95,1):'Información necesaria para supervisar.',(95,2):'Entrega íntegra y oportuna dentro de funciones del delegado.',(95,3):'Excepción solo con obligación de secreto o confidencialidad fundada en norma y causal acreditada.',
 (97,1):'Incumplimiento de requisito legal o reglamentario de certificación.',(97,2):'Sanción por infracción indicada, con infracción del artículo 48.',
 (99,1):'Requisitos completos y subsanación fehaciente de causal.',(99,2):'Antecedentes de medidas para prevenir reiteración de la infracción.'}
# Remisiones visibles y verificables en el propio literal; no se afirma haber contrastado la norma remitida.
ref_pat=re.compile(r'(?:artículos?\s+[\d°]+(?:\s*(?:bis|ter|quáter|sexies))?|ley\s+N°\s*[\d.]+|decreto supremo N°\s*\d+|Código del Trabajo|Párrafo\s+[IVX]+)',re.I)
source_short='Decreto supremo N° 662, Ministerio de Hacienda; versión única publicada 09-SEP-2026'
all_nodes=[]
for n,ids in arts.items():
 folder=root/f'articulo-{n:02d}';folder.mkdir(exist_ok=True)
 links=[]
 for k,i in enumerate(ids,1):
  b=blocks[i];base=label(n,i,k)
  body=b['body']
  if i in split:
   parts=split_sentences(body)
  else:parts=[body]
  # Una oración separada no es un título ni marcador vacío.
  assert all(len(s)>5 for s in parts),(i,parts)
  for j,s in enumerate(parts,1):
   name=base+(f'-fragmento-{j}' if len(parts)>1 else '')
   path=folder/(name+'.md')
   loc=f'Artículo {n}, {base.replace("-"," ")}' + (f', fragmento {j}' if len(parts)>1 else '')
   pages=', '.join(map(str,b['pages']))
   intro=''
   if n in (3,13,16) and base!='enunciado':
    intro={3:'La enumeración depende del [enunciado del artículo 3](enunciado-fragmento-2.md): contenido mínimo del programa.',13:'La letra integra las funciones mínimas del delegado anunciadas en el [enunciado del artículo 13](enunciado.md).',16:'La letra integra las causales de pérdida de efecto del certificado anunciadas en el [enunciado del artículo 16](enunciado.md).'}[n]
   if base.startswith('letra-d-numeral'):
    intro+=' Pertenece a la [caracterización de la letra d)](letra-d-fragmento-2.md) del artículo 3.'
   if n==13 and i==71:intro='Continúa la [función de atención de titulares de la letra j)](letra-j.md), iniciada en la página 7.'
   if n==13 and i==73:intro='Párrafo posterior a la enumeración de funciones; el destinatario cambia al responsable.'
   if len(parts)>1:
    neighbors=[]
    if j>1:neighbors.append(f'[fragmento anterior]({base}-fragmento-{j-1}.md)')
    if j<len(parts):neighbors.append(f'[fragmento siguiente]({base}-fragmento-{j+1}.md)')
    intro+=f' Fragmento {j} de {len(parts)} del mismo párrafo impreso; contexto contiguo: {", ".join(neighbors)}.' 
   rr=sorted(set(ref_pat.findall(s)))
   refs='; '.join(rr) if rr else 'Sin remisión expresa en este literal.'
   condition=fragment_conditions.get((i,j),cond.get(i,'Sin condición o excepción expresa adicional en este fragmento; se conserva su contexto en el artículo.'))
   analysis=fragment_notes.get((i,j),notes[i])
   uncertainty=''
   if i==80:
    uncertainty=' La remisión al «inciso siguiente» fue verificada literalmente: el inciso cuarto existe, pero regula vigencia y renovación, sin describir el registro. Se conserva la redacción y se deja abierta su correspondencia sustantiva con el artículo 17.'
   # La comprobación compara el literal normalizado con el bloque completo; el informe documenta verificación visual.
   text=f'''# {loc}\n\n- **Fuente:** {source_short}.\n- **Localizador:** {loc}.\n- **PDF original:** `{source}`, página(s) {pages}.\n- **Artículo:** [articulo.md](articulo.md).\n\n## Texto literal\n\n> {s}\n\n## Contexto y análisis normativo\n\n{intro.strip() or 'Este párrafo se lee dentro del artículo completo y bajo su rúbrica.'}\n\n- **Clasificación propuesta:** {typ(i,j)}.\n- **Función propuesta:** {analysis}\n- **Condiciones y excepciones:** {condition}\n- **Remisiones expresas del fragmento:** {refs}\n- **Límite del análisis:** Esta clasificación describe la función del texto; no extrae una Exigencia ni comprueba el contenido de las normas remitidas.\n\n## Comprobación de fragmentación\n\nLiteral cotejado con el bloque impreso del artículo {n} en página(s) {pages}, conservando orden, puntuación y marcadores. Solo se normalizaron saltos de línea y espacios de maquetación. En este artículo se comprobaron las unidades vecinas y la continuidad de las páginas; no queda duda textual identificada en este localizador.{uncertainty}\n'''
   path.write_text(text)
   links.append((name,path,base,i,j,len(parts)))
   all_nodes.append({'article':n,'block':i,'part':j,'literal':s,'path':str(path),'pages':b['pages'],'base':base})
 # Contexto del artículo, sin duplicación del literal en articulo.md.
 first=min(blocks[i]['pages'][0] for i in ids);last=max(blocks[i]['pages'][-1] for i in ids)
 specific=article_summaries[n]
 ap=f'''# Artículo {n}. {article_titles[n]}\n\n- **Cuerpo:** reglamento aprobado por Decreto supremo N° 662, Ministerio de Hacienda.\n- **Versión:** única de 09-SEP-2026; promulgación del decreto 13-JUN-2025.\n- **Original:** `{source}`, página(s) {first}{f'–{last}' if last!=first else ''}.\n- **Rúbrica literal:** «{article_titles[n]}».\n- **Función en conjunto:** {specific}\n- **Estructura:** {len(ids)} bloques de texto impresos, desglosados en {len(links)} archivos de literal. Se conserva el orden del PDF y, cuando procede, la jerarquía de su enumeración.\n\n## Unidades\n\n'''
 for name,path,base,i,j,np in links:ap+=f'- [{name}]({name}.md) — p. {"–".join(map(str,blocks[i]["pages"]))}.\n'
 ap+='\n## Comprobación\n\nSe leyó el artículo íntegro antes de fijar cortes. Se reconstruyó su secuencia desde los literales enlazados y se cotejó con los bloques de texto del PDF, incluidos los párrafos que cruzan página. Los títulos y encabezados son contexto, no disposiciones añadidas.\n'
 (folder/'articulo.md').write_text(ap)
# Fórmula aprobatoria autónoma del acto, anterior al Título I.
ap_folder=root/'acto-aprobatorio';ap_folder.mkdir(exist_ok=True)
ap=blocks[1]['text']
(ap_folder/'articulo.md').write_text(f'''# Acto aprobatorio del Decreto 662\n\n- **Localizador:** fórmula «Decreto: Apruébase…», página 2 del PDF. El original no la numera como «artículo único».\n- **Relación:** aprueba el reglamento cuyo Título I comienza después de esta fórmula; los artículos 1 a 20 pertenecen a ese reglamento.\n- **Fuente y versión:** {source_short}; `{source}`.\n\n## Texto literal\n\n> {ap}\n\n## Análisis normativo\n\n{notes[1]} La fórmula refiere a la Ley N° 21.719 y a la Ley N° 19.628, sin reproducir su contenido.\n\n## Comprobación\n\nCotejado con la página 2: sigue inmediatamente a «Decreto:» y precede «Título I». No aparece numeración «artículo único» en el PDF. Solo se normalizaron saltos de línea y espacios de maquetación.\n''')
# Árbol integral, con estado de fragmentación y rutas de cada unidad.
tree=['# Árbol de fragmentación — Decreto 662, versión única 09-SEP-2026','','Original: `'+source+'`. Estados referidos solo a esta fragmentación. No hay disposiciones transitorias en el documento.','','```text','Decreto 662 / acto aprobatorio y reglamento [completo]','|-- Visto y considerandos [contexto, p. 1–2]','|-- Acto aprobatorio: «Apruébase…» [completo] -> acto-aprobatorio/articulo.md','|-- Título I. Disposiciones generales [contexto]']
for n in range(1,21):
 if n==3:tree.append('|-- Título II. De los programas de cumplimiento [contexto]');tree.append('|   |-- Párrafo 1. Elementos y publicidad de los programas de cumplimiento [contexto]')
 if n==6:tree.append('|   |-- Párrafo II. El Delegado de Protección de Datos [contexto]')
 if n==14:tree.append('|   `-- Párrafo III. De la aprobación, certificación, registro, implementación y supervisión de los programas de cumplimiento [contexto]')
 tree.append(f'|-- Artículo {n}. {article_titles[n]} [completo] -> articulo-{n:02d}/articulo.md')
 groups=[]
 for x in [x for x in all_nodes if x['article']==n]:
  if not groups or groups[-1][0]!=x['base']:groups.append((x['base'],[]))
  groups[-1][1].append(x)
 for base,xs in groups:
  nested=(n==3 and (base.startswith('letra-d-numeral-') or base in ('letra-d-parrafo-final','letra-f-parrafo-2','letra-g-parrafo-2','letra-h-parrafo-2'))) or (n==13 and base=='letra-j-parrafo-2')
  pref='|   |   |-- ' if nested else '|   |-- '
  shown=base.replace('letra-','letra ').replace('-numeral-',' > numeral ').replace('-parrafo-',' > párrafo ').replace('inciso-','inciso ').replace('fragmento-','fragmento ')
  if len(xs)>1:
   tree.append(pref+shown+' [completo]')
   for x in xs:
    path=Path(x['path']).name
    tree.append(('|   |   |   |-- ' if nested else '|   |   |-- ')+f'fragmento {x["part"]} [completo] -> articulo-{n:02d}/{path}')
  else:
   path=Path(xs[0]['path']).name
   tree.append(pref+shown+f' [completo] -> articulo-{n:02d}/{path}')
tree.extend(['`-- Fórmula de promulgación, firmas y transcripción [contexto, p. 10]','```','', 'Los numerales i–xi están bajo la letra d) del artículo 3. Los párrafos posteriores a las letras d), f), g) y h) del artículo 3 y a la letra j) del artículo 13 conservan su posición. Los fragmentos de oración solo separan reglas con destinatario o efecto propio; mantienen el mismo párrafo impreso.'])
(root/'ARBOL.md').write_text('\n'.join(tree)+'\n')
(root/'FUENTE.md').write_text(f'''# Fuente — Decreto supremo N° 662\n\n- **Cuerpo y versión:** Decreto supremo N° 662, Ministerio de Hacienda, versión única de 09-SEP-2026.\n- **Promulgación:** 13-JUN-2025. **Publicación:** 09-SEP-2026.\n- **Original encargado:** `{source}` (10 páginas).\n- **SHA-256:** `{sha}`.\n- **Objeto declarado:** reglamento de requisitos, modalidades y procedimientos de implementación, certificación, registro y supervisión de modelos de prevención de infracciones.\n- **Estructura:** visto y siete considerandos como contexto; fórmula aprobatoria sin número propio; reglamento aprobado con Títulos I y II, Párrafos 1, II y III, artículos 1 a 20; sin artículos transitorios.\n- **Inventario compacto:** acto aprobatorio (p. 2); artículos 1–2 (p. 2); artículos 3–4 (p. 3–5); artículos 5–8 (p. 5); artículos 9–12 (p. 5–7); artículo 13 (p. 7–8); artículos 14–16 (p. 8–9); artículos 17–20 (p. 9–10). Detalle y estado en [ARBOL.md](ARBOL.md).\n- **Método:** extracción con pypdf, lectura de artículos completos, cotejo de páginas renderizadas y comprobación de secuencia literal. Se normalizaron solo saltos de línea y espacios de maquetación; se conservaron tildes, puntuación y enumeradores.\n- **Alcance:** inventario y fragmentación de Disposiciones; no se extrajeron Exigencias ni se hizo auditoría independiente.\n''')
Path('tmp/pdfs/decreto-662/manifest.json').write_text(json.dumps(all_nodes,ensure_ascii=False,indent=2))
print('articles',len(arts),'block units',sum(map(len,arts.values())),'literal files',len(all_nodes),'sha',sha)

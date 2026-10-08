import json
import re
from pathlib import Path

from inventory import ROOT, DEST, art_slug, art_label, section

ART_RE = re.compile(r'^Artículo\s+\d+[°º]?(?:\s+(?:bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?\.-\s*')
ENUM_RE = re.compile(r'^(?:[a-zñ]\)|[ivx]+\.|\d+\.)\s+')
COND_RE = re.compile(r'\b(?:cuando|siempre que|salvo|excepto|con excepción de|sin perjuicio de|en caso de|a menos que|únicamente|sólo si|si [a-záéíóú])\b[^.;:]*',re.I)
REF_RE = re.compile(r'\b(?:artículos?\s+\d+[°º]?(?:\s+(?:bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?|inciso\s+(?:primero|segundo|tercero|anterior|siguiente)|Título\s+(?:[IVX]+|Preliminar)|ley\s+N[°º]\s*\d+[\.\d]*|decreto\s+supremo(?:\s+de\s+Hacienda)?\s+N[°º]\s*\d+|Constitución Política de la República|reglamento)\b',re.I)
GENERIC_REF_RE = re.compile(r'\b(?:que la ley le encomiende|que la ley le entregue|de conformidad a (?:esta|la) ley|previst[oa]s? en esta ley|establecid[oa]s? en esta ley|que establezcan otras leyes|que disponga la ley)\b',re.I)

ANALYSIS_OVERRIDES = {
 (2,'',11): 'La letra i define las fuentes de acceso público por la posibilidad de consulta lícita por cualquiera, pero su segunda oración conserva una consecuencia distinta: los datos obtenidos de ellas siguen sujetos a esta ley. La publicidad de la fuente no dispensa el régimen de tratamiento.',
 (13,'',5): 'La letra d habilita el tratamiento sin consentimiento por interés legítimo del responsable o de un tercero solo si no se afectan derechos y libertades del titular. Además reconoce al titular la facultad de exigir información sobre el tratamiento y el interés invocado; esa segunda garantía no desaparece por existir la base de licitud.',
 (14,'sexies',2): 'Impone al responsable registrar los reportes de vulneraciones dirigidos a la Agencia conforme al inciso primero. El registro debe documentar naturaleza y efectos del incidente, categorías de datos, número aproximado de titulares y medidas de gestión y prevención futura.',
 (14,'sexies',3): 'Extiende el reporte a los titulares cuando la vulneración afecta datos sensibles, de menores de catorce años o de obligaciones económicas. Precisa el contenido claro de la comunicación y exige notificación individual; si ésta no es posible, permite aviso masivo nacional.',
 (15,'bis',1): 'Permite al responsable encargar a un tercero el tratamiento, pero vincula al encargado a las instrucciones y al objeto pactado. Prohíbe usos, cesiones o entregas ajenos al encargo sin autorización expresa y específica del responsable.',
 (16,'',4): 'La letra b establece una base excepcional para entidades públicas o privadas sin fines de lucro que persigan un interés legítimo. Los cinco ordinales que la siguen son condiciones acumulativas sobre finalidad, miembros, finalidad institucional, garantías y prohibición de cesión.',
 (16,'',10): 'Cumplidos todos los ordinales de la letra b, la entidad deja de necesitar consentimiento para tratar los datos de sus miembros, incluso si son sensibles. En controversia, recae en el responsable acreditar cada condición.',
 (16,'',11): 'Cuando una persona deja de ser miembro de la entidad comprendida en la letra b, sus datos deben anonimizarse o suprimirse. Este deber cierra la excepción asociada a la pertenencia a la entidad.',
 (20,'',1): 'Autoriza el tratamiento público sin consentimiento únicamente para cumplir funciones legales dentro de la competencia del órgano y conforme a este título. En esas condiciones el órgano adquiere la calidad de responsable de datos.',
 (30,'bis',2): 'Atribuye a la Agencia potestad de dictar instrucciones y normas generales obligatorias sobre tratamiento. La somete a consulta pública y limita su contenido a lo necesario para cumplir esta ley.',
 (30,'ter',2): 'Atribuye al Consejo Directivo el ejercicio de las atribuciones y el cumplimiento de las funciones que la ley encomienda a la Agencia. La referencia legal es genérica: no señala aquí un artículo concreto, pero remite al conjunto de competencias legales de la Agencia.',
 (49,'',1): 'Permite al responsable adoptar voluntariamente un modelo de prevención materializado en un programa de cumplimiento. La voluntariedad se refiere al modelo, no al deber general de prevenir infracciones del artículo 48.',
 (50,'',1): 'Faculta al responsable a designar un delegado de protección de datos. La designación es potestativa en este inciso y, si se realiza, se sujeta a requisitos y funciones desarrollados después en el artículo.',
 (50,'',8): 'El párrafo impone confidencialidad al delegado respecto de los datos conocidos en su cargo; remite a la sanción penal de los funcionarios públicos que incumplan ese deber; y hace responder al responsable por la infracción de su encargado de prevención o delegado, conservando su eventual acción de repetición contra éste. La acción de repetición no exceptúa el deber de secreto.',
 (54,'',1): 'Reconoce licitud al tratamiento de las instituciones y órganos autónomos enumerados si actúan dentro de sus funciones y leyes orgánicas, con las excepciones expresas al Título IV. Les asigna calidad de responsables sin requerir consentimiento, pero impone secreto a sus funcionarios.',
}

ANALYSIS_OVERRIDES.update({
 (1,'bis',2): 'Hace aplicable la ley por establecimiento o constitución del responsable o mandatario en Chile; el lugar de los titulares o de los servidores no forma parte de esta causal.',
 (1,'bis',3): 'Extiende la aplicación al mandatario situado fuera de Chile que trata datos por cuenta de un responsable establecido o constituido en el país.',
 (1,'bis',4): 'Alcanza a responsables o mandatarios no establecidos en Chile cuando ofrecen bienes o servicios a personas en el país o monitorean su conducta; el pago no es requisito para la primera hipótesis.',
 (1,'bis',5): 'Añade la aplicación de la ley al responsable extranjero sujeto a legislación chilena por contrato o por derecho internacional, aunque no concurra una causal territorial de las letras anteriores.',
 (2,'',8): 'Precisa el criterio de identificabilidad de la letra f: se consideran los medios y factores objetivos razonablemente utilizables al momento del tratamiento; evita reducir el concepto a identificadores expresos.',
 (2,'',25): 'Completa la definición de portabilidad de la letra u con transmisión directa entre responsables cuando sea técnicamente posible.',
 (4,'',2): 'Declara personales, intransferibles e irrenunciables los derechos del titular e impide que un acto o convención los limite.',
 (4,'',3): 'Permite a los herederos ejercer los derechos reconocidos al titular fallecido, sujeto al límite del inciso siguiente.',
 (4,'',4): 'Restringe el acceso, rectificación y supresión pedidos por herederos si el causante lo prohibió expresamente o una ley así lo establece.',
 (6,'',1): 'Reconoce al titular la rectificación de datos tratados por el responsable cuando sean inexactos, desactualizados o incompletos.',
 (6,'',3): 'Prohíbe volver a tratar la versión sin rectificar una vez efectuada la corrección, cerrando la posibilidad de reintroducir el dato defectuoso.',
 (8,'ter',1): 'Reconoce bloqueo temporal mientras se resuelve una solicitud de rectificación, supresión u oposición formulada conforme al artículo 11; suspende operaciones de tratamiento, no el almacenamiento.',
 (8,'ter',2): 'Permite solicitar bloqueo como alternativa a la supresión en las causales del artículo 7°, no solo durante el trámite de una solicitud.',
 (8,'ter',3): 'Aclara que el bloqueo suspende operaciones de tratamiento sin obligar a destruir o dejar de almacenar los datos.',
 (9,'',2): 'Exige tratamiento automatizado como primera condición acumulativa para la portabilidad.',
 (9,'',3): 'Exige consentimiento del titular como base de licitud de ese tratamiento, junto con la automatización de la letra a.',
 (9,'',6): 'Habilita transmisión directa de datos entre responsables cuando sea técnicamente posible, como modalidad adicional a la entrega de copia al titular.',
 (9,'',7): 'El ejercicio de portabilidad no elimina por sí solo los datos que conserva el responsable cedente; la supresión requiere su propio fundamento o ejercicio.',
 (10,'',3): 'Obliga a los responsables a habilitar mecanismos tecnológicos para ejercer derechos de modo expedito y simple, y no solo a recibir solicitudes por canales existentes.',
 (10,'',4): 'Establece gratuidad absoluta de rectificación, supresión y oposición y la regla de gratuidad del acceso, con los límites de cobro desarrollados a continuación.',
 (10,'',6): 'Remite a la Agencia la determinación de parámetros y mecanismos para calcular los costos excepcionales de ejercicio de derechos.',
 (10,'',7): 'Asigna a la Agencia velar por el ejercicio efectivo de los derechos del titular conforme a las atribuciones que le confiere la ley.',
 (11,'',9): 'Frente al silencio del responsable tras el plazo legal, permite al titular reclamar directamente ante la Agencia; el vencimiento del plazo activa esa vía.',
 (11,'',12): 'Permite al titular agregar antecedentes que faciliten localizar sus datos, aun después de los requisitos mínimos de la solicitud.',
 (12,'',1): 'Establece el consentimiento del titular como base general de licitud para tratar los datos que le conciernen; los requisitos y límites de ese consentimiento se desarrollan en los incisos siguientes.',
 (12,'',4): 'Permite revocar el consentimiento en cualquier momento y sin causa, por medios equivalentes a los usados para otorgarlo; la revocación opera hacia el futuro.',
 (12,'',5): 'Exige canales de otorgamiento y revocación expeditos, fidedignos, gratuitos y disponibles permanentemente, para que el derecho de revocar sea practicable.',
 (12,'',6): 'Presume falta de libertad del consentimiento recabado como condición contractual o de servicio si los datos no son necesarios para la ejecución respectiva.',
 (12,'',8): 'Impone al responsable la carga de probar tanto el consentimiento como la licitud, lealtad y transparencia del tratamiento.',
 (14,'bis',2): 'Conserva la posibilidad de comunicar o ceder datos por deber legal y de dar acceso al titular o a un órgano competente; esos supuestos limitan el secreto sin eliminarlo.',
 (14,'bis',4): 'Extiende la confidencialidad a las instituciones y personas del artículo 24 y a sus dependientes respecto del requerimiento y del hecho de entregar la información.',
 (14,'septies',1): 'Ordena graduar los estándares mínimos de información y seguridad según tipo de dato, naturaleza y tamaño del responsable, actividad, volumen y finalidad del tratamiento.',
 (14,'septies',2): 'Atribuye a la Agencia fijar por instrucción general los estándares mínimos y medidas diferenciadas descritos en el inciso primero.',
 (15,'',1): 'Permite ceder datos con consentimiento y para los fines del tratamiento, y también por contrato, interés legítimo o habilitación legal en los supuestos expresos del inciso.',
 (15,'',5): 'Tras perfeccionarse la cesión, el cesionario pasa a ser responsable; el cedente mantiene esa calidad por los tratamientos que continúe realizando.',
 (15,'bis',5): 'Al concluir el encargo, obliga a devolver o suprimir los datos que conserva el tercero, según corresponda; el fin del servicio no legitima retenerlos indefinidamente.',
 (16,'',1): 'Establece consentimiento expreso como regla general para datos sensibles, manifestado verbalmente, por escrito o por medio tecnológico equivalente.',
 (16,'',16): 'Extiende las excepciones de tratamiento sin consentimiento del artículo a datos que no son sensibles, evitando leerlas como exclusivas de esa categoría.',
 (16,'bis',1): 'Incluso con consentimiento expreso conforme al artículo 16, limita los datos de salud y perfil biológico a los fines previstos en leyes sanitarias especiales.',
 (16,'bis',10): 'Extiende las excepciones de consentimiento de este régimen especial a datos que no revisten la calidad especial tratada por el artículo.',
 (16,'ter',1): 'Define los datos biométricos por su origen en tratamiento técnico de características físicas, fisiológicas o conductuales y su aptitud para identificar unívocamente.',
 (16,'ter',7): 'Permite tratar datos biométricos sin consentimiento únicamente en los casos que remite al inciso segundo del artículo 16 bis.',
 (16,'quáter',1): 'Condiciona todo tratamiento de datos de niños, niñas y adolescentes al interés superior y la autonomía progresiva, antes de las reglas específicas de consentimiento.',
 (16,'quáter',5): 'Fija para esta ley la frontera etaria: niño o niña menor de catorce años; adolescente mayor de catorce y menor de dieciocho.',
 (16,'quáter',6): 'Impone a establecimientos educacionales, cuidadores y demás entidades que tratan datos de menores un deber especial de uso lícito y protección de esa información.',
 (16,'quinquies',1): 'Reconoce interés legítimo para tratamientos exclusivamente históricos, estadísticos, científicos o de investigación solo cuando atiendan un fin de interés público.',
 (16,'quinquies',3): 'Permite publicar resultados de estos tratamientos, pero exige anonimizar previamente los datos divulgados.',
 (16,'sexies',1): 'Sujeta el tratamiento de geolocalización a las mismas bases de licitud de los artículos 12 y 13, sin crear una autorización autónoma.',
})

ANALYSIS_OVERRIDES.update({
 (35,'',2): 'Permite amonestación escrita o multa máxima de 5.000 unidades tributarias mensuales para infracción leve.',
 (36,'',2): 'Atenúa responsabilidad la reparación unilateral o el acuerdo reparatorio con titulares afectados.',
 (36,'',3): 'Atenúa responsabilidad la colaboración del infractor en la investigación administrativa de la Agencia.',
 (36,'',4): 'Atenúa responsabilidad la ausencia de sanciones previas del responsable.',
 (36,'',5): 'Atenúa responsabilidad la autodenuncia acompañada de medidas para cesar la infracción o mitigarla.',
 (36,'',6): 'Atenúa responsabilidad demostrar dirección y supervisión diligentes mediante el certificado del artículo 51.',
 (36,'',8): 'Agrava la reincidencia: al menos dos sanciones firmes en treinta meses por esta ley.',
 (36,'',9): 'Agrava el carácter continuado de la infracción.',
 (36,'',10): 'Agrava haber puesto en riesgo derechos y libertades de titulares respecto de sus datos.',
 (37,'',2): 'Manda considerar la gravedad propia de la conducta al fijar monto de multa.',
 (37,'',3): 'Manda considerar falta de diligencia cuando ésta no integra ya el tipo infraccional.',
 (37,'',4): 'Manda considerar el perjuicio y especialmente el número de titulares afectados.',
 (37,'',5): 'Manda considerar el beneficio económico obtenido por la infracción, si lo hubo.',
 (37,'',6): 'Manda considerar si el tratamiento incluyó datos sensibles o de niños, niñas y adolescentes.',
 (37,'',7): 'Manda considerar la capacidad económica del infractor.',
 (37,'',8): 'Manda considerar sanciones anteriores de la Agencia en circunstancias equivalentes.',
 (37,'',9): 'Manda ponderar atenuantes y agravantes concurrentes al calcular la multa.',
 (49,'',3): 'Exige designar delegado de protección de datos como pieza mínima del programa voluntario.',
 (49,'',4): 'Exige definir medios y facultades concretas del delegado dentro del programa.',
 (49,'',5): 'Exige inventariar datos, bases, territorio y titulares para conocer el perfil de riesgo del responsable.',
 (49,'',6): 'Exige identificar procesos que generan o aumentan riesgo de las infracciones de los artículos 34 bis a 34 quáter.',
 (49,'',7): 'Exige protocolos y procedimientos para que quienes ejecutan procesos de riesgo prevengan infracciones.',
 (49,'',8): 'Exige canales internos de reporte de cumplimiento y de reporte a la autoridad para incidentes del artículo 14 sexies.',
 (49,'',9): 'Exige sanciones internas y procedimientos para denunciar e investigar incumplimientos del sistema preventivo.',
 (50,'',11): 'Asigna al delegado asesorar a responsable, encargados y dependientes sobre obligaciones de protección de datos.',
 (50,'',12): 'Asigna al delegado promover y participar en la política de protección y tratamiento del responsable.',
 (50,'',13): 'Asigna al delegado supervisar cumplimiento de ley y política interna dentro de su competencia.',
 (50,'',14): 'Asigna al delegado impulsar formación continua de quienes intervienen en tratamientos.',
 (50,'',15): 'Asigna al delegado apoyar identificación de riesgos y medidas de protección de titulares.',
 (50,'',16): 'Asigna al delegado elaborar plan anual de trabajo y rendir cuenta de sus resultados.',
 (50,'',17): 'Asigna al delegado resolver consultas y solicitudes de titulares.',
 (50,'',18): 'Asigna al delegado cooperar con la Agencia y servir de punto de contacto.',
 (52,'',2): 'Termina anticipadamente el certificado si la Agencia lo revoca.',
 (52,'',3): 'Termina el certificado por muerte del responsable cuando es persona natural.',
 (52,'',4): 'Termina el certificado por disolución de la persona jurídica responsable.',
 (52,'',5): 'Termina el certificado por resolución judicial ejecutoriada.',
 (52,'',6): 'Termina el certificado por cese voluntario de la actividad del responsable.',
})

ANALYSIS_OVERRIDES.update({
 (41,'',3): 'Fija plazo de treinta días hábiles para reclamar tras rechazo o silencio; exige identificar decisión, fundamentos y canal de notificación.',
 (41,'',4): 'Permite a la Agencia suspender provisionalmente el tratamiento a petición fundada del titular en casos justificados y tras oír al responsable.',
 (41,'',5): 'Da a la Agencia diez días hábiles para revisar admisibilidad; exige fundar el rechazo y considera admitido el reclamo si guarda silencio.',
 (41,'',6): 'Tras admitir, ordena notificar al responsable y le otorga treinta días corridos prorrogables para contestar con antecedentes.',
 (41,'',7): 'Permite prueba por diez días hábiles solo si existen hechos sustanciales, pertinentes y controvertidos, haya o no respuesta del responsable.',
 (41,'',8): 'Regula allanamiento del responsable: exige acreditarlo, permite al titular pronunciarse diez días y luego archivar con sanción o instrucción si procede.',
 (41,'',9): 'Faculta a la Agencia a pedir antecedentes y convocar acuerdo; preserva competencia de sus funcionarios si fracasa la audiencia y archiva si hay acuerdo.',
 (41,'',10): 'Exige resolución fundada del reclamo y limita la duración total de la tutela administrativa a seis meses.',
 (41,'',11): 'Permite impugnar judicialmente inadmisión o decisión del reclamo dentro de quince días hábiles mediante el artículo 43.',
 (42,'',2): 'Entrega a la Agencia la instrucción del procedimiento sancionatorio.',
 (42,'',3): 'Permite iniciar de oficio o a petición tras fiscalización o reclamo; exige certificar reclamo y designar instructor al abrir expediente.',
 (42,'',4): 'Obliga a formular cargos describiendo hechos, principios, obligaciones y normas infringidas con antecedentes de sustento.',
 (42,'',5): 'Exige notificar los cargos al domicilio o canal electrónico del responsable declarado conforme al artículo 14 ter.',
 (42,'',6): 'Concede quince días hábiles para descargos y prueba del responsable, quien debe fijar canal para comunicaciones posteriores.',
 (42,'',7): 'Permite abrir prueba por diez días ante hechos sustanciales, pertinentes y controvertidos después de descargos o de vencer su plazo.',
 (42,'',8): 'Obliga a admitir diligencias probatorias pertinentes y necesarias pedidas por el responsable; exige fundar el rechazo.',
 (42,'',9): 'Permite cualquier prueba admisible en derecho y exige valorarla conforme a sana crítica.',
 (42,'',10): 'Faculta a la Agencia a pedir antecedentes e informes útiles para resolver el procedimiento sancionatorio.',
 (42,'',11): 'Exige decisión final fundada que resuelva defensas, declare infracción o absolución y, si sanciona, pondere agravantes y atenuantes.',
 (42,'',12): 'Exige motivar la resolución sancionatoria e informar recursos, órganos y plazos; abre revisión judicial del artículo siguiente.',
 (42,'',13): 'Limita el procedimiento a seis meses y permite reclamo de ilegalidad si vence ese plazo sin decisión.',
 (43,'',2): 'Exige al recurrente individualizar resolución, normas infringidas, modo de infracción y agravio si corresponde.',
 (43,'',3): 'Permite inadmisión por falta de requisitos y orden de no innovar ante daño irreparable por ejecutar el acto.',
 (43,'',4): 'Ordena a la Corte pedir informe a la Agencia con plazo de diez días.',
 (43,'',5): 'Permite abrir prueba judicial tras traslado cuando la Corte la considera necesaria, conforme a reglas de incidentes civiles.',
 (43,'',6): 'Tras prueba, ordena traer autos en relación y da preferencia a la vista de esta causa.',
 (43,'',7): 'Si acoge reclamo, la Corte determina agravio y ordena rectificar el acto o dictar nueva resolución según corresponda.',
 (43,'',8): 'En reclamos sancionatorios, permite a la Corte confirmar o revocar hechos, infracción, sanción o absolución.',
 (43,'',9): 'Aplica supletoriamente reglas del Código Orgánico de Tribunales y Código de Procedimiento Civil en lo no regulado.',
})

ANALYSIS_OVERRIDES.update({
 (7,'',2): 'Da derecho a supresión cuando los datos dejaron de ser necesarios para el fin por el que fueron recogidos.',
 (7,'',3): 'Da derecho a supresión tras revocar consentimiento si no existe otra base legal para continuar el tratamiento.',
 (7,'',4): 'Da derecho a supresión frente a obtención o tratamiento ilícitos por el responsable.',
 (7,'',5): 'Da derecho a supresión de datos caducos conforme a la definición legal de caducidad.',
 (7,'',6): 'Da derecho a supresión exigida por sentencia, resolución de la autoridad de datos u obligación legal.',
 (7,'',7): 'Da derecho a supresión tras oposición del titular cuando no subsiste otra base legal de tratamiento.',
 (7,'',9): 'Excluye supresión si los datos son necesarios para ejercer libertad de opinión o de información.',
 (7,'',10): 'Excluye supresión necesaria para obligación legal o ejecución de contrato entre titular y responsable.',
 (7,'',11): 'Excluye supresión necesaria para función pública o actividad de interés público.',
 (7,'',12): 'Excluye supresión por interés público sanitario bajo las condiciones y garantías que fija la ley.',
 (7,'',13): 'Excluye supresión cuando los datos son necesarios para fines históricos, estadísticos, científicos o investigación de interés público.',
 (7,'',14): 'Excluye supresión necesaria para formular, ejercer o defender reclamación administrativa o judicial.',
 (8,'',2): 'Permite oposición al tratamiento basado en interés legítimo; el responsable debe cesar salvo que pruebe motivos imperiosos prevalentes o necesidad para reclamaciones.',
 (8,'',3): 'Permite oposición al tratamiento para marketing directo, incluido perfilamiento relacionado, sin exigir motivación al titular.',
 (8,'',4): 'Permite oposición si los datos provienen de fuente pública y el responsable carece de otra base legal.',
 (8,'bis',3): 'Exceptúa el derecho frente a decisión automatizada cuando la decisión es necesaria para celebrar o ejecutar contrato con el titular.',
 (8,'bis',4): 'Exceptúa la decisión automatizada si existe consentimiento previo y expreso conforme al artículo 12.',
 (8,'bis',5): 'Exceptúa decisiones automatizadas previstas por ley solo si ésta dispone salvaguardas de derechos y libertades del titular.',
 (13,'',2): 'Permite tratar sin consentimiento información de obligaciones económicas si se cumplen las reglas especiales del Título III.',
 (13,'',3): 'Permite tratar sin consentimiento cuando es necesario para cumplir una obligación legal o la ley lo dispone.',
 (13,'',4): 'Permite tratar sin consentimiento para contratar, ejecutar contrato o medidas precontractuales pedidas por el titular.',
 (13,'',6): 'Permite tratar sin consentimiento cuando es necesario para formular, ejercer o defender un derecho ante tribunales u órganos públicos.',
 (16,'',3): 'Exceptúa consentimiento para datos sensibles que el titular hizo manifiestamente públicos, solo si el nuevo uso se relaciona con el fin de publicación.',
 (16,'',12): 'Exceptúa consentimiento ante protección indispensable de vida, salud o integridad, o impedimento del titular; terminado éste exige informar los datos y operaciones tratados.',
 (16,'',13): 'Exceptúa consentimiento para datos sensibles necesarios para formular, ejercer o defender derechos ante tribunal u órgano administrativo.',
 (16,'',14): 'Exceptúa consentimiento si el tratamiento es necesario para derechos u obligaciones laborales o de seguridad social dentro de la ley.',
 (16,'',15): 'Exceptúa consentimiento cuando una ley autoriza o manda expresamente tratar datos sensibles.',
})

ANALYSIS_OVERRIDES.update({
 (23,'',6): 'Abre reclamo ante la Agencia por denegación expresa o tácita de derechos ante un órgano público y remite al procedimiento de tutela del artículo 41.',
 (35,'',6): 'Permite triplicar la multa de la infracción cometida si existe reincidencia según el artículo 36.',
 (35,'',7): 'Para empresas que no son de menor tamaño y reinciden en infracción grave o gravísima, permite aplicar el monto más alto entre la regla anterior y 2% o 4% de ingresos anuales según gravedad.',
 (41,'',12): 'Acelera a tres días hábiles y sin audiencia previa la decisión de la Agencia sobre reclamos y suspensión tras rechazo de bloqueo temporal.',
 (53,'',1): 'Permite a la Agencia revocar certificación por incumplir este párrafo y requerir información necesaria para supervisar la causa de revocación.',
})

ANALYSIS_OVERRIDES.update({
 (17,'',5): 'Exige a cesantes fuera del seguro acreditar esa condición ante el Boletín con finiquito o acta; el bloqueo dura tres meses y puede renovarse una vez con declaración jurada.',
 (19,'',2): 'Obliga al acreedor a informar pago o extinción al registro público dentro de siete días hábiles; permite al deudor pedir directamente la modificación si recibe constancia suficiente.',
 (21,'',2): 'Concreta coordinación y eficiencia pública en interoperabilidad, datos coherentes y menor duplicación de trámites o requerimientos al titular.',
 (22,'',1): 'Permite cesiones entre órganos públicos solo para funciones legales dentro de sus competencias y tratamiento específico; prohíbe al receptor cambiar de finalidad.',
 (30,'bis',16): 'Obliga al organismo requerido para funciones de la Agencia a colaborar conforme al inciso segundo del artículo 14 de la Ley 19.880.',
 (30,'quáter',2): 'Asigna al Presidente la propuesta de candidatos al Consejo y al Senado el pronunciamiento sobre ella.',
 (30,'sexies',1): 'Reserva la remoción de consejeros a la Corte Suprema por incapacidad, mal comportamiento o negligencia manifiesta, a solicitud de los actores y con el quórum que el inciso fija.',
 (31,'',2): 'Fija treinta días corridos para que el Consejo para la Transparencia informe desde que recibe la consulta de la Agencia.',
 (31,'',4): 'Establece consulta recíproca del Consejo a la Agencia ante normas que afecten su competencia, con informe en treinta días y motivación de la decisión.',
 (32,'',4): 'Obliga a la Agencia a defender jurídicamente a consejeros y personal demandados por actos del cargo, incluso tras cesar; la excepción del inciso siguiente limita el deber.',
 (32,'',6): 'Sujeta a la Agencia al régimen de administración financiera del Decreto Ley 1.263.',
 (37,'',11): 'Exige pagar multas en Tesorería dentro de diez días hábiles desde la firmeza y acreditar el pago ante la Agencia en otros diez días hábiles.',
 (38,'',3): 'Durante la suspensión, obliga al responsable a ajustar operaciones a las exigencias de la resolución para superar la medida.',
 (38,'',5): 'Antes de suspender a una entidad fiscalizada por otro organismo, obliga a la Agencia a informar a ese regulador para proteger derechos de usuarios.',
 (39,'',2): 'Exige registrar sancionados, gravedad, conducta, atenuantes, agravantes y sanción, además de responsables con modelos preventivos certificados vigentes.',
 (44,'',1): 'Impone al jefe superior del órgano velar por tratamientos conformes a principios, derechos y deberes del Título IV.',
 (47,'',1): 'Impone indemnizar daños patrimoniales y extrapatrimoniales causados por infracción de principios, derechos o deberes, sin excluir otros derechos del titular.',
 (49,'',10): 'Exige incorporar las reglas internas del programa a contratos de trabajo o servicio, o al reglamento interno, con publicidad según el Código del Trabajo.',
 (50,'',2): 'Exige nombramiento del delegado por la máxima autoridad directiva o administrativa e identifica quién ocupa esa posición según la entidad.',
 (50,'',3): 'Exige autonomía funcional del delegado; en empresas micro, pequeñas y medianas permite que dueño o máxima autoridad asuma el papel.',
 (50,'',6): 'Exige idoneidad, capacidad y conocimientos específicos en quien sea designado delegado.',
 (50,'',9): 'Obliga al responsable a dotar al delegado de facultades y recursos materiales suficientes, ajustados al tamaño y capacidad de la entidad.',
 (53,'',4): 'Tras revocación del certificado, exige probar que se subsanó la causal antes de pedir una nueva certificación.',
})

ANALYSIS_OVERRIDES.update({
 (8,'bis',6): 'Aun en las excepciones al derecho de oposición, obliga al responsable a asegurar explicación, intervención humana, expresión del punto de vista y revisión de decisiones automatizadas.',
 (9,'',4): 'Obliga al responsable a facilitar la portabilidad con medios rápidos y de bajo costo, sin obstáculos artificiales.',
 (9,'',5): 'Obliga a explicar al titular cómo obtener sus datos y las características técnicas necesarias para transferirlos.',
 (10,'',2): 'Exige a responsables jurídicos no constituidos en Chile registrar ante la Agencia un contacto electrónico operativo y representante capaz de recibir solicitudes y notificaciones.',
 (11,'',6): 'Impone acuse de recibo y respuesta dentro de treinta días corridos, con una sola prórroga de hasta treinta días bajo las condiciones del inciso.',
 (11,'',7): 'Exige respuesta escrita al canal designado y conservación de respaldo que pruebe el envío al titular.',
 (11,'',8): 'Ante denegación total o parcial, exige motivar causa y antecedentes e informar al titular su vía de reclamo ante la Agencia.',
 (11,'',11): 'Limita los efectos de rectificación, supresión u oposición al responsable requerido, pero obliga a éste a comunicar los cambios a terceros a quienes cedió datos.',
 (12,'',2): 'Exige consentimiento libre, informado, específico, previo e inequívoco manifestado por declaración o acto afirmativo claro.',
 (12,'',3): 'Exige mandato expreso para que un tercero otorgue válidamente el consentimiento por el titular.',
 (13,'',7): 'Asigna al responsable la carga de acreditar la base de licitud que invoca para tratar datos sin consentimiento.',
 (14,'',2): 'Obliga al responsable a mantener disponibles y entregar al titular antecedentes que acrediten la licitud del tratamiento.',
 (14,'',3): 'Obliga a recoger datos de fuentes lícitas para fines específicos, explícitos y lícitos y a limitar el tratamiento a esos fines.',
 (14,'',4): 'Obliga a comunicar o ceder únicamente información exacta, completa y actual, conforme a la ley.',
 (14,'',5): 'Obliga a suprimir o anonimizar los datos obtenidos para medidas precontractuales en el supuesto que establece la letra.',
 (14,'',6): 'Integra al catálogo general los demás principios, deberes y obligaciones de tratamiento previstos en la ley, sin duplicarlos aquí.',
 (14,'',7): 'Exige al responsable sin domicilio chileno que trata datos de residentes mantener un canal de contacto actualizado y operativo para titulares y Agencia.',
 (14,'bis',3): 'Obliga al responsable a implementar medidas para que dependientes y encargados bajo su responsabilidad cumplan la confidencialidad.',
 (14,'quáter',1): 'Exige integrar medidas técnicas y organizativas antes y durante el tratamiento, considerando tecnología, costos, contexto y riesgo para proteger principios y derechos desde el diseño.',
 (14,'quáter',2): 'Exige configurar por defecto el tratamiento solo de datos específicos y necesarios, atendiendo cantidad, extensión, retención y accesibilidad.',
 (14,'quinquies',1): 'Impone medidas de seguridad proporcionales a riesgos, técnica, costos y naturaleza del tratamiento para asegurar confidencialidad, integridad, disponibilidad y resiliencia.',
 (14,'sexies',1): 'Obliga al responsable a reportar a la Agencia sin demora vulneraciones que destruyan, filtren, pierdan o alteren datos, o permitan acceso no autorizado, si existe riesgo razonable para titulares.',
 (15,'',2): 'Exige recabar nuevo consentimiento antes de ceder si el consentimiento inicial no contempló cesión; la ley trata la cesión como nueva operación.',
 (15,'',3): 'Exige documentar la cesión por escrito o medio electrónico, identificando partes, datos, finalidades y estipulaciones.',
 (15,'',4): 'Obliga al cesionario a tratar los datos únicamente conforme a las finalidades fijadas en el contrato de cesión.',
 (15,'bis',4): 'Extiende al encargado confidencialidad y seguridad de los artículos 14 bis y 14 quinquies, aplica estándares diferenciados y le exige reportar vulneraciones al responsable.',
 (15,'ter',1): 'Obliga a evaluar impacto antes de iniciar tratamientos probablemente de alto riesgo por naturaleza, escala, contexto, tecnología o fines.',
 (16,'quinquies',2): 'Exige demostrar medidas de calidad y seguridad para mantener el uso solo en fines de interés público; en datos sensibles exige evaluar y mitigar riesgos, y permite conservación indefinida tras cumplirlo.',
 (16,'sexies',2): 'Exige informar claramente al titular tipo de geolocalización, finalidad, duración y eventuales cesiones a terceros para servicios de valor añadido.',
})

ANALYSIS_OVERRIDES.update({
 (30,'',2): 'Define la finalidad institucional de la Agencia: proteger los derechos sobre vida privada y datos personales y fiscalizar el cumplimiento de la ley.',
 (30,'quáter',1): 'Fija tres consejeros y un nombramiento presidencial sujeto al acuerdo de dos tercios del Senado en ejercicio.',
 (30,'quáter',3): 'Exige prestigio profesional o académico acreditado en protección de datos para acceder al cargo de consejero.',
 (30,'quáter',4): 'Entrega al Consejo la elección interna de presidente y vicepresidente y limita esos cargos a tres años o al tiempo restante como consejero.',
 (30,'quáter',5): 'Fija mandato de seis años, prohíbe un nuevo período y organiza renovación individual cada dos años.',
 (30,'quáter',6): 'Exige dedicación exclusiva al cargo de consejero.',
 (30,'quáter',7): 'Fija decisión por mayoría, voto dirimente presidencial o vicepresidencial, quórum de dos y remisión reglamentaria para funcionamiento restante.',
 (30,'quinquies',1): 'Declara incompatible el cargo de consejero con empleos o servicios privados, funciones políticas, empleos públicos y otros servicios estatales enumerados; delimita independencia institucional.',
 (30,'quinquies',2): 'Exceptúa docencia en instituciones reconocidas por el Estado hasta doce horas semanales de las incompatibilidades del cargo.',
 (30,'quinquies',3): 'Prohíbe a cónyuge, conviviente civil y parientes hasta segundo grado dirigir o tener propiedad en empresas dedicadas a datos personales.',
 (30,'quinquies',9): 'Aplica supletoriamente las normas de incompatibilidades de la Ley 18.575 cuando este artículo no regula un punto.',
 (30,'sexies',7): 'Ordena nombrar sustituto por el procedimiento del artículo 30 quáter para completar el período restante del consejero cesado.',
 (30,'sexies',8): 'Si el cesado era presidente o vicepresidente, ordena elegir reemplazo para el tiempo restante del cargo directivo conforme al artículo 30 quáter.',
 (30,'septies',1): 'Equipara la remuneración bruta mensual del presidente del Consejo a la de un subsecretario y vincula el cargo a funciones del artículo 30 nonies.',
 (30,'septies',2): 'Fija para cada otro consejero una remuneración del 85% de la correspondiente al presidente.',
 (30,'nonies',13): 'Sustituye al presidente por el vicepresidente en todas sus funciones y atribuciones cuando el primero se ausenta.',
 (31,'',3): 'Obliga a motivar la instrucción de la Agencia considerando el informe del Consejo; ante silencio en plazo remite al artículo 38 de la Ley 19.880.',
 (32,'',3): 'Selecciona directivos por concurso del Servicio Civil sobre terna del Consejo de Alta Dirección Pública, sujeto a la Ley 19.882.',
 (32,'',7): 'Sujeta a la Agencia a fiscalización de Contraloría sobre personal y cuentas.',
 (32,'',8): 'Exime las resoluciones de la Agencia del trámite de toma de razón ante Contraloría.',
 (35,'',3): 'Asigna a la infracción grave una multa máxima de 10.000 unidades tributarias mensuales.',
 (35,'',4): 'Asigna a la infracción gravísima una multa máxima de 20.000 unidades tributarias mensuales.',
 (38,'',1): 'Permite a la Agencia suspender hasta treinta días el tratamiento tras multas por infracciones gravísimas reiteradas en veinticuatro meses, preservando el almacenamiento.',
 (38,'',4): 'Permite prorrogar la suspensión por períodos sucesivos de hasta treinta días mientras el responsable incumpla la resolución que la ordenó.',
 (39,'',1): 'Crea un registro administrado por la Agencia, público, gratuito y electrónico, que da publicidad a sanciones y modelos certificados.',
 (41,'',1): 'Abre reclamación del titular ante la Agencia por denegación de una solicitud del artículo 11 o falta de respuesta del responsable en plazo.',
 (41,'',3): 'Exige reclamo escrito dentro de treinta días hábiles desde el rechazo o vencimiento del plazo de respuesta, con decisión impugnada, fundamentos y canal de notificación.',
 (44,'',2): 'Obliga al órgano público a cumplir medidas de corrección o prevención indicadas por la Agencia o programas de cumplimiento del artículo 49.',
 (44,'',3): 'Aplica a jefaturas multas de 20% a 50% de remuneración por infracciones del órgano; cuantía depende de gravedad, datos, titulares y atenuantes.',
 (44,'',7): 'Entrega a la Agencia la sanción configurada y permite a Contraloría, a petición de ella, instruir procedimientos y proponer sanciones conforme a su ley.',
 (44,'',8): 'Abre reclamo judicial de ilegalidad contra resoluciones de la Agencia mediante el artículo 43.',
 (44,'',9): 'Obliga a publicar las sanciones en los sitios de la Agencia y del órgano dentro de cinco días hábiles desde que quedan firmes.',
 (46,'',2): 'Transmite al órgano receptor y a sus funcionarios el mismo deber de secreto que protegía los datos cedidos por obligación legal.',
 (47,'',2): 'Condiciona la demanda de indemnización a resolución administrativa o judicial firme favorable y aplica procedimiento sumario civil.',
 (48,'',1): 'Impone a todo responsable público o privado acciones preventivas frente a las infracciones tipificadas en los artículos 34 bis, 34 ter y 34 quáter.',
 (50,'',4): 'Permite al delegado otras funciones solo si conserva independencia; el responsable debe prevenir conflictos de interés.',
 (50,'',5): 'Permite un delegado común a un grupo empresarial si comparte estándares y políticas y el delegado es accesible a todas las entidades.',
 (50,'',7): 'Permite a los titulares contactar al delegado sobre tratamiento de sus datos y ejercicio de derechos.',
 (54,'',2): 'Obliga a autoridades superiores de estos órganos a dictar políticas y estándares internos para derechos y seguridad, con posible asistencia de la Agencia, y a ejercer disciplina sobre funcionarios infractores.',
 (55,'',2): 'Permite reclamar ante Corte de Apelaciones según el artículo 43 contra denegaciones arbitrarias o infracciones con perjuicio de los cuatro órganos enumerados.',
 (55,'',3): 'Obliga a autoridades de órganos legislativos y jurisdiccionales a asegurar principios, deberes y derechos mediante medidas internas de fiscalización y control.',
})

ANALYSIS_OVERRIDES.update({
 (4,'',1): 'Reconoce a toda persona los seis derechos sobre sus datos —acceso, rectificación, supresión, oposición, portabilidad y bloqueo— ejercidos personalmente o mediante representante o mandatario según corresponda.',
 (8,'bis',1): 'Reconoce oposición a decisiones exclusivamente automatizadas, incluidos perfiles, cuando producen efectos jurídicos o afectan significativamente al titular.',
 (10,'',1): 'Sitúa el ejercicio de derechos ante el responsable; si varios responsables tratan los datos, permite acudir a cualquiera de ellos.',
 (14,'quinquies',7): 'En un litigio o controversia administrativa por incidente de seguridad, asigna al responsable probar existencia y funcionamiento de las medidas adoptadas según riesgo y tecnología disponible.',
 (14,'sexies',4): 'Aclara que los reportes de este artículo se acumulan con deberes informativos que impongan otras leyes; no los sustituyen.',
 (15,'ter',3): 'Hace obligatoria la evaluación previa de impacto para evaluación sistemática y exhaustiva de titulares basada en automatización o perfiles.',
 (15,'ter',4): 'Hace obligatoria la evaluación previa para tratamientos masivos o de gran escala.',
 (15,'ter',5): 'Hace obligatoria la evaluación previa cuando se observa o monitorea sistemáticamente una zona de acceso público.',
 (15,'ter',6): 'Hace obligatoria la evaluación previa para datos sensibles y especialmente protegidos tratados bajo excepciones al consentimiento.',
 (15,'ter',7): 'Obliga a la Agencia a publicar lista orientativa de operaciones con o sin evaluación de impacto y criterios mínimos para prepararla.',
 (15,'ter',8): 'Permite al responsable consultar a la Agencia si su evaluación revela alto riesgo, con el fin de obtener recomendaciones antes de tratar.',
 (23,'',5): 'Traslada al sector público el procedimiento del artículo 11 y dirige la solicitud al jefe superior del servicio.',
 (24,'',6): 'Permite tratar y compartir datos dentro de los regímenes especiales solo para funciones legales, dentro de competencias y con respeto a garantías constitucionales y principios del artículo 3°.',
 (24,'',7): 'Obliga a los órganos comprendidos en las letras a–c a intercambiar información necesaria para fines específicos autorizados por ley o, si no es posible, mediante requerimiento necesario y proporcional.',
 (24,'',8): 'Faculta a la Agencia, tras oír a los órganos competentes, a instruir cómo aplicar garantías y principios sin impedir el cumplimiento de funciones legales.',
 (25,'',2): 'Obliga a los órganos públicos a asegurar exactitud, suficiencia, actualidad e integridad de información de infracciones que comunican o publican.',
 (25,'',7): 'Prohíbe el tratamiento masivo de registros electrónicos de infracciones públicas y califica su incumplimiento como infracción gravísima.',
 (25,'',8): 'Permite comunicar información reservada si la piden tribunales u otros órganos públicos para funciones legales dentro de competencia, manteniendo deber de reserva.',
 (26,'',2): 'Excluye el reglamento de cesiones de este artículo cuando interviene alguno de los órganos del Título VIII.',
 (28,'',7): 'Obliga a la Agencia a publicar países adecuados y modelos de cláusulas e instrumentos para que los interesados conozcan las vías de transferencia.',
 (28,'',9): 'Faculta a la Agencia a autorizar un caso particular cuando no se cumplan las vías del artículo 27, siempre que transmisor y receptor otorguen garantías adecuadas.',
 (28,'',10): 'Coloca en el responsable transmisor la carga de acreditar ante la Agencia que la transferencia respetó las reglas de esta ley.',
})

ANALYSIS_OVERRIDES.update({
 (27,'',2): 'Habilita transferir a un receptor sujeto a un país con nivel adecuado de protección determinado conforme al artículo 28.',
 (27,'',3): 'Habilita transferir bajo cláusulas contractuales, normas corporativas u otros instrumentos entre transmisor y receptor que establezcan garantías adecuadas.',
 (27,'',4): 'Habilita la transferencia cuando transmisor y receptor adopten modelo de cumplimiento o certificación con garantías adecuadas.',
 (27,'',6): 'En la vía subsidiaria de transferencias singulares y no habituales, admite consentimiento expreso para una transferencia concreta.',
 (27,'',7): 'Admite transferencias bancarias, financieras o bursátiles específicas sujetas a sus leyes sectoriales como supuesto subsidiario.',
 (27,'',8): 'Admite transferencias necesarias para cumplir tratados o convenios ratificados y vigentes de Chile.',
 (27,'',9): 'Admite transferencias necesarias bajo convenios de cooperación, intercambio o supervisión de órganos públicos dentro de sus competencias.',
 (27,'',10): 'Admite transferencias expresamente autorizadas por ley y destinadas a una finalidad determinada.',
 (27,'',11): 'Admite transferencias dirigidas a prestar o solicitar colaboración judicial internacional.',
 (27,'',12): 'Admite transferencias necesarias para contratar o ejecutar un contrato con el titular, o medidas precontractuales pedidas por él.',
 (27,'',13): 'Admite transferencias urgentes por prevención, diagnóstico, atención o gestión sanitaria o médica.',
 (28,'',2): 'Exige considerar si el país receptor reconoce principios para el tratamiento como primer indicador de adecuación.',
 (28,'',3): 'Exige considerar derechos garantizados al titular y existencia de autoridad pública de control o tutela.',
 (28,'',4): 'Exige considerar obligaciones de información y seguridad impuestas a responsables y encargados en el país receptor.',
 (28,'',5): 'Exige considerar el régimen de responsabilidad por infracciones en el país receptor.',
 (30,'quinquies',5): 'Impide designar consejero a quien tenga condenas por los delitos y penas indicados, relacionados especialmente con función pública y fe pública.',
 (30,'quinquies',6): 'Impide designar a persona con dependencia de drogas ilegales, salvo justificación por tratamiento médico.',
 (30,'quinquies',7): 'Impide designar durante cinco años a quien haya recibido sanción grave o gravísima en protección de datos.',
 (30,'quinquies',8): 'Impide designar a quien en el último año tuvo funciones de dirección, delegación de datos o propiedad en empresas dedicadas al tratamiento de datos.',
 (30,'sexies',3): 'Hace cesar el cargo de consejero al expirar el plazo de designación.',
 (30,'sexies',4): 'Hace cesar el cargo por renuncia presentada al Presidente de la República.',
 (30,'sexies',5): 'Hace cesar el cargo al postularse a uno de elección popular.',
 (30,'sexies',6): 'Hace cesar el cargo por inhabilidad o incompatibilidad sobreviniente, calificada por consejeros sin participación del afectado.',
 (32,'bis',2): 'Incluye el aporte anual de la Ley de Presupuestos entre los recursos patrimoniales de la Agencia.',
 (32,'bis',3): 'Incorpora al patrimonio bienes muebles e inmuebles transferidos o adquiridos y los frutos que generen.',
 (32,'bis',4): 'Incorpora donaciones aceptadas por la Agencia y las exceptúa de insinuación judicial.',
 (32,'bis',5): 'Incorpora herencias y legados aceptados con beneficio de inventario y los exime de impuestos y gravámenes.',
 (32,'bis',6): 'Incorpora aportes de cooperación internacional al patrimonio de la Agencia.',
})

ANALYSIS_OVERRIDES.update({
 (11,'',2): 'Exige identificar y autenticar al titular y, cuando actúe por otra persona, al representante o mandatario para tramitar el ejercicio del derecho.',
 (11,'',3): 'Exige un domicilio o canal electrónico donde el responsable pueda comunicar su respuesta al solicitante.',
 (11,'',4): 'Exige individualizar los datos o el tratamiento concreto sobre los que recae la solicitud, para delimitar la búsqueda y la decisión.',
 (11,'',5): 'Distingue cargas según derecho: rectificación precisa cambios y antecedentes, supresión u oposición identifica causal, y oposición por interés legítimo añade fundamento breve; para acceso basta individualizar al titular.',
 (14,'quinquies',3): 'Incluye seudonimización y cifrado entre las medidas que pueden integrar la seguridad apropiada al riesgo; el inciso introductor impide tratarlas como únicas medidas obligatorias en todo caso.',
 (14,'quinquies',4): 'Incorpora capacidad permanente de confidencialidad, integridad, disponibilidad y resiliencia del sistema como dimensión de seguridad.',
 (14,'quinquies',5): 'Incluye recuperación rápida de acceso y disponibilidad tras incidentes físicos o técnicos, de acuerdo con el riesgo del tratamiento.',
 (14,'quinquies',6): 'Exige considerar un proceso regular de verificación y evaluación de la eficacia de las medidas técnicas y organizativas, no solo su instalación inicial.',
 (16,'',5): 'La entidad de la letra b debe perseguir una finalidad política, filosófica, religiosa, cultural, sindical o gremial; es el primer requisito acumulativo.',
 (16,'',6): 'Restringe la excepción al tratamiento de datos de miembros o afiliados de la entidad, excluyendo terceros ajenos a ella.',
 (16,'',7): 'Exige que el tratamiento sirva a las finalidades específicas de la institución, de modo que la mera pertenencia del titular no habilita otros fines.',
 (16,'',8): 'Exige garantías de la entidad contra filtración, sustracción, uso y tratamiento no autorizados de los datos.',
 (16,'',9): 'Prohíbe comunicar o ceder los datos a terceros dentro de la excepción de la letra b; completa las cinco condiciones acumulativas.',
 (16,'bis',3): 'Admite tratar datos de salud sin consentimiento ante necesidad indispensable de proteger vida o integridad, o impedimento del titular; terminado el impedimento, exige información detallada del tratamiento realizado.',
 (16,'bis',4): 'Habilita tratamiento de datos de salud sin consentimiento durante una alerta sanitaria legalmente decretada.',
 (16,'bis',5): 'Habilita investigación y desarrollo médico bajo los fines públicos o sanitarios descritos; los resultados pueden difundirse solo tras anonimizar los datos publicados.',
 (16,'bis',6): 'Permite tratar datos de salud sin consentimiento si es necesario para formular, ejercer o defender un derecho ante tribunal u órgano administrativo.',
 (16,'bis',7): 'Permite el tratamiento necesario para prevención, diagnóstico, asistencia, tratamiento o gestión de sistemas y servicios sanitarios o sociales.',
 (16,'bis',8): 'Exige una ley que permita el tratamiento sin consentimiento e indique expresamente su finalidad.',
 (23,'',3): 'Permite rechazar el ejercicio de derechos si con ello se impiden o entorpecen funciones fiscalizadoras, investigativas, de protección de víctimas o sancionatorias del órgano.',
 (23,'',4): 'Permite rechazar una solicitud que afecte información cuyo carácter secreto está establecido por ley.',
 (24,'',2): 'Sujeta al régimen especial los tratamientos para persecución penal, ejecución de sanciones y seguridad pública, incluidos protección de víctimas y análisis criminal; excluye la aplicación del artículo 25 a esta finalidad.',
 (24,'',3): 'Incluye en el régimen especial los tratamientos directamente relacionados con seguridad de la Nación, defensa nacional o política exterior.',
 (24,'',4): 'Cubre tratamientos cuyo objeto exclusivo sea atender emergencia o catástrofe legalmente declarada, solo mientras esa declaración esté vigente.',
 (24,'',5): 'Incluye datos protegidos por secreto, reserva o confidencialidad legal; el receptor de una cesión obligatoria hereda el mismo deber de resguardo.',
 (25,'',5): 'Somete el plazo de publicidad de infracciones penales a sus normas particulares, sin fijar aquí un período uniforme.',
 (25,'',6): 'Fija cinco años de acceso público a información de infracciones civiles, administrativas y disciplinarias cuando la norma de publicidad no señaló plazo.',
})

ANALYSIS_OVERRIDES.update({
 (33,'',1): 'Somete a sanción al responsable público o privado que infringe principios, derechos u obligaciones durante el tratamiento; el Título VII determina la consecuencia aplicable.',
 (34,'',1): 'Establece la clasificación tripartita de las infracciones del responsable en leves, graves y gravísimas, según su gravedad.',
 (34,'',2): 'Aclara que la responsabilidad prevista en esta ley puede coexistir con otras responsabilidades legales, civiles o penales.',
 (35,'',1): 'Introduce las escalas de sanciones que se asignan a cada clase de infracción en las letras siguientes.',
 (37,'',10): 'Aplica una sola multa basada en la infracción más grave cuando hay concurso por una misma conducta, pero acumula sanciones si las conductas son independientes.',
 (37,'',12): 'Impide sanciones duplicadas por los mismos hechos y fundamentos bajo esta ley y otras normas: se aplica la sanción de mayor gravedad.',
 (39,'',3): 'Limita la publicidad de cada anotación del registro a cinco años desde su inscripción.',
 (40,'',1): 'Fija cuatro años desde el hecho infraccional para ejercer la acción administrativa de persecución.',
 (40,'',2): 'Para infracciones continuadas, desplaza el inicio del plazo de acción al día en que cesa la infracción.',
 (40,'',3): 'Interrumpe la prescripción de la acción con la notificación de inicio del procedimiento administrativo.',
 (40,'',4): 'Fija tres años desde que queda ejecutoriada la resolución para la prescripción de la sanción impuesta.',
 (41,'',2): 'Introduce las reglas especiales que ordenan admisión, prueba, decisión e impugnación del reclamo del titular ante la Agencia.',
 (42,'',1): 'Somete la determinación de infracciones y sanciones por incumplir principios, derechos u obligaciones al procedimiento especial enumerado en este artículo.',
 (44,'',4): 'Agrava la responsabilidad de la jefatura si el órgano persiste en la infracción: duplica la sanción inicial y agrega suspensión de cinco días.',
 (44,'',5): 'Establece multa del cincuenta por ciento de la remuneración y suspensión de hasta treinta días cuando la infracción se refiere a datos sensibles.',
 (44,'',6): 'Entrega a la Agencia la determinación de infracciones de órganos públicos mediante el procedimiento del artículo 42.',
 (45,'',1): 'Activa investigación sumaria de Contraloría, a petición de la Agencia, si se detecta responsabilidad individual de funcionarios; las sanciones se rigen por el Estatuto Administrativo.',
 (45,'',2): 'Califica como contravención grave a la probidad la responsabilidad de un funcionario por infracción gravísima del artículo 34 quáter.',
 (47,'',3): 'Fija cinco años para las acciones civiles desde que queda ejecutoriada la resolución o sentencia que impone la multa.',
 (51,'',1): 'Asigna a la Agencia certificar y supervisar modelos preventivos frente a los requisitos de la ley y el reglamento.',
 (51,'',2): 'Obliga a inscribir en el Registro Nacional de Sanciones y Cumplimiento a las entidades con certificación vigente.',
 (51,'',3): 'Remite a reglamento los requisitos y procedimientos de implementación, certificación, registro y supervisión de modelos preventivos.',
 (52,'',1): 'Fija tres años de vigencia para los certificados de la Agencia y anuncia las causales legales que pueden terminarla anticipadamente.',
 (52,'',7): 'Mantiene oponible a terceros la certificación mientras no se elimine del registro, pese a una causal de término.',
 (53,'',2): 'Permite retener información requerida para supervisión si está amparada por secreto o confidencialidad, con carga de acreditar esa protección.',
 (53,'',3): 'Somete a sanción no entregar la información requerida para supervisión o entregarla falsa, incompleta o manifiestamente errónea.',
 (55,'',1): 'Reconoce el ejercicio de derechos ante los órganos constitucionales y autónomos enumerados mediante procedimientos racionales y justos definidos por ellos.',
})

ANALYSIS_OVERRIDES.update({
 (17,'',1): 'Limita la comunicación por registros comerciales a obligaciones documentadas en los instrumentos y operaciones enumerados. Excluye créditos INDAP y obligaciones repactadas, renegociadas, novadas o sujetas a modalidad pendiente.',
 (17,'',3): 'Prohíbe publicar o comunicar protestos y morosidades originados durante la cesantía del deudor; activa el régimen de bloqueo desarrollado en los incisos siguientes.',
 (17,'',4): 'Ordena a la Administradora de Fondos de Cesantía comunicar beneficiarios al Boletín solo mientras subsista el beneficio, para bloquear su información comercial.',
 (17,'',6): 'Hace gratuito para el deudor el bloqueo de los datos comerciales durante la cesantía.',
 (17,'',8): 'Obliga a los responsables a suprimir de oficio información de obligaciones prescritas, sin exigir solicitud, orden judicial ni instrucción de la autoridad.',
 (17,'',9): 'Prohíbe marcar o caracterizar a una persona como beneficiada por el bloqueo de esta ley en las bases comerciales.',
 (18,'',1): 'Impide comunicar datos comerciales de una persona identificada o identificable después de cinco años desde la exigibilidad de la obligación.',
 (18,'',2): 'Termina la posibilidad de comunicar los datos cuando la obligación se paga o extingue por otro modo, aun si no han transcurrido los cinco años.',
 (18,'',3): 'Mantiene un cauce de comunicación de información requerida por tribunales para juicios pendientes como excepción a los límites anteriores.',
 (19,'',1): 'Aclara que el pago o extinción no hace caducar inmediatamente los datos para el artículo 4°, aunque el artículo 18 impide continuar comunicándolos; distingue conservación y comunicación.',
 (19,'',3): 'Obliga a quienes reutilizan datos de la fuente pública a actualizar la información de pago o extinción prontamente o dentro de tres días; si no pueden, deben bloquear los datos hasta la actualización.',
 (19,'',4): 'Remite el conocimiento y sanción de infracciones a las obligaciones del artículo al Título VII.',
 (21,'',1): 'Somete el tratamiento de los órganos públicos a los principios del artículo 3° y a coordinación, probidad y eficiencia de la Administración del Estado.',
 (22,'',2): 'Permite compartir datos entre organismos solo para otorgar beneficios al titular o reducir trámites y requerimientos repetidos; la finalidad exclusiva limita la cesión.',
 (22,'',3): 'Limita la conservación del receptor público al tratamiento específico; permite mayor duración para reclamaciones, control, seguimiento o respaldo de decisiones.',
 (22,'',5): 'Exige consentimiento obtenido en la oportunidad del artículo 20 de la Ley 20.285 para ceder datos mediante una solicitud de acceso a información pública.',
 (22,'',6): 'Somete la comunicación de datos de infracciones penales, civiles, administrativas y disciplinarias al régimen del artículo 25.',
 (22,'',7): 'Obliga a publicar mensualmente en la web institucional los convenios de cesión o transferencia con entidades públicas o privadas; la Agencia fiscaliza esta publicidad.',
 (23,'',1): 'Reconoce ante órganos públicos acceso, rectificación y oposición, más supresión en el supuesto del artículo 22 inciso tercero; la oposición también cubre tratamientos contrarios a este título.',
 (24,'',1): 'Delimita un régimen exclusivo para tratamientos de datos sensibles por órganos públicos en cuatro materias enumeradas; las letras precisan su alcance.',
 (25,'',1): 'Restringe el tratamiento de datos de infracciones a organismos públicos que cumplen funciones legales dentro de sus competencias y en casos expresamente autorizados.',
 (26,'',1): 'Remite a reglamento las condiciones e instrumentos de comunicación y cesión de datos por órganos públicos, incluidos procedimientos de anonimización; exige informe previo de la Agencia.',
 (27,'',1): 'Habilita transferencias internacionales solo si el tratamiento de base es lícito y concurre adecuación del país, garantías contractuales o un modelo certificado, según las letras siguientes.',
 (27,'',5): 'Abre una vía subsidiaria para transferencias específicas y no habituales cuando faltan adecuación o garantías, condicionada a uno de los supuestos de las letras que siguen.',
 (28,'',1): 'Define país adecuado por estándares de protección similares o superiores a esta ley y asigna a la Agencia su determinación fundada conforme a criterios mínimos.',
 (28,'',6): 'Define garantías adecuadas por derechos exigibles y acciones legales efectivas comparables a esta ley; faculta a la Agencia aprobar instrumentos modelo y dispensa autorización adicional a los aprobados.',
 (28,'',8): 'Permite transferencias intragrupo bajo normas corporativas vinculantes aprobadas por la Agencia; impone responsabilidad al transmisor por infracciones del grupo salvo prueba de no imputabilidad.',
 (29,'',1): 'Atribuye a la Agencia fiscalizar transferencias internacionales y adoptar recomendaciones, medidas conservativas o suspensión temporal en casos calificados.',
 (30,'',1): 'Crea la Agencia como corporación autónoma de derecho público, técnica y descentralizada, con personalidad y patrimonio propios, relacionada con el Ejecutivo por Economía.',
 (30,'ter',1): 'Asigna la dirección superior de la Agencia al Consejo Directivo y vincula a éste las atribuciones enumeradas en las letras siguientes.',
 (30,'octies',1): 'Entrega a estatutos la organización de la Agencia y fija un procedimiento de propuesta por la Agencia y aprobación mediante decreto supremo del ministerio indicado.',
 (30,'nonies',1): 'Designa al presidente del Consejo como jefe de servicio y representante judicial y extrajudicial de la Agencia; le asigna organización, administración y control jerárquico del personal.',
 (31,'',1): 'Exige a la Agencia consultar al Consejo para la Transparencia antes de dictar normas generales que afecten su competencia, para prevenir conflictos y coordinar regulaciones.',
 (32,'',1): 'Sujeta al personal de la Agencia al Código del Trabajo; los incisos siguientes añaden reglas de probidad, selección y control público.',
 (32,'bis',1): 'Introduce las fuentes que forman el patrimonio de la Agencia; cada letra identifica un origen admisible de recursos.',
})

# Functional categories. The numbered article's full text and its lists determine
# the narrower classification of each file below.
TOPICS = {
 (1,'bis'):('criterio de aplicación territorial','alcance territorial de la ley'),
 (2,''):('definición legal','vocabulario de la ley'),
 (3,''):('principio rector','estándares generales del tratamiento'),
 (4,''):('titularidad y ejercicio de derechos','derechos del titular y sus herederos'),
 (5,''):('derecho de acceso','contenido de la respuesta al acceso'),
 (6,''):('derecho de rectificación','corrección y comunicación de datos'),
 (7,''):('derecho de supresión','causales y límites de la eliminación'),
 (8,''):('derecho de oposición','causales y límites de la oposición'),
 (8,'bis'):('garantía frente a decisiones automatizadas','decisiones y perfiles automatizados'),
 (8,'ter'):('derecho de bloqueo','suspensión temporal del tratamiento'),
 (9,''):('derecho de portabilidad','entrega y transmisión de datos'),
 (10,''):('regla de ejercicio de derechos','canales y costos del ejercicio'),
 (11,''):('regla procedimental','solicitud y respuesta del responsable'),
 (12,''):('regla de consentimiento','licitud y requisitos del consentimiento'),
 (13,''):('base de licitud sin consentimiento','supuestos legales de tratamiento'),
 (14,''):('obligación del responsable','deberes generales del responsable'),
 (14,'bis'):('deber de confidencialidad','reserva de los datos y sus límites'),
 (14,'ter'):('deber de información y transparencia','información pública del responsable'),
 (14,'quáter'):('deber de protección desde el diseño y por defecto','medidas previas y configuración del tratamiento'),
 (14,'quinquies'):('deber de seguridad','medidas proporcionadas al riesgo'),
 (14,'sexies'):('deber de reporte','vulneraciones de seguridad'),
 (14,'septies'):('criterio para estándares diferenciados','exigencias mínimas según responsable y datos'),
 (15,''):('regla de cesión','licitud, formalización y efectos de la cesión'),
 (15,'bis'):('regla del encargo de tratamiento','instrucciones, contrato y responsabilidad del encargado'),
 (15,'ter'):('evaluación de impacto','riesgo previo al tratamiento'),
 (16,''):('régimen de datos sensibles','licitud y límites para datos sensibles'),
 (16,'bis'):('régimen de datos de salud','datos de salud y perfil biológico'),
 (16,'ter'):('régimen biométrico','datos biométricos'),
 (16,'quáter'):('protección de niños, niñas y adolescentes','datos de menores de edad'),
 (16,'quinquies'):('régimen de fines históricos, estadísticos y científicos','tratamientos de investigación'),
 (16,'sexies'):('régimen de geolocalización','datos de ubicación'),
 (17,''):('régimen de información comercial','obligaciones económicas, financieras, bancarias o comerciales'),
 (18,''):('límite al tratamiento de información comercial','tratamiento de obligaciones económicas'),
 (19,''):('efecto de la extinción de una obligación','datos de obligaciones extinguidas'),
 (20,''):('base de licitud pública','tratamiento por órganos públicos'),
 (21,''):('principios aplicables al sector público','tratamiento público de datos'),
 (22,''):('comunicación o cesión pública','transferencia de datos entre órganos o a terceros'),
 (23,''):('ejercicio de derechos ante órganos públicos','procedimiento y reclamación'),
 (24,''):('régimen especial','tratamientos sujetos a leyes especiales'),
 (25,''):('régimen de datos de infracciones','antecedentes penales, civiles y administrativos'),
 (26,''):('remisión reglamentaria','comunicación y cesión por órganos públicos'),
 (27,''):('habilitación de transferencia internacional','transferencias al extranjero'),
 (28,''):('criterio de adecuación y garantías','evaluación de protección en otro país'),
 (29,''):('facultad de fiscalización','transferencias internacionales'),
 (30,''):('creación y régimen institucional','Agencia de Protección de Datos Personales'),
 (30,'bis'):('atribución de la Agencia','competencias de la autoridad de control'),
 (30,'ter'):('regla de dirección institucional','Consejo Directivo de la Agencia'),
 (30,'quáter'):('regla de integración y nombramiento','miembros del Consejo Directivo'),
 (30,'quinquies'):('inhabilidad o incompatibilidad','aptitud y conducta de consejeros'),
 (30,'sexies'):('causal o procedimiento de remoción','término del cargo de consejero'),
 (30,'septies'):('regla de remuneración','Consejo Directivo'),
 (30,'octies'):('remisión a estatutos','organización de la Agencia'),
 (30,'nonies'):('atribución de la presidencia','dirección ejecutiva de la Agencia'),
 (31,''):('regla de coordinación','Agencia y Consejo para la Transparencia'),
 (32,''):('régimen de personal y fiscalización','funcionarios de la Agencia'),
 (32,'bis'):('fuente de patrimonio','financiamiento de la Agencia'),
 (33,''):('regla de responsabilidad','infracciones del responsable'),
 (34,''):('clasificación de infracciones','gravedad y concurrencia de responsabilidades'),
 (34,'bis'):('tipificación de infracción leve','conductas leves'),
 (34,'ter'):('tipificación de infracción grave','conductas graves'),
 (34,'quáter'):('tipificación de infracción gravísima','conductas gravísimas'),
 (35,''):('sanción administrativa','escalas y efectos de multas'),
 (36,''):('circunstancia de responsabilidad','atenuantes y agravantes'),
 (37,''):('criterio de determinación de multa','cuantía y reglas de multas'),
 (38,''):('sanción accesoria','suspensión temporal del tratamiento'),
 (39,''):('registro público de sanciones','inscripción y publicidad'),
 (40,''):('prescripción','plazos de persecución y sanción'),
 (41,''):('procedimiento administrativo de tutela','reclamo del titular ante la Agencia'),
 (42,''):('procedimiento sancionatorio','infracciones investigadas por la Agencia'),
 (43,''):('reclamación judicial','control por Corte de Apelaciones'),
 (44,''):('responsabilidad de jefatura pública','infracciones de órganos públicos'),
 (45,''):('responsabilidad de funcionario','infracción individual'),
 (46,''):('deber de reserva de funcionario','datos conocidos por órganos públicos'),
 (47,''):('responsabilidad civil','indemnización por infracciones'),
 (48,''):('prevención de infracciones','modelo preventivo del responsable'),
 (49,''):('elemento de modelo preventivo','programa de cumplimiento'),
 (50,''):('atribución o requisito del delegado','delegado de protección de datos'),
 (51,''):('certificación de modelo','registro y supervisión del cumplimiento'),
 (52,''):('vigencia de certificado','duración y término de certificación'),
 (53,''):('revocación de certificación','causales y nueva solicitud'),
 (54,''):('régimen de órganos constitucionales','tratamiento por instituciones autónomas'),
 (55,''):('ejercicio de derechos ante órganos constitucionales','derechos y reclamaciones'),
}

def first_clause(text):
    core=ART_RE.sub('',text)
    core=ENUM_RE.sub('',core)
    # Remove an epigraph ending in a period only on the article's first block.
    if text.startswith('Artículo ') and '. ' in core:
        core=core.split('. ',1)[1]
    sentence=re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])',core,1)[0]
    return sentence

def evidence(text, max_chars=190):
    s=first_clause(text).strip()
    if len(s)>max_chars:
        s=s[:max_chars].rsplit(' ',1)[0]+'…'
    return s

def classification(a,b):
    n,suf=a['num'],a['suffix']
    text=b['text']; low=text.lower()
    is_list=b['depth']>=2
    if n==50 and not suf and b['name']=='inciso-08':
        return 'deber de secreto, consecuencia sancionatoria y asignación de responsabilidad'
    if a['transitory']:
        return ('regla transitoria de vigencia' if n==1 else 'reconocimiento transitorio de derechos' if n==2 else 'regla transitoria de continuidad normativa')
    if n==2:
        return 'criterio complementario de identificación' if 'parrafo-' in b['name'] else 'contexto de definiciones' if not is_list else 'definición legal'
    if n==3:
        return 'deber derivado del principio' if b['depth']==3 else 'contexto de principios' if not is_list else 'principio rector'
    if n==7:
        if 'ordinal-' in b['name']: return 'excepción a la supresión'
        if is_list: return 'causal de supresión'
    if n==8 and suf=='bis' and is_list: return 'excepción al derecho frente a decisiones automatizadas'
    if n==8 and not suf and is_list: return 'supuesto de oposición'
    if n==5 and is_list: return 'contenido del derecho de acceso'
    if n==11 and is_list: return 'requisito de la solicitud del titular'
    if n==14 and not suf and is_list: return 'obligación específica del responsable'
    if n==14 and suf=='ter' and is_list: return 'información mínima de transparencia'
    if n==14 and suf=='quinquies' and is_list: return 'medida de seguridad considerada por la ley'
    if n==9 and is_list: return 'condición acumulativa de portabilidad'
    if n==13 and is_list: return 'base de licitud sin consentimiento'
    if n==16 and suf=='bis' and is_list: return 'excepción para datos de salud sin consentimiento'
    if n==16 and suf=='ter' and is_list: return 'información específica para tratamiento biométrico'
    if n==16 and 'ordinal-' in b['name']: return 'condición acumulativa de la excepción de la letra b'
    if n==16 and is_list: return 'supuesto especial de tratamiento de datos sensibles'
    if n==23 and is_list: return 'causal de rechazo de derecho ante órgano público'
    if n==24 and is_list: return 'materia sometida a régimen especial'
    if n==25 and is_list: return 'plazo de publicidad de sanciones'
    if n==27 and is_list: return 'supuesto subsidiario de transferencia singular' if 'inciso-02-' in b['name'] else 'supuesto general de transferencia internacional'
    if n==28 and is_list: return 'criterio de evaluación de adecuación'
    if n==30 and suf=='bis' and is_list: return 'atribución de la Agencia'
    if n==30 and suf=='ter' and is_list: return 'atribución del Consejo Directivo'
    if n==30 and suf=='nonies' and is_list: return 'atribución de la presidencia de la Agencia'
    if n==30 and suf=='quinquies' and is_list: return 'causal de inhabilidad para ser consejero'
    if n==30 and suf=='sexies' and is_list: return 'causal de cesación del consejero'
    if n==32 and suf=='bis' and is_list: return 'fuente patrimonial de la Agencia'
    if n==34 and suf in ('bis','ter','quáter') and is_list: return TOPICS[(n,suf)][0]
    if n==35 and is_list: return 'escala de sanción según gravedad'
    if n==36 and is_list: return 'circunstancia atenuante' if 'numeral-' in b['name'] else 'circunstancia agravante'
    if n==37 and is_list: return 'factor para determinar multa'
    if n in (41,42,43) and is_list: return 'etapa o regla del procedimiento'
    if n==49 and is_list: return 'contenido mínimo del programa preventivo'
    if n==50 and is_list: return 'función del delegado de protección de datos'
    if n==52 and is_list: return 'causal de término del certificado'
    if text.rstrip().endswith(':') or text.rstrip().endswith('siguientes:'):
        return 'contexto introductor de enumeración'
    if re.search(r'\bno (?:podrá|puede|procederá|se podrá|se aplicará|deberá)\b',low):
        return 'prohibición o límite expreso'
    if re.search(r'\b(?:salvo|excepto|sin perjuicio|no se aplicará|no procederá)\b',low):
        return 'regla con excepción o límite'
    if re.search(r'\b(?:deberá|debe|está obligado|será obligatorio|tendrá que)\b',low):
        return 'deber específico' if n not in (41,42,43) else 'regla procedimental obligatoria'
    if re.search(r'\b(?:tiene derecho|tendrá derecho|podrá reclamar)\b',low):
        return 'derecho o facultad del titular'
    if re.search(r'\b(?:podrá|puede)\b',low):
        return 'facultad legal condicionada por el texto'
    return TOPICS.get((n,suf),('regla de alcance','tratamiento de datos'))[0]

def role_analysis(a,b,cl,topic,index):
    if a['transitory']:
        return {
            1:'Fija la entrada en vigencia de la Ley 19.628 a sesenta días desde su publicación de 1999, con excepción del artículo 22. Es una disposición transitoria propia del texto consolidado y no determina por sí sola la vigencia de la reforma de 2026.',
            2:'Reconoce a titulares ya inscritos en bancos de datos anteriores a la vigencia de esta ley los derechos que ella confiere. Evita que la antigüedad del registro excluya esos derechos.',
            3:'Mantiene aplicables las normas del Boletín de Informaciones Comerciales del Decreto Supremo de Hacienda 950 de 1928 solo en lo que no contradigan esta ley.',
        }[a['num']]
    override=ANALYSIS_OVERRIDES.get((a['num'],a['suffix'],index))
    if override: return override
    lead=evidence(b['text'])
    label=b['label']
    if cl=='contexto introductor de enumeración' or cl.startswith('contexto de'):
        return f'Este {label} fija el marco que da sentido a las unidades enumeradas del artículo: «{lead}». Su texto se conserva como contexto operativo; la enumeración posterior concreta sus supuestos y no debe leerse aislada.'
    if cl=='definición legal':
        m=re.match(r'^[a-zñ]\)\s+([^,:.]+)',b['text'])
        term=m.group(1) if m else 'el término indicado'
        return f'Delimita el significado legal de «{term}» para aplicar el resto de la ley. La delimitación depende de los elementos expresos del literal: «{lead}».'
    if cl=='principio rector':
        return f'Enuncia un estándar rector del tratamiento que deberá orientar las reglas operativas posteriores. Su contenido propio es «{lead}»; las oraciones adicionales del mismo literal precisan cómo se cumple.'
    if cl=='deber derivado del principio':
        return f'Concreta el principio de la letra anterior mediante un deber o límite adicional: «{lead}». Su ubicación dentro de la misma letra impide tratarlo como un principio distinto.'
    if cl.startswith('tipificación de infracción'):
        return f'Tipifica como {cl.split("de ")[-1]} la conducta descrita en esta letra: «{lead}». La calificación proviene del encabezado del artículo y es necesaria para interpretar el literal.'
    if cl in ('causal de supresión','excepción a la supresión','supuesto de oposición','excepción al derecho frente a decisiones automatizadas','base de licitud sin consentimiento','supuesto de transferencia internacional','supuesto especial de tratamiento de datos sensibles'):
        return f'Concreta {cl} mediante el supuesto «{lead}». Opera dentro del marco del inciso que introduce la enumeración; las condiciones de esa introducción se suman a las de esta unidad.'
    if cl in ('etapa o regla del procedimiento','regla procedimental obligatoria'):
        return f'Ordena una fase o efecto concreto de {topic}: «{lead}». El sujeto que debe actuar, el plazo y el resultado se toman del literal, sin trasladar reglas de otras etapas.'
    if cl in ('contenido mínimo del programa preventivo','función del delegado de protección de datos','factor para determinar multa','circunstancia atenuante','circunstancia agravante','escala de sanción según gravedad','causal de término del certificado'):
        return f'Integra la enumeración de {topic} con el elemento «{lead}». La función indicada por la categoría depende del encabezado o inciso introductor, que determina su efecto jurídico.'
    if cl in ('deber específico','obligación específica del responsable'):
        return f'Impone una conducta identificable en materia de {topic}: «{lead}». La obligación recae en el sujeto señalado expresamente en el literal y no se extiende por inferencia a otros actores.'
    if cl=='prohibición o límite expreso':
        return f'Fija una restricción en materia de {topic}: «{lead}». Su alcance se limita al supuesto y destinatario formulados en el literal.'
    if cl=='regla con excepción o límite':
        return f'Establece una regla de {topic} que se modula por una excepción o límite expreso: «{lead}». La excepción se conserva en el mismo literal para evitar una lectura absoluta.'
    if cl in ('atribución de la Agencia','atribución del Consejo Directivo','atribución de la presidencia de la Agencia'):
        actor={'atribución de la Agencia':'Agencia','atribución del Consejo Directivo':'Consejo Directivo','atribución de la presidencia de la Agencia':'presidencia de la Agencia'}[cl]
        return f'Atribuye al {actor} la actuación identificada en la letra: «{lead}». La competencia se ejerce bajo los límites y procedimientos que el propio literal o los artículos conexos expresan.'
    if cl in ('información mínima de transparencia','contenido del derecho de acceso','información específica para tratamiento biométrico'):
        return f'Identifica un contenido concreto que debe informarse en el régimen de {topic}: «{lead}». Su exigibilidad procede del inciso introductor y el literal delimita la materia que debe cubrir la información.'
    if cl in ('requisito de la solicitud del titular','medida de seguridad considerada por la ley','condición acumulativa de la excepción de la letra b','causal de rechazo de derecho ante órgano público','materia sometida a régimen especial','plazo de publicidad de sanciones','causal de inhabilidad para ser consejero','causal de cesación del consejero','fuente patrimonial de la Agencia','criterio de evaluación de adecuación','supuesto general de transferencia internacional','supuesto subsidiario de transferencia singular','excepción para datos de salud sin consentimiento'):
        return f'Concreta {cl} mediante el elemento «{lead}». El efecto se obtiene al leer esta unidad con el inciso introductor y, cuando corresponde, con las otras condiciones de la misma serie.'
    return f'Esta unidad cumple la función de {cl} respecto de {topic}. Su efecto concreto se apoya en el enunciado «{lead}» y en las condiciones que el propio literal expresa.'

def conditions(text):
    pieces=[]
    for m in COND_RE.finditer(text):
        s=m.group(0).strip()
        if len(s)>230: s=s[:230].rsplit(' ',1)[0]+'…'
        if s not in pieces: pieces.append(s)
    return pieces[:8]

def references(text):
    vals=[]
    text=ART_RE.sub('',text)
    for m in REF_RE.finditer(text):
        if m.group(0) not in vals: vals.append(m.group(0))
    for m in GENERIC_REF_RE.finditer(text):
        tag='remisión genérica: '+m.group(0)
        if tag not in vals: vals.append(tag)
    return vals

arts=json.loads((Path(__file__).parent/'inventory.json').read_text(encoding='utf-8'))
source='Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
created=0
for a in arts:
    if a['num']==1 and not a['suffix'] and not a['transitory']:
        continue
    folder=DEST/art_slug(a)
    folder.mkdir(parents=True,exist_ok=True)
    if a['transitory']:
        class_base,topic={
            1:('regla transitoria de vigencia','entrada en vigor original de la Ley 19.628'),
            2:('reconocimiento transitorio de derechos','titulares inscritos en bancos de datos anteriores'),
            3:('regla transitoria de continuidad normativa','normas del Boletín de Informaciones Comerciales'),
        }[a['num']]
    else:
        class_base,topic=TOPICS[(a['num'],a['suffix'])]
    first=a['blocks'][0]['text']
    core=ART_RE.sub('',first)
    heading=core.split('. ',1)[0] if not a['transitory'] and '. ' in core else 'Sin epígrafe'
    block_lines=[]
    for j,b in enumerate(a['blocks']):
        bfile=folder/(b['name']+'.md')
        cl=classification(a,b)
        page_text=', '.join(str(p) for p in b['pages'])
        prev=a['blocks'][j-1]['name']+'.md' if j else 'articulo.md'
        nxt=a['blocks'][j+1]['name']+'.md' if j<len(a['blocks'])-1 else 'articulo.md'
        parent_context=''
        if b['depth']==3:
            base=b['name'].rsplit('-parrafo-',1)[0]
            parent=next((x for x in a['blocks'] if x['name']==base),None)
            if parent: parent_context=f"Este párrafo prolonga [{parent['label']}]({base}.md) y se lee con sus condiciones."
        elif b['depth']==2:
            prefix=b['name'].split('-letra-')[0].split('-numeral-')[0].split('-ordinal-')[0]
            parent=next((x for x in a['blocks'] if x['name']==prefix),None)
            if parent:
                parent_context=f"La unidad depende de [{parent['label']}]({parent['name']}.md), cuyo enunciado introductor es «{evidence(parent['text'],240)}»."
        cond=conditions(b['text'])
        if a['transitory'] and a['num']==3:
            cond=['en todo lo que no sean contrarias a las disposiciones de esta ley']
        refs=references(b['text'])
        condi='; '.join('«'+x+'»' for x in cond) if cond else 'No contiene fórmula condicional o exceptiva expresa en esta unidad.'
        rem='; '.join(refs) if refs else 'No hay remisión expresa en esta unidad.'
        if a['num']==50 and not a['suffix'] and b['name']=='inciso-08':
            condi='La sanción penal presupone que un funcionario público desempeñe estas funciones e infrinja el deber. La frase «sin perjuicio de las acciones de repetición que pueda ejercer contra éste» preserva esa acción frente al encargado o delegado; no limita la confidencialidad ni elimina la responsabilidad inicial del responsable.'
            rem='artículos 246 a 247 bis del Código Penal.'
        txt=f'''# {art_label(a)} — {b['label']}

- **Fuente y versión:** Ley 19.628 consolidada BCN, vigencia diferida desde 01-DIC-2026; última modificación indicada en el PDF: Ley 21.719 de 13-DIC-2024.
- **Localizador:** {art_label(a)}, {b['label']}; [artículo](articulo.md), [unidad anterior]({prev}), [unidad siguiente]({nxt}).
- **Original:** `{source}`, página{'s' if len(b['pages'])>1 else ''} {page_text} del PDF.

## Texto literal

> {b['text']}

Se normalizaron solo espacios y saltos de línea de maquetación; se conservaron las palabras y la puntuación extraídas del original.

## Análisis normativo

**Función propuesta:** {cl}. {role_analysis(a,b,cl,topic,j+1)}

**Contexto y alcance:** {parent_context if parent_context else f'Esta unidad pertenece a {section(a)} y se interpreta dentro del artículo completo sobre {topic}.'}

**Condiciones o excepciones expresas:** {condi}

**Remisiones expresas:** {rem}

## Comprobación de fragmentación

La unidad se localizó en la{'s' if len(b['pages'])>1 else ''} página{'s' if len(b['pages'])>1 else ''} {page_text}; se revisó su comienzo y final frente a las unidades vecinas del mismo artículo. Su literal se incluyó en la reconstrucción ordenada del artículo. No se extrae una Exigencia ni se afirma auditoría independiente.
'''
        bfile.write_text(txt,encoding='utf-8')
        block_lines.append(f"{j+1}. [{b['label']}]({b['name']}.md) — {cl}; página{'s' if len(b['pages'])>1 else ''} {page_text}.")
        created+=1
    pages=sorted({p for b in a['blocks'] for p in b['pages']})
    page_span=f"{pages[0]}" if len(pages)==1 else f"{pages[0]}–{pages[-1]}"
    structure_note=('Una sola unidad conserva íntegro el artículo.' if len(a['blocks'])==1 else 'Las introducciones de enumeraciones determinan la interpretación de sus letras o numerales; las excepciones y remisiones se documentan en las unidades correspondientes.')
    article_txt=f'''# {art_label(a)} — {heading}

- **Fuente y versión:** Ley 19.628 consolidada BCN, vigencia diferida desde 01-DIC-2026; última modificación indicada en el PDF: Ley 21.719 de 13-DIC-2024.
- **Original:** `{source}`, página{'s' if len(pages)>1 else ''} {page_span} del PDF.
- **Ubicación sistemática:** {section(a)}.

## Función y estructura

{role_analysis(a,a['blocks'][0],classification(a,a['blocks'][0]),topic,1) if a['transitory'] else ANALYSIS_OVERRIDES.get((a['num'],a['suffix'],1),f'El artículo trata {topic} y cumple una función de {class_base}.')} {structure_note}{' Estos son artículos transitorios de la Ley 19.628 consolidada; no son los artículos transitorios de la Ley 21.719 modificatoria.' if a['transitory'] else ''}

## Unidades en orden del original

{chr(10).join(block_lines)}

## Control de cobertura

Se localizaron {len(a['blocks'])} bloque{'s' if len(a['blocks'])>1 else ''} textual{'es' if len(a['blocks'])>1 else ''} en orden, de la{'s' if len(pages)>1 else ''} página{'s' if len(pages)>1 else ''} {page_span}. La reconstrucción literal, los archivos y las referencias del árbol se comprueban en el informe global de fragmentación. No hay texto de otro artículo en esta carpeta.
'''
    (folder/'articulo.md').write_text(article_txt,encoding='utf-8')
print('created',created,'unit files and',len(arts)-1,'article files')

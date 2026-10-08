import json,re
from pathlib import Path
out=Path('tmp/pdfs/ley-21719')
blocks=[]
started=False
finished=False
for page in range(1,56):
 for raw in (out/f'main-{page:02}.txt').read_text(encoding='utf-8').splitlines():
  if not started:
   if raw.startswith('     "Artículo primero.-'):started=True
   else:continue
  if finished:break
  if raw.startswith('     Habiéndose cumplido'):finished=True;break
  if raw.strip()=='DISPOSICIONES TRANSITORIAS':
   blocks.append({'text':raw.strip(),'pages':[page],'kind':'heading'});continue
  if raw.startswith('     '):
   blocks.append({'text':raw.strip(),'pages':[page]})
  elif blocks:
   blocks[-1]['text']+=' '+raw.strip()
   if page not in blocks[-1]['pages']:blocks[-1]['pages'].append(page)
 if finished:break
for i,b in enumerate(blocks):
 b['i']=i
(out/'blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(blocks))
for b in blocks[:55]+blocks[-18:]:print(b['i'],b['pages'],b['text'][:135])

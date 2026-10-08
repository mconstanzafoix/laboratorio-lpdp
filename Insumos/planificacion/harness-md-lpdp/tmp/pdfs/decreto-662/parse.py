from pypdf import PdfReader
import re,json
r=PdfReader('Fuentes-primarias/Decreto-662-2026/Decreto-662_09-SEP-2026.pdf')
blocks=[]
for p,page in enumerate(r.pages,1):
 lines=page.extract_text().splitlines()
 for line in lines:
  if not line.strip() or line.startswith('Decreto 662, HACIENDA') or line.startswith('Biblioteca del Congreso') or re.match(r'\s*página \d+ de \d+',line): continue
  if re.match(r'^\s{5}\S',line): blocks.append({'text':line.strip(),'pages':[p]})
  elif blocks:
   blocks[-1]['text'] += ' '+line.strip()
   if p not in blocks[-1]['pages']:blocks[-1]['pages'].append(p)
blocks=blocks[next(i for i,x in enumerate(blocks) if x['text']=='Decreto:'):]
for i,b in enumerate(blocks): print(f"{i:03d} {b['pages']} {b['text'][:145]}")
open('tmp/pdfs/decreto-662/blocks.json','w').write(json.dumps(blocks,ensure_ascii=False,indent=2))

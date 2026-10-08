from pathlib import Path
import pdfplumber
p='Fuentes-primarias/Ley-21719-2024/Ley-21719_13-DIC-2024.pdf'
out=Path('tmp/pdfs/ley-21719')
with pdfplumber.open(p) as doc:
 for n,page in enumerate(doc.pages,1):
  words=[w for w in page.extract_words(x_tolerance=2,y_tolerance=2) if w['x0']<445 and 45<=w['top']<755]
  lines=[]
  for w in words:
   if not lines or abs(lines[-1][0]-w['top'])>2:
    lines.append((w['top'],[w]))
   else:lines[-1][1].append(w)
  text=[]
  for top,ws in lines:
   ws.sort(key=lambda x:x['x0'])
   x=ws[0]['x0']
   s=' '.join(w['text'] for w in ws)
   text.append(('     ' if x>=98 else '')+s)
  (out/f'main-{n:02}.txt').write_text('\n'.join(text)+'\n',encoding='utf-8')
(out/'main-all.txt').write_text('\n'.join(f'<<< PAGE {n} >>>\n'+(out/f'main-{n:02}.txt').read_text() for n in range(1,len(doc.pages)+1)),encoding='utf-8')

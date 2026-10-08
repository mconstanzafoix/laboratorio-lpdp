from pathlib import Path
import json,re
root=Path('Fragmentador-de-Fuentes/Fuentes/Decreto-662-version-2026-09-09')
b=json.loads(Path('tmp/pdfs/decreto-662/blocks.json').read_text())
n=json.loads(Path('tmp/pdfs/decreto-662/manifest.json').read_text())
errors=[]
for x in n:
 p=Path(x['path'])
 if not p.is_file():errors.append(('missing',p));continue
 t=p.read_text()
 if '> '+x['literal']+'\n' not in t:errors.append(('literal missing',p))
 if f'página(s) {", ".join(map(str,x["pages"]))}' not in t:errors.append(('pages',p))
 for dest in re.findall(r'\]\(([^)]+\.md)\)',t):
  if not (p.parent/dest).exists():errors.append(('broken link',p,dest))
for i in sorted(set(x['block'] for x in n)):
 xs=[x for x in n if x['block']==i]
 actual=' '.join(x['literal'] for x in xs)
 expected=b[i]['text']
 if re.match(r'^Artículo \d+\.-',expected):expected=re.sub(r'^Artículo \d+\.- [^.]+\. ','',expected)
 if actual!=expected:errors.append(('reconstruct',i,actual[:40],expected[:40]))
expected_ids=set(range(4,101))-{8,9,10,11,41,42,74,75}
if set(x['block'] for x in n)!=expected_ids:errors.append(('coverage ids',sorted(expected_ids-set(x['block'] for x in n))))
for p in root.glob('articulo-*/articulo.md'):
 t=p.read_text()
 for dest in re.findall(r'\]\(([^)]+\.md)\)',t):
  if not (p.parent/dest).exists():errors.append(('article link',p,dest))
tree=(root/'ARBOL.md').read_text()
for x in n:
 rel=Path(x['path']).relative_to(root).as_posix()
 if rel not in tree:errors.append(('tree missing',rel))
print('articles',len(list(root.glob('articulo-*/articulo.md'))))
print('literal_files',len(n),'source_blocks',len(set(x['block'] for x in n)))
print('errors',len(errors))
for e in errors[:30]:print(e)

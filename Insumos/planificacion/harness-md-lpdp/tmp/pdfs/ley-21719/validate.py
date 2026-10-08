import json,re,collections
from pathlib import Path
N=json.load(open('tmp/pdfs/ley-21719/structure.json'))
P=json.load(open('tmp/pdfs/ley-21719/paths.json'))
root=Path('Fragmentador-de-Fuentes/Fuentes/Ley-21719-version-diferida-2026-12-01')
errors=[]
for n in N:
 i=n['i']
 if i==619:continue
 path=root/P[str(i)]
 if not path.exists():errors.append(f'missing {i} {path}');continue
 s=path.read_text(encoding='utf-8')
 if '> '+n['text']+'\n' not in s:errors.append(f'literal mismatch {i} {path}')
 for page in n['pages']:
  if not re.search(r'\b'+str(page)+r'\b',s.split('## Texto literal')[0]):errors.append(f'page missing {i} p{page}')
for md in root.rglob('*.md'):
 s=md.read_text(encoding='utf-8')
 for link in re.findall(r'\]\(([^)]+\.md)\)',s):
  if not (md.parent/link).resolve().exists():errors.append(f'broken link {md}: {link}')
print('blocks',len(N),'files',len(list(root.rglob('*.md'))),'errors',len(errors))
for e in errors[:100]:print(e)

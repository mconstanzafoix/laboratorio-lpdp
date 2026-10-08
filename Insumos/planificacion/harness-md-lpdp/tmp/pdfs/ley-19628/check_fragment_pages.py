from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
DEST=ROOT/'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01'
normalize=lambda s: ' '.join(s.split())
issues=[]
rows=[]
for file in sorted(DEST.glob('*/*-fragmento-*.md')):
    t=file.read_text(encoding='utf-8')
    match=re.search(r'## Texto literal\s*\n(.*?)(?=\n## |\Z)',t,re.S)
    assert match,file
    literal=normalize(' '.join(line[2:] for line in match.group(1).splitlines() if line.startswith('> ')))
    parent=DEST/file.parent.name/(file.name.split('-fragmento-')[0]+'.md')
    pt=parent.read_text(encoding='utf-8')
    line=next(x for x in pt.splitlines() if x.startswith('- **Original:**'))
    allpages=[int(n) for n in re.findall(r'(?<!\d)\d{1,2}(?!\d)',line.split('`,',1)[1])]
    pieces=[normalize((HERE/f'body-{p:02}.txt').read_text(encoding='utf-8')) for p in allpages]
    combined=' '.join(pieces)
    loc=combined.find(literal)
    if loc<0:
        issues.append((str(file.relative_to(DEST)),'literal not located in parent pages',allpages))
        continue
    if combined.find(literal,loc+1)>=0:
        issues.append((str(file.relative_to(DEST)),'multiple occurrences',allpages))
        continue
    start=0
    hits=[]
    for p,piece in zip(allpages,pieces):
        end=start+len(piece)
        if loc<end and loc+len(literal)>start:hits.append(p)
        start=end+1
    declared=[int(n) for n in re.findall(r'(?<!\d)\d{1,2}(?!\d)',next(x for x in t.splitlines() if x.startswith('- **Original:**')).split('`,',1)[1])]
    rows.append({'file':str(file.relative_to(DEST)),'actual_pages':hits,'declared_pages':declared})
    if hits!=declared:issues.append((str(file.relative_to(DEST)),'page mismatch',hits,declared))
print(json.dumps({'checked':len(rows),'issues':issues},ensure_ascii=False,indent=2))

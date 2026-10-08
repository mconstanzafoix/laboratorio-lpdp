import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DEST=ROOT/'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01'
arts=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'))
index=json.loads((HERE/'line_index.json').read_text(encoding='utf-8'))

def literal(p):
    txt=p.read_text(encoding='utf-8')
    m=re.search(r'## Texto literal\n\n> (.*?)\n\n',txt,re.S)
    assert m,p
    return m.group(1)

expected=set()
checks=0
for a in arts:
    slug=('transitorio-' if a['transitory'] else 'articulo-')+f"{a['num']:02}"+(('-'+a['suffix']) if a['suffix'] else '')
    artpath=DEST/slug/'articulo.md'
    assert artpath.exists(),artpath
    expected.add(artpath.relative_to(DEST).as_posix())
    reconstructed=[]
    for b in a['blocks']:
        path=DEST/b['path']
        assert path.exists(),path
        assert literal(path)==b['text'],(path,'literal mismatch')
        expected.add(path.relative_to(DEST).as_posix())
        reconstructed.append(literal(path))
        checks+=1
        children=sorted(path.parent.glob(path.stem+'-fragmento-*.md'))
        if children:
            assert 'unidad estructural' in path.read_text(encoding='utf-8'),path
            assert ' '.join(literal(c) for c in children)==b['text'],(path,'fragment coverage mismatch')
            for child in children:
                expected.add(child.relative_to(DEST).as_posix())
                checks+=1
    assert len(reconstructed)==len(a['blocks'])

actual={p.relative_to(DEST).as_posix() for p in DEST.glob('*/*.md')}
assert expected==actual,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}

tree=(DEST/'ARBOL.md').read_text(encoding='utf-8')
paths=re.findall(r'->\s+([^\s]+\.md)',tree)
assert len(paths)==len(expected),(len(paths),len(expected))
assert set(paths)==expected,{'missing_in_tree':sorted(expected-set(paths)),'extra_in_tree':sorted(set(paths)-expected)}

badlinks=[]
for p in DEST.rglob('*.md'):
    txt=p.read_text(encoding='utf-8')
    for link in re.findall(r'\]\(([^)]+\.md)\)',txt):
        target=(p.parent/link).resolve()
        if not target.exists():badlinks.append((str(p.relative_to(DEST)),link))
assert not badlinks,badlinks[:20]

used=set()
for span in index['spans']:
    rowrange=set(range(span['start'],span['end']))
    assert not used.intersection(rowrange)
    used.update(rowrange)
assert len(index['spans'])==len(arts)==86
excluded=[row for j,row in enumerate(index['lines']) if j not in used]
assert len(used)==2894 and len(excluded)==86,(len(used),len(excluded))
assert sum(1 for a in arts if a['transitory'])==3
assert sum(1 for a in arts if not a['transitory'])==83

result={'articles':86,'permanent':83,'transitory':3,'structural_units':sum(len(a['blocks']) for a in arts),
        'atomic_fragments':len(expected)-86-sum(len(a['blocks']) for a in arts),'unit_checks':checks,
        'article_lines':len(used),'context_lines':len(excluded),'tree_paths':len(paths),
        'broken_links':len(badlinks)}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

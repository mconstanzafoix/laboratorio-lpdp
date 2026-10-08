from pathlib import Path
import json,re,pdfplumber
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SOURCE='Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
DEST=ROOT/'Fragmentador-de-Fuentes/Fuentes/Ley-19628-consolidada-desde-2026-12-01'
norm=lambda t: re.sub(r'\s+',' ',t).strip()
pages=[]
with pdfplumber.open(ROOT/SOURCE) as pdf:
    for page in pdf.pages:
        words=[w for w in page.extract_words(x_tolerance=2,y_tolerance=2) if w['x0']<445 and 45<=w['top']<755]
        rows=[]
        for word in words:
            if not rows or abs(rows[-1][0]-word['top'])>2:rows.append((word['top'],[word]))
            else:rows[-1][1].append(word)
        pages.append(norm(' '.join(' '.join(w['text'] for w in sorted(ws,key=lambda w:w['x0'])) for _,ws in rows)))
issues=[]
count=0
for file in sorted(DEST.rglob('*.md')):
    t=file.read_text(encoding='utf-8')
    match=re.search(r'## Texto literal\s*\n(.*?)(?=\n## |\Z)',t,re.S)
    if not match:continue
    literal=norm(' '.join(line[2:] for line in match.group(1).splitlines() if line.startswith('> ')))
    if not literal:continue
    count+=1
    loc=re.search(r'página(?:\(s\)|s)?(?: PDF)? ([\d, –-]+)',t)
    if not loc:
        issues.append({'archivo':str(file.relative_to(DEST)),'problema':'sin páginas reconocibles'})
        continue
    nums=[]
    for part in loc.group(1).strip().split(','):
        interval=re.findall(r'\d+',part)
        if len(interval)==2 and re.search(r'[-–]',part):nums.extend(range(int(interval[0]),int(interval[1])+1))
        else:nums.extend(map(int,interval))
    if literal not in norm(' '.join(pages[n-1] for n in nums)):
        issues.append({'archivo':str(file.relative_to(DEST)),'paginas':nums,'problema':'literal no coincide como secuencia en páginas indicadas'})
result={'literal_files_checked':count,'issues':issues}
(HERE/'literal_check_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'literal_files_checked':count,'issue_count':len(issues),'issues':issues[:4]},ensure_ascii=False))

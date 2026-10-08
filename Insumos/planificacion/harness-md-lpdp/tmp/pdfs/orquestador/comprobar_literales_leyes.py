from pathlib import Path
import json,re,pdfplumber
root=Path(__file__).resolve().parents[3]
configs=[('ley-19628','Ley-19628-consolidada-desde-2026-12-01','Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'),('ley-21719','Ley-21719-version-diferida-2026-12-01','Ley-21719-2024/Ley-21719_13-DIC-2024.pdf')]
def norm(t):return re.sub(r'\s+',' ',t).strip()
for name,out,source in configs:
    pages=[]
    with pdfplumber.open(root/'Fuentes-primarias'/source) as pdf:
        for page in pdf.pages:
            words=[w for w in page.extract_words(x_tolerance=2,y_tolerance=2) if w['x0']<445 and 45<=w['top']<755]
            rows=[]
            for word in words:
                if not rows or abs(rows[-1][0]-word['top'])>2:rows.append((word['top'],[word]))
                else:rows[-1][1].append(word)
            pages.append(norm(' '.join(' '.join(w['text'] for w in sorted(ws,key=lambda w:w['x0'])) for y,ws in rows)))
    results=[];count=0
    for file in sorted((root/'Fragmentador-de-Fuentes/Fuentes'/out).rglob('*.md')):
        t=file.read_text()
        match=re.search(r'## Texto literal\s*\n(.*?)(?=\n## |\Z)',t,re.S)
        if not match:continue
        literal=norm(' '.join(line[2:] for line in match.group(1).splitlines() if line.startswith('> ')))
        if not literal:continue
        count+=1
        loc=re.search(r'página(?:\(s\)|s)?(?: PDF)? ([\d, –-]+)',t)
        if not loc:
            results.append({'archivo':str(file.relative_to(root)),'problema':'sin páginas reconocibles'});continue
        nums=[]
        for part in loc.group(1).strip().split(','):
            interval=re.findall(r'\d+',part)
            if len(interval)==2 and re.search(r'[-–]',part):nums.extend(range(int(interval[0]),int(interval[1])+1))
            else:nums.extend(map(int,interval))
        expected=norm(' '.join(pages[n-1] for n in nums))
        if literal not in expected:
            results.append({'archivo':str(file.relative_to(root)),'paginas':nums,'problema':'literal no coincide como secuencia en páginas indicadas','inicio':literal[:130]})
    report={'fuente':source,'control':'Presencia íntegra de cada literal en páginas del PDF (columna principal; solo normalización de espacios). No acredita cobertura por sí solo.','literales_comprobados':count,'incidencias':results}
    (Path(__file__).parent/f'literales-{name}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({'fuente':name,'literales':count,'incidencias':len(results),'muestra':results[:5]},ensure_ascii=False))

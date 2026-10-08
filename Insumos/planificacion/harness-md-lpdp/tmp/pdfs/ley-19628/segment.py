import json
import re
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent
PDF = ROOT.parents[2] / 'Fuentes-primarias/Ley-19628-consolidada-desde-2026-12-01/LEY-19628_28-AGO-1999 modificada con la Ley 21.719.pdf'
ART = re.compile(r'^Artículo\s+(\d+)[°º]?(?:\s+(bis|ter|quáter|quinquies|sexies|septies|octies|nonies))?\.-')
SECT = re.compile(r'^(Título (?:Preliminar|[IVX]+)|Párrafo (?:Primero|Segundo|Tercero|Cuarto|Quinto)|Disposiciones transitorias)$')

all_lines = []
with pdfplumber.open(PDF) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        if page_num > 56:
            break
        for row in page.crop((65, 0, 445, 740)).extract_text_lines():
            text = row['text'].strip()
            if not text:
                continue
            all_lines.append({'p': page_num, 'y': round(row['top'], 1), 'x': round(row['x0'], 1), 't': text})

sections = []
for i, row in enumerate(all_lines):
    if SECT.match(row['t']) and (row['x'] >= 95):
        sections.append(i)

articles = []
transitory = False
for i, row in enumerate(all_lines):
    if row['t'] == 'Disposiciones transitorias':
        transitory = True
    match = ART.match(row['t']) if row['x'] >= 95 else None
    if match:
        articles.append({'start': i, 'num': int(match.group(1)), 'suffix': match.group(2) or '', 'transitory': transitory})

spans=[]
for n, art in enumerate(articles):
    end = articles[n+1]['start'] if n+1 < len(articles) else len(all_lines)
    cuts = [k for k in sections if art['start'] < k < end]
    if art['transitory'] and art['num'] == 3:
        cuts.append(next(k for k in range(art['start']+1,end) if all_lines[k]['t'].startswith('Habiéndose cumplido')))
    if not art['transitory'] and art['num'] == 55:
        cuts.append(next(k for k in range(art['start']+1,end) if all_lines[k]['t'] == 'NOTA'))
    if cuts:
        end = min(cuts)
    spans.append({'num':art['num'],'suffix':art['suffix'],'transitory':art['transitory'],'start':art['start'],'end':end})
    art['lines'] = all_lines[art['start']:end]
    # A new paragraph normally begins at the typewriter's first-line indent.
    blocks = []
    for j, row in enumerate(art['lines']):
        if j == 0 or row['x'] >= 94:
            blocks.append({'lines': [row]})
        else:
            blocks[-1]['lines'].append(row)
    for b in blocks:
        b['text'] = ' '.join(x['t'] for x in b['lines'])
        b['pages'] = sorted({x['p'] for x in b['lines']})
        del b['lines']
    art['blocks'] = blocks
    del art['lines']
    del art['start']

(ROOT/'segments.json').write_text(json.dumps(articles,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'line_index.json').write_text(json.dumps({'lines':all_lines,'sections':sections,'spans':spans},ensure_ascii=False,indent=2),encoding='utf-8')
for a in articles:
    tag = f"{a['num']}{('-'+a['suffix']) if a['suffix'] else ''}{'-T' if a['transitory'] else ''}"
    print(f"{tag:18} {len(a['blocks']):3} p{a['blocks'][0]['pages'][0]}-{a['blocks'][-1]['pages'][-1]}  ",a['blocks'][0]['text'][:80])

"""Genera ../index.html desde template.html + data/ + pose/.

Uso:  python3 tools/build.py   (desde la raíz del repo, o desde cualquier lado)
"""
import json, glob, os

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)

tpl = open(os.path.join(BASE, 'template.html')).read()
data = json.dumps(json.load(open(os.path.join(BASE, 'data', 'data_es.json'))),
                  ensure_ascii=False, separators=(',', ':'))

trails = {}
for f in sorted(glob.glob(os.path.join(BASE, 'pose', 'trails_*.json'))):
    code = os.path.basename(f)[len('trails_'):-len('.json')]
    trails[code] = json.load(open(f))

out = tpl.replace('__DATA__', data)
out = out.replace('__TRAILS__', json.dumps(trails, separators=(',', ':')))

dest = os.path.join(REPO, 'index.html')
open(dest, 'w').write(out)
print(f'{dest} generado | {len(out)} bytes | trails: {sorted(trails)}')

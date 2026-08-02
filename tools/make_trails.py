"""Convierte pose_<código>.json (detección cruda) en trails_<código>.json.

Uso: python3 tools/make_trails.py
Requiere que exista pose/pose_<código>.json para cada código en ID_MAP.
El mapeo de IDs de tracking a roles se determina viendo el video:
quien mira a cámara trackea estable; los fragmentos del ocluido se
encadenan por coexistencia temporal (dos ids que coexisten = dos personas).
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
POSE = os.path.join(BASE, 'pose')

ID_MAP = {
    'awa': {'lead': ['1', '4'], 'follow': ['2']},
    'aoc': {'follow': ['1'], 'lead': ['4', '12', '13', '11', '9']},
    'aga': {'follow': ['1'], 'lead': ['3', '12', '9', '10']},
    'spl': {'lead': ['1', '3'], 'follow': ['2']},
    'sfh': {'follow': ['1'], 'lead': ['2', '8', '5']},
    'sdt': {'follow': ['1'], 'lead': ['3']},
    'lvv': {'lead': ['1'], 'follow': ['2']},
    'eca': {'follow': ['2'], 'lead': ['1']},
    'eos': {'follow': ['1'], 'lead': ['2', '6']},
    'bre': {'follow': ['1', '6', '20'], 'lead': ['2', '9', '13', '19']},
}

def build_trails(posefile, id_map, conf_min=0.5, smooth_w=5, keep_every=2):
    data = json.load(open(posefile))
    feet = {}
    for role, ids in id_map.items():
        for foot, ck in (('la', 'lc'), ('ra', 'rc')):
            pts = []
            for fr in data:
                for pid in ids:
                    if pid in fr['p'] and fr['p'][pid][ck] >= conf_min:
                        x, y = fr['p'][pid][foot]
                        pts.append([fr['t'], x, y])
                        break
            sm = []
            for i in range(len(pts)):
                lo = max(0, i - smooth_w // 2); hi = min(len(pts), i + smooth_w // 2 + 1)
                win = [p for p in pts[lo:hi] if abs(p[0] - pts[i][0]) < 0.45]
                xs = [p[1] for p in win]; ys = [p[2] for p in win]
                sm.append([round(pts[i][0], 2), round(sum(xs) / len(xs), 3),
                           round(sum(ys) / len(ys), 3)])
            if sm:
                feet[f'{role}_{foot}'] = sm[::keep_every]
    return feet

if __name__ == '__main__':
    for code, id_map in ID_MAP.items():
        src = os.path.join(POSE, f'pose_{code}.json')
        if not os.path.exists(src):
            print(f'{code}: sin pose_{code}.json, salteado')
            continue
        trails = build_trails(src, id_map)
        json.dump(trails, open(os.path.join(POSE, f'trails_{code}.json'), 'w'))
        print(code, {k: len(v) for k, v in trails.items()})

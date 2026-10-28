"""Export the structured input of the pilot matches (prompt v1, condition A: raw data).

Run from the repo root:  python scripts/export_pilot_inputs.py
Input:  data/processed/pilot_games.csv, data/raw/<year>.wikitext
Output: data/processed/pilot_inputs.json (input fields + a `truth` block that is not sent to the model)

Scorers are kept as written in the Wikipedia match box (wiki markup removed), not
re-parsed per player. The score and the sum test come from parse_matches.py.
"""
import csv
import json
import re
from pathlib import Path

import parse_matches as pm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'processed'


def scorers(f, side):
    parts = [pm.clean(f.get(k + side, '')) for k in ('goals', 'points')]
    s = '; '.join(p for p in parts if p)
    s = re.sub(r'\s+', ' ', s.replace('–', '-').replace('−', '-'))
    return s.strip(' ;')


def truth(t1, t2, s1, s2):
    """Ground truth computed from the score (1 goal = 3 points). Never sent to the model."""
    a, b = s1[0] * 3 + s1[1], s2[0] * 3 + s2[1]
    return {'points': {'team1': a, 'team2': b},
            'winner': t1 if a > b else t2 if b > a else 'draw',
            'margin_points': abs(a - b)}


def main():
    pilot = list(csv.DictReader(open(OUT / 'pilot_games.csv', encoding='utf-8')))
    want = {(int(r['year']), int(r['line'])): r for r in pilot}
    out = []
    for y in pm.YEARS:
        text = (pm.RAW / f'{y}.wikitext').read_text(encoding='utf-8')
        for blk in pm.blocks(text):
            line = text[:text.find(blk)].count('\n') + 1
            if (y, line) not in want:
                continue
            f = pm.fields(blk)
            (g1, p1), (g2, p2) = pm.parse_score(f)
            assert (g1, p1) == pm.team_total(f, '1') and (g2, p2) == pm.team_total(f, '2'), (y, line)
            r = want[(y, line)]
            out.append({
                'id': len(out) + 1, 'year': y, 'line': line, 'permalink': r['permalink'],
                'date': pm.clean(f.get('date', '')), 'round': pm.clean(f.get('round', '')),
                'team1': pm.team(f.get('team1', '')), 'team2': pm.team(f.get('team2', '')),
                'score': {'team1': f'{g1}-{p1}', 'team2': f'{g2}-{p2}'},
                'scorers': {'team1': scorers(f, '1'), 'team2': scorers(f, '2')},
                'truth': truth(pm.team(f.get('team1', '')), pm.team(f.get('team2', '')), (g1, p1), (g2, p2)),
            })
    assert len(out) == len(want), (len(out), len(want))
    (OUT / 'pilot_inputs.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'{len(out)} matches written to {OUT / "pilot_inputs.json"}')


if __name__ == '__main__':
    main()

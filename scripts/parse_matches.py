"""Step 2 of the Wikipedia collection: parse match blocks from the raw wikitext,
run the sum test (points of the scorers = final score) and report exclusions.

Run from the repo root:  python scripts/parse_matches.py [--list]
Input:  data/raw/<year>.wikitext
Output: printed summary + data/processed/matches_exclusions.csv and matches_summary.md
"""
import csv
import json
import re
import sys
from datetime import date
from collections import Counter
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
YEARS = [2021, 2022, 2023, 2024]
START = re.compile(r'\{\{\s*(GAA\s*match(?:box)?|football\s*box(?:\s*collapsible)?)\b', re.I)
DASH = r'[–\-−]'
GP = re.compile(rf'(\d+)\s*{DASH}\s*(\d+)')


def clean(s):
    s = re.sub(r'<ref[^>]*/>', '', s)
    s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'\{\{\s*nowrap\s*\|([^{}]*)\}\}', r'\1', s, flags=re.I)  # keep names inside nowrap
    s = re.sub(r'\{\{[^{}]*\}\}', '', s)
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
    return s.strip()


def blocks(text):
    starts = [m.start() for m in START.finditer(text)] + [len(text)]
    for a, b in zip(starts, starts[1:]):
        blk = text[a:b]
        end = blk.find('\n}}')
        yield blk[:end] if end > 0 else blk


def fields(blk):
    out = {}
    for part in re.split(r'\n\s*\|', blk)[1:]:
        if '=' in part:
            k, v = part.split('=', 1)
            out[k.strip().lower()] = v.strip()
    return out


def team(raw):
    raw = re.sub(r'\[\[File:[^\]]*\]\]', '', raw or '')
    return clean(raw)


def parse_score(f):
    """Return ((g1,p1),(g2,p2)) or None."""
    if f.get('score'):
        pairs = GP.findall(clean(f['score']))
        if len(pairs) == 2:
            return tuple(map(int, pairs[0])), tuple(map(int, pairs[1]))
    if f.get('score1') and f.get('score2'):
        a, b = GP.findall(clean(f['score1'])), GP.findall(clean(f['score2']))
        if len(a) == 1 and len(b) == 1:
            return tuple(map(int, a[0])), tuple(map(int, b[0]))
    return None


def count_scorers(raw, kind):
    """kind: 'goals', 'points' or 'both'. Returns (goals, points) or raises ValueError."""
    s = clean(raw)
    # count inside the brackets right after a name: "Name (1-6, 5f)" / "Name (0-2 each)"
    s = re.sub(rf'(?<=[^\W\d_])\s*\((\d+\s*{DASH}\s*\d+)(?![\da-zA-Z])(?!\s*(?:marks?|frees?|pens?)\b)([^()]*)\)',
               lambda m: ' ' + m.group(1) + (' each' if re.search(r'\beach\b', m.group(2), re.I) else ''), s)
    s = re.sub(r'\([^()]*\)', '', s)          # drop details: (2f), (1 mark), (1f, 145)
    s = s.replace('(', '').replace(')', '')     # stray brackets (typos in the source)
    s = re.sub(rf'\ball\s+(\d+\s*{DASH}\s*\d+)', r'\1 each', s)  # "A, B, C all 0-1"
    s = s.replace('.', ' ').replace(';', ',')
    tokens = [t.strip() for t in re.split(r',|\band\b|&', s) if t.strip()]
    g = p = 0
    pending = 0
    for t in tokens:
        each = bool(re.search(r'\beach\s*$', t, re.I))
        t = re.sub(r'\beach\s*$', '', t, flags=re.I).strip()
        m = re.search(rf'(\d+)\s*{DASH}\s*(\d+)[a-zA-Z]{{0,3}}\s*$', t)
        if m:
            cg, cp = int(m.group(1)), int(m.group(2))
        else:
            m = re.search(r'(\d+)[a-zA-Z]{0,3}\s*$', t)
            if not m:
                pending += 1
                continue
            n = int(m.group(1))
            if kind == 'goals':
                cg, cp = n, 0
            elif kind == 'points':
                cg, cp = 0, n
            else:
                raise ValueError('plain count in combined field')
        if each:
            k = pending + 1
        else:
            if pending:
                raise ValueError('names without count')
            k = 1
        g += cg * k
        p += cp * k
        pending = 0
    if pending:
        raise ValueError('names without count')
    return g, p


def team_total(f, side):
    """Sum scorers for side '1' or '2'. Returns (g,p) or raises ValueError / KeyError."""
    gk, pk = f.get('goals' + side, ''), f.get('points' + side, '')
    if not gk.strip() and not pk.strip():
        raise KeyError('no_scorers')
    g = p = 0
    if gk.strip():
        # combined format has "g–p" tokens inside the goals field
        kind = 'both' if (not pk.strip() or GP.search(clean(gk))) else 'goals'
        gg, gp = count_scorers(gk, kind)
        g += gg; p += gp
    if pk.strip():
        pg, pp = count_scorers(pk, 'points')
        g += pg; p += pp
    return g, p


REASONS = [
    ('no_score', 'No final score in the match box'),
    ('no_scorers', 'No scorer lists in the match box'),
    ('extra_time', 'Match went to extra time and/or a penalty shoot-out (left out for now)'),
    ('parse_error', 'Scorer list could not be parsed (ambiguous or malformed in the source)'),
    ('sum_mismatch', 'Scorers do not add up to the final score (sum test failed)'),
]
OUT = Path(__file__).resolve().parents[1] / 'data' / 'processed'


def main():
    show = '--list' in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    excluded, included, counts, meta = [], [], {}, {}
    for y in YEARS:
        text = (RAW / f'{y}.wikitext').read_text(encoding='utf-8')
        meta[y] = json.loads((RAW / f'{y}.meta.json').read_text(encoding='utf-8'))
        c = counts[y] = Counter()
        for blk in blocks(text):
            f = fields(blk)
            c['total'] += 1
            line = text[:text.find(blk)].count('\n') + 1
            row = dict(year=y, line=line, date=clean(f.get('date', ''))[:40], round=clean(f.get('round', ''))[:40],
                       team1=team(f.get('team1', '')), team2=team(f.get('team2', '')),
                       permalink=meta[y]['permalink'])
            score_raw = ' '.join(f.get(k, '') for k in ('score', 'score1', 'score2'))
            # Wikipedia flags extra time with its own |aet = yes parameter (and penalties with
            # |penaltyscore / |penalties1), so looking only at the score text is not enough.
            flagged = f.get('aet', '').strip().lower() in ('yes', 'y', 'true', '1') \
                or any(f.get(k, '').strip() for k in ('penaltyscore', 'penalties1', 'penalties2'))
            if flagged or re.search(r'a\.e\.t|\baet\b|extra time|shoot-?out|\bpens?\b', score_raw, re.I):
                c['extra_time'] += 1
                excluded.append({**row, 'score_listed': '', 'reason': 'extra_time', 'detail': ''}); continue
            sc = parse_score(f)
            if not sc:
                c['no_score'] += 1
                excluded.append({**row, 'score_listed': '', 'reason': 'no_score', 'detail': ''}); continue
            row['score_listed'] = f'{sc[0][0]}-{sc[0][1]} v {sc[1][0]}-{sc[1][1]}'
            try:
                t1, t2 = team_total(f, '1'), team_total(f, '2')
            except KeyError:
                c['no_scorers'] += 1
                excluded.append({**row, 'reason': 'no_scorers', 'detail': ''}); continue
            except ValueError as e:
                c['parse_error'] += 1
                excluded.append({**row, 'reason': 'parse_error', 'detail': str(e)}); continue
            if t1 == sc[0] and t2 == sc[1]:
                c['ok'] += 1
                included.append(row)
                if show:
                    print(y, row['date'].ljust(24), row['team1'], row['score_listed'], row['team2'])
            else:
                c['sum_mismatch'] += 1
                excluded.append({**row, 'reason': 'sum_mismatch',
                                 'detail': f'scorers sum to {t1[0]}-{t1[1]} v {t2[0]}-{t2[1]}'})
    cols = ['year', 'line', 'date', 'round', 'team1', 'team2', 'score_listed', 'reason', 'detail', 'permalink']
    with open(OUT / 'matches_exclusions.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(excluded)
    with open(OUT / 'matches_included.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=[k for k in cols if k not in ('reason', 'detail')])
        w.writeheader(); w.writerows(included)
    tot = Counter()
    for c in counts.values(): tot.update(c)
    lines = ['# Wikipedia match collection: inclusion and exclusion summary', '',
             f'Generated by `scripts/parse_matches.py` on {date.today().isoformat()}. '
             'A match is included only if the scorers listed for each team add up to the final score (sum test).', '',
             '| Season page | Revision id | Retrieved | Match boxes | Included | ' + ' | '.join(k for k, _ in REASONS) + ' |',
             '|---|---|---|---|---|' + '---|' * len(REASONS)]
    for y in YEARS:
        c = counts[y]
        lines.append(f"| {y} All-Ireland SFC | {meta[y]['revid']} | {meta[y]['retrieved_at'][:10]} | {c['total']} | {c['ok']} | "
                     + ' | '.join(str(c[k]) for k, _ in REASONS) + ' |')
    lines.append(f"| **Total** | | | {tot['total']} | {tot['ok']} | " + ' | '.join(str(tot[k]) for k, _ in REASONS) + ' |')
    lines += ['', '## Exclusion reasons', ''] + [f'- `{k}`: {d}' for k, d in REASONS]
    lines += ['', 'Per-match detail (line in the raw file, teams, permalink): `matches_exclusions.csv`.', '']
    (OUT / 'matches_summary.md').write_text('\n'.join(lines), encoding='utf-8')
    for y in YEARS:
        c = counts[y]
        print(f"{y}: matches {c['total']} | included {c['ok']} | " + ' | '.join(f'{k} {c[k]}' for k, _ in REASONS))
    print(f"TOTAL: matches {tot['total']} | included {tot['ok']} | " + ' | '.join(f'{k} {tot[k]}' for k, _ in REASONS))
    print(f"saved to {OUT}")


if __name__ == '__main__':
    main()

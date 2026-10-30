"""Pilot run: generate one match report per pilot match with prompt v1 (condition A).

Run from the repo root:
  python scripts/run_pilot.py --dry-run        # build and show the prompts, no API call
  python scripts/run_pilot.py --only 1         # one match
  python scripts/run_pilot.py                  # all matches in pilot_inputs.json

The prompt template is read from prompts/v1_condition_a.md, so the text sent is exactly
the versioned one. Its SHA-256 is saved with every run. The API key is read from .env
(OPENAI_API_KEY), which is not tracked by git.
Output: outputs/pilot_runs/<YYYY-MM-DD_HHMM>/ (run_info.json + one game_NN.json per match).
A run folder is never overwritten and failed calls are recorded, not retried.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = ROOT / 'prompts' / 'v1_condition_a.md'
INPUTS = ROOT / 'data' / 'processed' / 'pilot_inputs.json'
RUNS = ROOT / 'outputs' / 'pilot_runs'
MODEL = 'gpt-6.1-sol'


def load_template():
    raw = PROMPT_FILE.read_bytes()
    text = raw.decode('utf-8')
    section = text.split('## Message sent to the model', 1)[1]
    m = re.search(r'```\n(.*?)\n```', section, re.S)
    if not m:
        sys.exit('Template block not found in ' + str(PROMPT_FILE))
    return m.group(1), hashlib.sha256(raw).hexdigest()


def build_prompt(template, g):
    values = {
        'year': g['year'], 'round': g['round'], 'date': g['date'],
        'team1': g['team1'], 'team2': g['team2'],
        'score_team1': g['score']['team1'], 'score_team2': g['score']['team2'],
        'scorers_team1': g['scorers']['team1'], 'scorers_team2': g['scorers']['team2'],
    }
    prompt = template
    for k, v in values.items():
        prompt = prompt.replace('{' + k + '}', str(v))
    left = re.findall(r'\{[a-z_0-9]+\}', prompt)
    if left:
        sys.exit(f'Unfilled placeholders in game {g["id"]}: {left}')
    return prompt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', type=int, help='run a single match id')
    a = ap.parse_args()
    games = json.loads(INPUTS.read_text(encoding='utf-8'))
    if a.only:
        games = [g for g in games if g['id'] == a.only]
        if not games:
            sys.exit(f'No match with id {a.only}')
    template, sha = load_template()
    prompts = {g['id']: build_prompt(template, g) for g in games}

    if a.dry_run:
        first = games[0]
        print(f'Template: {PROMPT_FILE}\nSHA-256: {sha}\nMatches: {len(games)}\n')
        print(f'--- prompt for match {first["id"]} ---\n{prompts[first["id"]]}\n---')
        for g in games:
            print(f'match {g["id"]:>2}: {g["team1"]} v {g["team2"]} ({len(prompts[g["id"]])} characters)')
        print('Dry run: no API call made, nothing written.')
        return

    from dotenv import load_dotenv
    from openai import OpenAI
    load_dotenv(ROOT / '.env')
    client = OpenAI()
    run_dir = RUNS / datetime.now().strftime('%Y-%m-%d_%H%M')
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / 'run_info.json').write_text(json.dumps({
        'prompt_file': 'prompts/v1_condition_a.md', 'prompt_sha256': sha, 'model_requested': MODEL,
        'api': 'responses', 'parameters': 'API defaults (none set)', 'matches': [g['id'] for g in games],
        'started_utc': datetime.now(timezone.utc).isoformat()}, indent=2), encoding='utf-8')
    for g in games:
        rec = {'match_id': g['id'], 'prompt': prompts[g['id']], 'model_requested': MODEL,
               'timestamp_utc': datetime.now(timezone.utc).isoformat()}
        try:
            r = client.responses.create(model=MODEL, input=prompts[g['id']])
            rec.update({'response_id': r.id, 'model_returned': r.model, 'report': r.output_text,
                        'usage': r.usage.model_dump() if r.usage else None})
            print(f'match {g["id"]:>2}: ok ({r.model})')
        except Exception as e:
            rec['error'] = f'{type(e).__name__}: {e}'
            print(f'match {g["id"]:>2}: ERROR {rec["error"]}')
        (run_dir / f'game_{g["id"]:02d}.json').write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Saved to {run_dir}')


if __name__ == '__main__':
    main()

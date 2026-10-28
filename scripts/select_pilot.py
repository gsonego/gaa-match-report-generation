"""Draw the pilot sample: 10 matches at random (fixed seed) from the matches that
pass the sum test (data/processed/matches_included.csv).

Run from the repo root (after parse_matches.py):  python scripts/select_pilot.py
Output: data/processed/pilot_games.csv (and printed list)
Same seed + same input = same 10 matches.
"""
import csv
import random
from pathlib import Path

SEED = 2026
N = 10
PROC = Path(__file__).resolve().parents[1] / "data" / "processed"


def main():
    with open(PROC / "matches_included.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    sample = random.Random(SEED).sample(rows, N)
    sample.sort(key=lambda r: (r["year"], int(r["line"])))
    with open(PROC / "pilot_games.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(sample)
    print(f"seed {SEED}: {N} of {len(rows)} matches")
    for r in sample:
        print(r["year"], f"line {r['line']}".ljust(11), r["date"].ljust(16), r["round"].ljust(18),
              r["team1"], r["score_listed"], r["team2"])


if __name__ == "__main__":
    main()

# Data

Description of data sources, collection and processing.

## Raw data (`data/raw/`)

Wikitext of the English Wikipedia season pages of the All-Ireland Senior Football Championship, 2021 to 2024 (licence CC BY-SA 4.0). Each page is saved with its revision id and retrieval date (`<year>.meta.json`), so every result can be traced to a fixed version of the page. Collected with `scripts/collect_wikipedia.py`.

| Season page | Revision id | Retrieved |
|---|---|---|
| 2021 | 1368408440 | 2026-10-21 |
| 2022 | 1376360989 | 2026-10-21 |
| 2023 | 1368377747 | 2026-10-21 |
| 2024 | 1368439200 | 2026-10-21 |

To collect again (this fetches the current revision, which may differ from the ones above): `python scripts/collect_wikipedia.py`.

## Processed data (`data/processed/`)

Produced from the raw pages by `scripts/parse_matches.py`. A match is included only if, for each team, the goals and points of the listed scorers add up to the final score (the sum test).

| File | Content |
|---|---|
| `matches_included.csv` | The 131 matches that pass the sum test (year, line in the saved page, date, round, teams, score, permalink) |
| `matches_exclusions.csv` | The 23 excluded matches, each with its reason and permalink |
| `matches_summary.md` | Counts per season page and per exclusion reason |

To rebuild: `python scripts/parse_matches.py` (needs the files in `data/raw/`).

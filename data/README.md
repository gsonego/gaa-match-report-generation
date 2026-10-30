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
| `matches_included.csv` | The 122 matches that pass the sum test and are not extra-time or penalty matches (year, line in the saved page, date, round, teams, score, permalink) |
| `matches_exclusions.csv` | The 32 excluded matches, each with its reason and permalink |
| `matches_summary.md` | Counts per season page and per exclusion reason |

To rebuild: `python scripts/parse_matches.py` (needs the files in `data/raw/`).

## Pilot sample (`data/processed/`)

| File | Content |
|---|---|
| `pilot_games.csv` | 10 matches drawn at random (seed 2026) from the 131 matches included at that time, by `scripts/select_pilot.py`. Game 10 (Armagh v Kerry, 2024) was later found to have gone to extra time and is now excluded from the included set. The sample is kept as it was run, and game 10 is treated as out of scope in the analysis. Running the script again on the corrected set would draw a different sample |
| `pilot_inputs.json` | Structured input of those matches, written by `scripts/export_pilot_inputs.py`: teams, date, round, score and the scorer lists as written in the source. Each match also has a `truth` block (points, winner, margin; 1 goal = 3 points) used to check the reports, which is not sent to the model |

## Validation against an independent source (`data/processed/`)

| File | Content |
|---|---|
| `validation_games.xlsx` | 20 matches (the 10 pilot matches plus 10 drawn at random, seed 2027) compared by hand with RTE Sport: score, date, round, winner and, for the pilot matches, the top scorer and total. The "How to" sheet explains the columns |
| `validation_summary.md` | Method, results and limits of the check |

## Exploration (`notebooks/`)

`notebooks/01_eda_wikipedia.ipynb` explores the included matches (matches per season, exclusion reasons, rounds, margins, goals, scorer notation, the pilot sample against the rest, coverage and the 20-match validation). Figures and tables are saved to `notebooks/figures/`. Run it from anywhere inside the repository after the files above are in place.

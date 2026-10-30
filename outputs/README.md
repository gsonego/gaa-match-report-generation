# Outputs

Generated reports and the checks made on them.

## `pilot_runs/2026-10-28_2207/`

The pilot run: one report for each of the 10 pilot matches, written with prompt v1 (`prompts/v1_condition_a.md`, condition A: raw scores and scorer lists) by `gpt-6.1-sol` through the OpenAI Responses API with default parameters.

| File | Content |
|---|---|
| `run_info.json` | Prompt file and its SHA-256, model requested, API, parameters, matches, start time (UTC) |
| `game_NN.json` | The exact prompt sent, the report, the model id returned, the response id, the token usage and the timestamp |

The reports are kept exactly as generated and are never regenerated or edited. A new run goes in a new folder (`scripts/run_pilot.py` refuses to overwrite one).

Match 10 (Armagh v Kerry, 2024) went to extra time. It was drawn before the extra-time filter of `scripts/parse_matches.py` was fixed, so it is part of the run but out of scope for the analysis, which uses matches 1 to 9.

## `pilot_error_table.xlsx`

Claim-by-claim check of the reports of matches 1 to 9 against `data/processed/pilot_inputs.json`: 146 claims, each with its type, a verdict (`ok`, `error`, `partly`, or not in the data) and a note. The sheet `Summary` counts the verdicts by claim type; the sheet `Notes` explains the method and its limits. The rows were written by hand after reading each report; `scripts/build_pilot_error_table.py` turns them into the workbook.

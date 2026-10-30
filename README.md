# GAA Match Report Generation

MSc in Applied Data Science dissertation, Dundalk Institute of Technology (2026-2027).

**Topic:** factual verification of LLM-generated GAA (Gaelic games) match reports from structured match data.

**Research question:** how can automated factual verification improve the reliability of LLM-generated sports match reports?

The contribution is the verification and its evaluation, not the report generator. Three verifiers (rule-based, LLM-based, hybrid) will be compared against human-labelled ground truth, and used as a publication gate: a report with no claim judged wrong is published, otherwise it is held for review.

## Status (interim, 30 Oct 2026)

- Data: Wikipedia All-Ireland SFC match boxes 2021-2024; 154 collected, 122 pass the sum test (see `data/README.md`).
- Validation: 20 matches checked against RTE Sport.
- Pilot: 10 reports with prompt v1 (`prompts/`), 9 in scope, 146 claims checked by hand (`outputs/`).
- Next: sealed test set, pre-registration, error taxonomy, verifiers (from November).

## Structure

| Folder | Content |
|---|---|
| `data/` | Data description and processed datasets (no raw third-party data) |
| `notebooks/` | Exploratory analysis (`01_eda_wikipedia.ipynb`) and figures |
| `scripts/` | Collection, parsing, pilot generation and error-table code |
| `models/` | Verifier configurations (empty until the verifiers are built) |
| `prompts/` | Experiment prompts, versioned |
| `outputs/` | Generated reports and the claim-level error table |
| `docs/` | Journal, supervisor meetings, ethics note and AI usage log |

## Reproduce

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then set OPENAI_API_KEY (only needed for run_pilot.py)

python scripts/collect_wikipedia.py       # saves raw pages (data/raw is not tracked)
python scripts/parse_matches.py           # sum test -> data/processed/
python scripts/select_pilot.py
python scripts/export_pilot_inputs.py
python scripts/run_pilot.py --dry-run     # then without --dry-run to call the API
python scripts/build_pilot_error_table.py
```

`collect_wikipedia.py` fetches the current page revisions; the revision ids used in the study are in `data/README.md`.

## Author

Guilherme Sonego Neto

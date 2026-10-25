# AI Usage Log

Generative AI tools were used in this project in line with the DkIT Academic Integrity Policy and the dissertation guidelines.

- One entry per work session that informed a decision, a method or a deliverable. Sessions with no bearing on the project are omitted.
- The main prompt is quoted verbatim or lightly trimmed.
- Prompts used in the experiments are part of the method and are kept separately in [`prompts/`](../prompts/).

Responsibility for all research decisions and for the final text remains with the author.

## Categories

- **Research / literature**: finding and summarising sources. All sources were read in the original.
- **Structuring / planning**: outlines and initial structure, revised by the author.
- **Code**: implementation support. All code was reviewed and tested by the author.
- **Data**: data processing support.
- **Text review**: language and clarity review of the author's own text.

## Entry template

```
### YYYY-MM-DD: short title
- Category:
- Tool / model:
- Main prompt:
- How the output was used or changed:
- Verification:
- Decision informed:
```

## Entries

### 2026-10-24: Wikipedia match parsing, sum test, exclusion log and pilot sample

- Category: Data / Code
- Tool / model: Claude (claude-opus-5-5, then claude-sonnet-5-5)
- Main prompt: "If we have enough data to start, let's exclude the inconsistencies. I'd like a summary of these situations recorded so we can put it in the dissertation."
- How the output was used or changed: the author asked for each step to be explained and approved before it was run. The author widened the scope from the All-Ireland knockout games to any match with complete data, decided to exclude inconsistent matches and log every exclusion, left matches that went to extra time or penalties out for now, and chose a seeded random draw for the pilot over a planned selection. A first parser fix caused a regression (2021 dropped from 6 to 4 matches passing the sum test); it was caught by comparing runs and then corrected.
- Verification: the sum test (scorers add up to the final score) was run over all 154 match boxes of the 2021-2024 season pages, and the pilot draw was run twice with identical output. The author checked by hand, against the raw page text, that the scorers of Dublin v Kildare (2022) add up to the listed score and that the Leitrim v Sligo (2024) scorer list is one point short of the listed score; one pilot match (Armagh v Kerry, 2024) was compared with the Wikipedia page of the saved revision.
- Decision informed: inclusion rule (sum test), exclusion log kept for the dissertation, pilot sample of 10 matches drawn at random (seed 2026) from the 131 that pass.

### 2026-10-21: Wikipedia collection and alternative data source

- Category: Data
- Tool / model: Claude (claude-opus-5-5)
- Main prompt: "Start the Wikipedia collection, and help me judge whether the data is rich enough; assess the Foireann open data API as an alternative."
- How the output was used or changed: the author ran the collection script on their own machine; the author asked for each step to be approved before it was run and wrote and sent the email to Foireann.
- Verification: scorer totals were checked against match scores for the 2024 knockout games; the API specification was read directly.
- Decision informed: the pilot data source stays Wikipedia; access to the Foireann API was requested.

### 2026-10-19: Kick-off: supervisor questions, repository layout and API access

- Category: Structuring / planning
- Tool / model: Claude (claude-opus-5-5)
- Main prompt: "Guide me step by step through today's kick-off tasks; rewrite the supervisor questions more concisely and explain each one in plain terms."
- How the output was used or changed: the author asked for the questions to be shortened, added a question on the depth of the project and a suggestion to compare several generator models in a second phase, and decided the repository layout and the pilot model.
- Verification: the Wikipedia limitations were checked on the 2025 championship page; model pricing was checked against public sources.
- Decision informed: questions for the supervisor meeting of 20 Oct 2026; repository layout; pilot model (OpenAI gpt-6.1-sol).

### 2026-10-18: Repository structure and roadmap consolidation

- Category: Structuring / planning
- Tool / model: Claude (claude-opus-5-5)
- Main prompt: "Compare the earlier decisions log with the roadmap approved by my supervisor, explain each item that could be carried over, and help me decide item by item."
- How the output was used or changed: the author reviewed 12 candidate items one at a time, accepted 10 and rejected 2 (automatic correction and editing-cost measurement). Together with 4 items selected earlier, the accepted items were written into the roadmap; superseded planning documents were removed. The two-repository layout and per-session AI log were also set up.
- Verification: each item was checked against the approved roadmap's research question and scope.
- Decision informed: the roadmap is the single plan of record; additions include a three-way claim verdict, invented-entity and coverage metrics, pre-registration of metrics, a template reference, clean-room matches, a sealed test set and rules for using published reports.

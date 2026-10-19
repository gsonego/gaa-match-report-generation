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

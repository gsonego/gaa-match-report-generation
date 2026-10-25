# Project Journal

One entry per week, newest first. Meetings with the supervisor are recorded in [`meetings.md`](meetings.md).

Template:

```
## Week YYYY-Www (dd Mon - dd Mon)
### Done
### Problems / decisions
### Next week
```

---

## Week 2026-W43 (19 Oct - 25 Oct)

### Plan
- Mon 19: kick-off. Public repository reorganised into the artefact layout (`data/`, `notebooks/`, `scripts/`, `models/`, `prompts/`, `outputs/`, `docs/`); journal and meeting log created; talking points prepared for the supervisor meeting.
- Tue 20: supervisor meeting (thesis format and artefact, Wikipedia as data source, ethics route, use of published reports); literature search strategy and reference manager.
- Wed 21 - Thu 22: Wikipedia collection script (All-Ireland SFC 2021-2025) and parser (`matches.csv`, `scorers.csv`, data dictionary).
- Fri 23 - Sat 24: reading (data-to-text generation, hallucination, fact verification, LLM-as-a-judge); validation of 20 random matches against official sources; ethics form not required (confirmed 21 Oct).
- Sun 25: research questions and hypothesis fixed; introduction and literature review outline drafted.

### Done
- Repository reorganised; journal and meeting log in place.
- Supervisor questions rewritten for the 20 Oct meeting, with a new question on project depth.
- API access for the pilot model (OpenAI gpt-6.1-sol) set up and tested.
- Wikipedia collection, step 1: raw page text and revision ids saved for 2021-2024.
- Supervisor answers received by email (see `meetings.md`).
- Enquiry sent to Foireann about access to its open data API.
- Wikipedia collection, step 2: match parser and sum test (scorers must add up to the final score). 131 of 154 match boxes on the 2021-2024 season pages pass; every exclusion is logged with its reason.
- Pilot sample drawn: 10 matches at random (fixed seed) from the 131 that pass.

### Problems / decisions
- The meeting with the supervisor replaces the email planned in the roadmap for raising the priority A questions.
- Wikipedia page formats differ by year, and half-time scores exist in some years (2021, 2022) but not in others; the extraction has to handle several formats.
- No ethics form is needed (no human participants).
- Foireann API access requires a club administrator, so the pilot stays with Wikipedia while the enquiry is pending.
- Scope widened: any match with complete, documentable data is eligible, not only the All-Ireland knockout games. Inconsistent matches are excluded and logged.
- Matches that went to extra time or penalties are left out for now (possible use in the final report).
- The half-time score is present in only 5 of the 154 match boxes, so claims about the flow of a match are possible for very few matches.

### Next week
- To be filled on Sunday 25 Oct.

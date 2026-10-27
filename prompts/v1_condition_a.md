# Prompt v1, condition A (raw match data)

- Version: v1
- Condition: A, raw structured data (no pre-computed totals, winner or margin)
- Factual constraint: none (baseline)
- Used for: pilot, 10 matches (`pilot_inputs.json`, drawn with seed 2026)
- Model and parameters: recorded with every run (model id, timestamp, API parameters); not fixed in this file

## Message sent to the model

The text below is sent as a single user message. Placeholders in braces are filled from the match record.

```
Write a match report for the following Gaelic football match, in the style of a newspaper match report. Write about 250 words in English, with a headline.

Competition: All-Ireland Senior Football Championship {year}
Round: {round}
Date: {date}

{team1}: {score_team1}
{team2}: {score_team2}

Scores are written as goals-points.

Scorers for {team1}: {scorers_team1}
Scorers for {team2}: {scorers_team2}
```

## Input fields

| Placeholder | Source field in `pilot_inputs.json` |
|---|---|
| `{year}` | `year` |
| `{round}` | `round` |
| `{date}` | `date` |
| `{team1}`, `{team2}` | `team1`, `team2` |
| `{score_team1}`, `{score_team2}` | `score.team1`, `score.team2` |
| `{scorers_team1}`, `{scorers_team2}` | `scorers.team1`, `scorers.team2` (as written in the source, wiki markup removed) |

## Rationale

- Baseline condition: no instruction to avoid invention, so the errors that occur are the ones a plain request produces.
- The scoring notation is named but the conversion (1 goal = 3 points) is not given, so the winner and margin have to be calculated by the model.
- Venue, man of the match and match report links are not provided: they are outside the claim types kept after Gate 2 (final score, winner, scorers with totals, margin).

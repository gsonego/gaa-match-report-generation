# Validation of Wikipedia match data (20 matches)

Date: 26 Oct 2026. Data: `validation_games.xlsx` (same folder).

## Method

- Sample: 20 of the 131 matches that pass the sum test. Games 1-10 are the pilot matches (`pilot_games.csv`); games 11-20 are drawn with `random.Random(2027)` from the other 121.
- Each match was checked by hand against one independent source (RTE Sport), not the Wikipedia box.
- Fields checked: final score of each team, date, round, winner. Top scorer and total only for the 10 pilot matches.

## Results

- Score: 20/20 agree (0% disagreement). Date and winner: 20/20 agree.
- Round: 1/20 real disagreement (game 2: Wikipedia "Preliminary Round", RTE "First round"). Games 14, 15 and 19 are counted as not applicable: Wikipedia gives "Round N", RTE adds the group ("Round Robin Group X"), which is not a contradiction.
- Top scorer and total: 10/10 pilot matches agree with RTE.
- Draws (games 4 and 7): confirmed as final results.

## Limits

- Single independent source (RTE).
- With 0 disagreements in 20, the true rate is only bounded (about 15% at 95% confidence, rule of three).
- The sample is drawn after the sum test, so it describes the 131 included matches, not all 154.
- Scorer lists are not validated one by one; the sum test checks consistency with the score, and the top-scorer check covers the pilot matches only.
- The `round` field does not carry the group in the group stage.

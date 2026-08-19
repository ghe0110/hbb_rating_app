# Rating Engine v2.0

## Output
- Current Rating: recent-window oriented
- Historical Rating: all loaded data
- Live Rating: separate output for in-progress data

## Factor weights

Current:
- Win rate 25%
- Run differential/game 20%
- Inning stability 20%
- Participation 15%
- Advancement 10%
- Coach continuity 10%

Historical:
- Win rate 20%
- Run differential/game 15%
- Inning stability 20%
- Participation 15%
- Advancement 20%
- Coach continuity 10%

Each factor is converted to a 0-100 percentile among the schools in the same rating population.

## Small sample correction

Win percentage is shrunk toward .500:
`(wins + 1) / (games + 2)`

Current Rating additionally applies a confidence factor based on recent-year coverage and game count.

## Inning stability

The stability score penalizes:
- 3+ run innings
- 5+ run innings
- high maximum inning score
- late (7th inning onward) big innings

It rewards shutout innings.

This is intentionally transparent and can be replaced by a more sophisticated model later.

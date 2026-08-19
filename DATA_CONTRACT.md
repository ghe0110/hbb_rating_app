# Data contract

Required fields in `games.csv`:
`game_id,tournament_id,round,game_date,school_a_id,school_b_id,school_a_name,school_b_name,score_a,score_b,result`

Required fields in `inning_scores.csv`:
`game_id,school_id,school_name,inning,runs`

Required fields in `tournament_entries.csv`:
`tournament_id,school_id,school_name`

Optional:
`master/coaches.csv`

Do not put derived rating numbers into raw CSV. The engine calculates them.

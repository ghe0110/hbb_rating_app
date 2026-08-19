# Data Model

## 1. schools.csv

| field | meaning |
|---|---|
| school_id | 永続ID |
| school_name | 現在の表示名 |
| prefecture | 都道府県 |
| aliases | 旧校名等 |
| first_appearance_year | 初出場年 |

学校名変更に対応するため、表示名ではなく `school_id` を主キーにします。

## 2. tournaments.csv

| field | meaning |
|---|---|
| tournament_id | 大会ID |
| year | 年 |
| season | spring / summer |
| tournament_no | 大会回 |
| status | completed / live / planned |

## 3. games.csv

| field | meaning |
|---|---|
| game_id | 試合ID |
| tournament_id | 大会ID |
| round | 回戦 |
| school_a_id | 学校A |
| school_b_id | 学校B |
| score_a | 得点 |
| score_b | 得点 |
| result | 勝敗 |
| source_url | 出典 |

## 4. inning_scores.csv

1試合×1校×1イニング。

```text
game_id
school_id
inning
runs
```

延長は `10, 11, 12...` と整数で保持します。

## 5. coaches.csv

監督履歴。

```text
school_id
coach_name
start_year
end_year
```

## 6. pro_players.csv

主な出身プロ野球選手。

```text
school_id
player_name
pro_team
debut_year
```

## 7. rating_snapshots.csv

計算済みRatingの保存。

```text
snapshot_date
rating_type
school_id
rating
rank
confidence
```

これにより、将来Ratingロジックを変更しても過去のランキングを比較できます。

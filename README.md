# Koshien Rating 追加データファイル v1.1

既存のGitHubリポジトリへ追加するためのCSVテンプレートです。

## 大会データ
大会ごとに以下へ追加します。

- `raw/YYYY_spring/games.csv`
- `raw/YYYY_spring/inning_scores.csv`
- `raw/YYYY_spring/tournament_entries.csv`
- `raw/YYYY_summer/...`

## マスターデータ
- `master/coaches.csv`
- `master/pro_players.csv`

## 入力ルール
1. `school_id` は既存の学校IDを使用。
2. 新しい高校は `data/master/schools.csv` に先に登録。
3. `tournament_id` は `SP2026` / `SU2026` の形式。
4. 得点は整数。
5. 延長は `inning=10,11,12...`。
6. `source_url` を必ず記録。
7. 未確認データを推測で埋めない。

## 試合CSVの例

```csv
game_id,tournament_id,round,game_date,school_a_id,school_b_id,score_a,score_b,result,source_url
G2026SU001,SU2026,1回戦,2026-08-06,S001,S002,5,3,A_WIN,https://example.com
```

上記は入力形式の例であり、実在試合データではありません。

# データ追加手順

## 大会を1つ追加する場合

### Step 1

`data/raw/` にCSVを追加。

例：

```text
data/raw/2026_summer_games.csv
data/raw/2026_summer_innings.csv
```

### Step 2

正規化。

```bash
python scripts/normalize.py data/raw/2026_summer_games.csv
```

### Step 3

検証。

```bash
python scripts/validate.py
```

エラーがあればRating計算を停止します。

### Step 4

Rating生成。

```bash
python scripts/build_rating.py
```

### Step 5

GitHubへcommit。

```bash
git add data/
git commit -m "Add 2026 summer tournament data"
git push
```

## 原則

- 未確認データを推測で埋めない
- 出典URLを保持する
- 学校名を直接IDとして使わない
- 過去データを上書きしない
- 大会追加はappend中心
- Ratingはデータから再生成可能にする

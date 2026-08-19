# Rating Specification v1.0

## Historical Rating

歴代実績を評価。

- Win Rate: 25
- Run Differential: 20
- Inning Stability: 20
- Appearance: 15
- Coach Continuity: 10
- Championship / Deep Run: 10

## Current Rating

直近5年間を基本母集団とする。

- Win Rate: 30
- Run Differential: 25
- Inning Stability: 20
- Recent Tournament Performance: 10
- Appearance: 5
- Coach Continuity: 5
- Championship / Deep Run: 5

### Time Decay

直近の大会ほど重くする。

初期仕様：

- 0〜1年前: 1.00
- 2年前: 0.75
- 3年前: 0.55
- 4年前: 0.35
- 5年前: 0.20

### Spring / Summer

Current Ratingは夏60%、春40%を基本値とする。

## Confidence

試合数が少ない高校を過大評価しないための信頼度。

正式なBayesian / shrinkage方式は全データ投入後に決定する。

## Live Rating

開催中大会の終了済み試合のみを暫定反映。

大会終了後にCurrent Ratingへ確定反映する。

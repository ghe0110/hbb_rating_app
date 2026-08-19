# Koshien Rating

全国高校野球の「Historical / Current / Live Rating」を公開・更新するためのGitHub Pages対応プロジェクトです。

## 基本方針

**最初から全歴代データをGitHubへ詰め込みません。**

アプリ本体・データ仕様・計算ロジックを先に公開し、データは年度・大会単位で追加します。

- `Historical Rating`：歴代甲子園実績
- `Current Rating`：直近5年間を中心とした現在の勢力
- `Live Rating`：開催中大会を反映する暫定値

## ディレクトリ

```text
data/
  master/       学校・大会・監督などのマスタ
  raw/          収集した原データ
  processed/    正規化済みデータ
  current/      Current/Live用集計
  historical/   Historical用集計
src/            ブラウザ側アプリ
scripts/        データ投入・検証・集計スクリプト
docs/           データ仕様・更新手順
tests/          データ検証
```

## データ追加の考え方

新しい大会を追加するときは、

1. `data/raw/` に元データを置く
2. `scripts/normalize.py` で正規化
3. `scripts/validate.py` で検証
4. `scripts/build_rating.py` でRatingを再計算
5. `data/processed/` とランキングを更新
6. GitHubへcommit / push

という流れにします。

**アプリ本体を変更せず、データだけ追加できます。**

## 最初の公開版

初期状態ではデータを最小限にしています。

- 学校マスタのサンプル
- 大会マスタ
- 試合データのサンプル
- イニングデータのサンプル
- Rating仕様
- データ検証ルール
- GitHub Pages用UI

データが増えてもUIのコードは基本的に変更不要です。

## GitHub Pages

GitHub Actionsで `data/` を読み込み、静的サイトを生成する方式を想定しています。

サーバー・DBは必須ではありません。

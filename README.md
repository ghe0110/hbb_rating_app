# Koshien Rating Engine v2.0

GitHubに登録して「データを追加 → 計算 → JSON更新 → Pages表示」まで動かすためのエンジンです。

## 最短手順

```bash
python scripts/validate.py
python scripts/build_rating.py
```

その後、生成されたJSONをGitHubへpushしてください。

## 注意
このv2.0は「計算が実際に動くこと」を優先した透明なベースモデルです。
今後、歴代データを増やしながら重み・補正・監督継続率・Live計算を精緻化できます。

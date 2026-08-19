import csv
from pathlib import Path

errors=[]
games=Path("data/processed/games.csv")
with games.open(encoding="utf-8-sig") as f:
    rows=list(csv.DictReader(f))

for r in rows:
    if not r["game_id"] or not r["school_a_id"] or not r["school_b_id"]:
        errors.append(f"missing id: {r}")
    if r["school_a_id"]==r["school_b_id"]:
        errors.append(f"same school: {r['game_id']}")

if errors:
    for e in errors: print("ERROR",e)
    raise SystemExit(1)

print(f"OK: {len(rows)} games")

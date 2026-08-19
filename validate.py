#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv, os, sys

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")

def read(path):
    if not os.path.exists(path): return []
    with open(path,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))

games=[]; innings=[]; entries=[]
for base,_,files in os.walk(os.path.join(DATA,"raw")):
    for fn in files:
        p=os.path.join(base,fn)
        if fn=="games.csv": games+=read(p)
        elif fn=="inning_scores.csv": innings+=read(p)
        elif fn=="tournament_entries.csv": entries+=read(p)

errors=[]
game_ids=set()
for g in games:
    gid=g.get("game_id","")
    if not gid or gid in game_ids: errors.append(f"duplicate/empty game_id: {gid}")
    game_ids.add(gid)
    try:
        a=float(g["score_a"]); b=float(g["score_b"])
        if a<0 or b<0: errors.append(f"negative score: {gid}")
    except: errors.append(f"bad score: {gid}")

inning_game_ids={r.get("game_id") for r in innings}
missing=[gid for gid in game_ids if gid not in inning_game_ids]
if missing: print("WARNING: no inning data for",len(missing),"games")

entry_keys={(e.get("tournament_id"),e.get("school_id")) for e in entries}
for g in games:
    for k in ["school_a_id","school_b_id"]:
        key=(g.get("tournament_id"),g.get(k))
        if key not in entry_keys:
            errors.append(f"school not registered in tournament: {key}")

if errors:
    print("\n".join("ERROR: "+e for e in errors))
    sys.exit(1)
print(f"OK: {len(games)} games, {len(innings)} inning rows, {len(entries)} entries")

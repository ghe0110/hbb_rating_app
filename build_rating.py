#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Koshien Rating Engine v2.0
- Reads normalized game / inning / coach / tournament data.
- Produces Current, Historical, and Live rating JSON.
- Uses percentile-based factor scores so adding more schools does not
  depend on arbitrary raw scales.
- Current Rating emphasizes recent tournaments.
"""

from __future__ import annotations
import csv, json, math, os, sys
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

WEIGHTS_CURRENT = {
    "win_rate": 25.0,
    "run_diff": 20.0,
    "inning_stability": 20.0,
    "participation": 15.0,
    "advancement": 10.0,
    "coach_continuity": 10.0,
}
WEIGHTS_HISTORICAL = {
    "win_rate": 20.0,
    "run_diff": 15.0,
    "inning_stability": 20.0,
    "participation": 15.0,
    "advancement": 20.0,
    "coach_continuity": 10.0,
}

# Current rating: recent 5 calendar years, exponential decay.
CURRENT_YEARS = 5
DECAY = 0.78

ROUND_VALUE = {
    "1回戦": 1, "2回戦": 2, "3回戦": 3,
    "準々決勝": 4, "準決勝": 5, "決勝": 6,
}

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def parse_year(s):
    try:
        return int(str(s)[:4])
    except Exception:
        return None

def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default

def percentile(values, higher_is_better=True):
    """Return 0-100 percentile ranks. Equal values receive their midpoint rank."""
    clean = sorted(set(v for v in values if v is not None))
    if not clean:
        return {}
    if len(clean) == 1:
        return {clean[0]: 50.0}
    out = {}
    n = len(clean)
    for i, v in enumerate(clean):
        p = 100.0 * i / (n - 1)
        out[v] = p if higher_is_better else 100.0 - p
    return out

def shrink_win_pct(wins, games):
    # Small samples are pulled toward .500.
    return (wins + 2.0 * 0.5) / (games + 2.0)

def stability_score(inning_values):
    """
    100 = very stable, 0 = very unstable.
    Components:
      - big-innings frequency (3+ runs)
      - disaster-innings frequency (5+)
      - maximum inning runs
      - late collapse (7th inning onward)
      - shutout inning ratio
    """
    if not inning_values:
        return 50.0
    vals = list(inning_values)
    n = len(vals)
    big = sum(v >= 3 for v in vals) / n
    disaster = sum(v >= 5 for v in vals) / n
    max_run = max(vals)
    late = [v for i, v in enumerate(vals, 1) if i >= 7]
    late_big = sum(v >= 3 for v in late) / len(late) if late else 0.0
    shutout = sum(v == 0 for v in vals) / n

    score = (
        100
        - big * 45
        - disaster * 35
        - min(max_run, 10) * 2.5
        - late_big * 20
        + shutout * 15
    )
    return max(0.0, min(100.0, score))

def load_all():
    games, innings, entries, coaches = [], [], [], []
    for base, _, files in os.walk(os.path.join(DATA, "raw")):
        for fn in files:
            if fn == "games.csv":
                games += read_csv(os.path.join(base, fn))
            elif fn == "inning_scores.csv":
                innings += read_csv(os.path.join(base, fn))
            elif fn == "tournament_entries.csv":
                entries += read_csv(os.path.join(base, fn))
    coaches = read_csv(os.path.join(DATA, "master", "coaches.csv"))
    return games, innings, entries, coaches

def build_school_stats(games, innings, entries, coaches):
    stats = defaultdict(lambda: {
        "games":0, "wins":0, "losses":0, "runs_for":0.0, "runs_against":0.0,
        "tournaments":set(), "round_values":[], "innings":[],
        "spring_games":0, "summer_games":0, "years":set()
    })
    names = {}

    for e in entries:
        sid = e.get("school_id","").strip()
        if not sid: continue
        names[sid] = e.get("school_name","").strip() or sid
        tid = e.get("tournament_id","").strip()
        if tid:
            stats[sid]["tournaments"].add(tid)
        y = parse_year(tid)
        if y: stats[sid]["years"].add(y)

    for g in games:
        sid_a, sid_b = g.get("school_a_id",""), g.get("school_b_id","")
        if not sid_a or not sid_b: continue
        for sid, name, rf, ra, win in [
            (sid_a, g.get("school_a_name",""), safe_float(g.get("score_a")), safe_float(g.get("score_b")),
             safe_float(g.get("score_a")) > safe_float(g.get("score_b"))),
            (sid_b, g.get("school_b_name",""), safe_float(g.get("score_b")), safe_float(g.get("score_a")),
             safe_float(g.get("score_b")) > safe_float(g.get("score_a"))),
        ]:
            names[sid] = name or names.get(sid, sid)
            s = stats[sid]
            s["games"] += 1
            s["wins"] += int(win)
            s["losses"] += int(rf < ra)
            s["runs_for"] += rf
            s["runs_against"] += ra
            tid = g.get("tournament_id","")
            if tid: s["tournaments"].add(tid)
            y = parse_year(g.get("game_date",""))
            if y: s["years"].add(y)
            if "spring" in tid.lower() or tid.startswith("SP"):
                s["spring_games"] += 1
            if "summer" in tid.lower() or tid.startswith("SU"):
                s["summer_games"] += 1
            s["round_values"].append(ROUND_VALUE.get(g.get("round",""), 0))

    for row in innings:
        sid = row.get("school_id","")
        if sid:
            stats[sid]["innings"].append(safe_float(row.get("runs")))

    # Coach continuity: ratio of time covered by the most recent coach among known coach records.
    coach_by_school = defaultdict(list)
    for c in coaches:
        sid = c.get("school_id","")
        if sid: coach_by_school[sid].append(c)

    out = {}
    for sid, s in stats.items():
        games_n = s["games"]
        years = sorted(s["years"])
        coach_cont = 0.5
        if coach_by_school[sid]:
            spans=[]
            for c in coach_by_school[sid]:
                a=parse_year(c.get("start_year")); b=parse_year(c.get("end_year")) or (max(years) if years else a)
                if a and b and b>=a: spans.append(b-a+1)
            if spans:
                coach_cont = min(1.0, max(spans) / max(1, (max(years)-min(years)+1 if len(years)>1 else max(spans))))

        out[sid] = {
            "school_id": sid,
            "school_name": names.get(sid, sid),
            "games": games_n,
            "wins": s["wins"],
            "losses": s["losses"],
            "win_rate": shrink_win_pct(s["wins"], games_n) if games_n else 0.5,
            "run_diff_per_game": ((s["runs_for"]-s["runs_against"])/games_n if games_n else 0.0),
            "participation": len(s["tournaments"]),
            "advancement": (sum(s["round_values"])/len(s["round_values"]) if s["round_values"] else 0.0),
            "inning_stability": stability_score(s["innings"]),
            "coach_continuity": coach_cont,
            "spring_games": s["spring_games"],
            "summer_games": s["summer_games"],
            "years": years,
        }
    return out

def current_filter(stats):
    if not stats: return {}
    latest=max((max(s["years"]) if s["years"] else 0) for s in stats.values())
    cutoff=latest-CURRENT_YEARS+1
    # This engine's source data is already tournament-level. For a strict
    # five-year Current Rating, games outside the window should be filtered
    # upstream in a future per-game implementation. Here we apply a confidence
    # multiplier based on how many recent years are represented.
    out={}
    for sid,s in stats.items():
        recent_years=sum(1 for y in s["years"] if y>=cutoff)
        if recent_years>0:
            x=dict(s)
            x["recent_year_coverage"]=recent_years/CURRENT_YEARS
            x["current_confidence"]=min(1.0, 0.45+0.55*x["recent_year_coverage"])
            out[sid]=x
    return out

def make_ratings(stats, mode):
    if not stats: return []
    weights=WEIGHTS_CURRENT if mode=="current" else WEIGHTS_HISTORICAL
    factor_fields={
        "win_rate":"win_rate",
        "run_diff":"run_diff_per_game",
        "inning_stability":"inning_stability",
        "participation":"participation",
        "advancement":"advancement",
        "coach_continuity":"coach_continuity",
    }
    pctmaps={}
    for factor,field in factor_fields.items():
        vals=[s[field] for s in stats.values()]
        pctmaps[factor]=percentile(vals)

    rows=[]
    for sid,s in stats.items():
        factors={f:round(pctmaps[f].get(s[field],50.0),2) for f,field in factor_fields.items()}
        raw=sum(factors[f]*weights[f]/100 for f in weights)
        confidence=1.0
        if mode=="current":
            confidence=s.get("current_confidence",1.0)
            # Small sample protection.
            confidence *= min(1.0, 0.70 + 0.30*min(s["games"],10)/10)
        rating=50.0+(raw-50.0)*confidence
        rows.append({
            **s,
            "rating":round(max(0.0,min(100.0,rating)),2),
            "factors":factors,
            "confidence":round(confidence,3),
            "mode":mode,
        })
    rows.sort(key=lambda x:(x["rating"],x["wins"],x["run_diff_per_game"]), reverse=True)
    for i,r in enumerate(rows,1): r["rank"]=i
    return rows

def write_json(path, payload):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(payload,f,ensure_ascii=False,indent=2)

def main():
    games, innings, entries, coaches=load_all()
    stats=build_school_stats(games,innings,entries,coaches)
    current=make_ratings(current_filter(stats),"current")
    historical=make_ratings(stats,"historical")

    # Live uses the same engine but is intentionally separate so an in-progress
    # tournament can be replaced without changing Current/Historical.
    live=current

    meta={
        "engine_version":"2.0",
        "generated_on":date.today().isoformat(),
        "current_window_years":CURRENT_YEARS,
        "weights_current":WEIGHTS_CURRENT,
        "weights_historical":WEIGHTS_HISTORICAL,
        "source_counts":{"games":len(games),"inning_rows":len(innings),"entries":len(entries),"schools":len(stats)}
    }
    write_json(os.path.join(DATA,"current","current_rating.json"),{"meta":meta,"rankings":current})
    write_json(os.path.join(DATA,"historical","historical_rating.json"),{"meta":meta,"rankings":historical})
    write_json(os.path.join(DATA,"current","live_rating.json"),{"meta":{**meta,"mode":"live"},"rankings":live})
    print(f"Generated: {len(current)} current / {len(historical)} historical schools")

if __name__=="__main__":
    main()

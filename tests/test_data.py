import csv

def test_school_ids_unique():
    with open("data/master/schools.csv", encoding="utf-8-sig") as f:
        rows=list(csv.DictReader(f))
    ids=[r["school_id"] for r in rows]
    assert len(ids)==len(set(ids))

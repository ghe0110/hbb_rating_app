import csv, sys
from pathlib import Path

if len(sys.argv) < 2:
    raise SystemExit("usage: python scripts/normalize.py <raw_csv>")

src=Path(sys.argv[1])
print(f"[normalize] input={src}")
print("Implement source-specific normalization here.")

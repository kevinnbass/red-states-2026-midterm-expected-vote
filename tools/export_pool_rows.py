"""Export the president's-party pool rows for one state, for repositories that compute that state on their own
(texas-2026-midterm-expected-vote reads them as data/pool/pool_rows_TX.csv).

The rows are exactly expected.pool_all(<inputs>, <ST>, <inputs>/pool50): office-year ratios of every other source in the
50-state pool. The state's own 2026-ballot offices are not included (the state's own model supplies them).
usage: export_pool_rows.py <inputs_dir> <ST> <out_csv>
"""
import csv, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import expected  # noqa: E402

inputs, st, out = sys.argv[1:4]
rows, info = expected.pool_all(inputs, st, os.path.join(inputs, "pool50"))
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["office", "year", "ratio_rep", "ratio_dem"])
    for r in sorted(rows, key=lambda r: (r["office"], r["year"])):
        w.writerow([r["office"], r["year"], repr(r["ratio_rep"]), repr(r["ratio_dem"])])
json.dump(info, open(os.path.splitext(out)[0] + "_info.json", "w"), indent=1)
print(f"{len(rows)} rows, {info['office_groups']} office groups, {info['states']} states")

"""50-state inputs for the president's-party pooling comparison.

Writes to <out_dir>:
  pres50.csv     R and D presidential votes by state, 1992-2024 (MEDSL "U.S. President 1976-2024", party_simplified)
  senate50.csv   U.S. Senate general elections in the midterm years 1994-2022, every state (MEDSL "U.S. Senate statewide
                 1976-2024"): R and D votes per race. Where a party has several candidates in one race (top-two, top-four,
                 Louisiana's November open primary) their votes are summed and the row is flagged. Mississippi's 2018 special
                 is left out (MEDSL holds only its Nov. 27 runoff). Races without both an R and a D are kept with a blank side.
  governors50.csv (not built here) comes from tools/governors50 notes: Wikipedia election boxes for every midterm-year governor
                 race 1994-2022, cross-checked against official state files and MEDSL 2018/2022 precinct files (see its README).
usage: pool_inputs.py <out_dir> [<raw_dir>]   (repo: python3 tools/pool_inputs.py data/inputs/pool50 data/raw/shared-as-results)
"""
import csv, os, re, subprocess, sys
from collections import defaultdict

E = sys.argv[2] if len(sys.argv) > 2 else "/mnt/data/projects/election/raw"  # folder holding results/president and results/senate
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
MID = [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]

# presidential
agg = defaultdict(lambda: [0, 0])
for r in csv.DictReader(open(f"{E}/results/president/1976-2024-president.csv")):
    y = int(r["year"])
    if y >= 1992 and r["party_simplified"] in ("REPUBLICAN", "DEMOCRAT"):
        agg[(r["state_po"], y)][0 if r["party_simplified"] == "REPUBLICAN" else 1] += int(r["candidatevotes"])
with open(f"{OUT}/pres50.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["state", "year", "rep_votes", "dem_votes"])
    for (s, y), (a, b) in sorted(agg.items()):
        w.writerow([s, y, a, b])

# Senate
races = defaultdict(lambda: {"R": [], "D": [], "tot": 0})
for r in csv.DictReader(open(f"{E}/results/senate/1976-2024-senate-state.tab")):
    y = int(r["year"])
    if y not in MID or r["stage"].strip().lower() != "gen":
        continue
    sp = r["special"] == "True"
    if (r["state_po"], y, sp) == ("MS", 2018, True):
        continue
    k = (r["state_po"], y, sp)
    races[k]["tot"] = int(float(r["totalvotes"]))
    p = {"REPUBLICAN": "R", "DEMOCRAT": "D"}.get(r["party_simplified"])
    if p:
        races[k][p].append((r["candidate"], int(float(r["candidatevotes"]))))
with open(f"{OUT}/senate50.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["state", "year", "special", "rep_votes", "dem_votes", "total_votes", "n_rep_cands", "n_dem_cands", "top_other_share", "notes"])
    for (s, y, sp), v in sorted(races.items()):
        rv = sum(x[1] for x in v["R"]) if v["R"] else ""
        dv = sum(x[1] for x in v["D"]) if v["D"] else ""
        other = v["tot"] - (rv or 0) - (dv or 0)
        note = "several candidates of one party summed" if len(v["R"]) > 1 or len(v["D"]) > 1 else ""
        w.writerow([s, y, int(sp), rv, dv, v["tot"], len(v["R"]), len(v["D"]), round(other / v["tot"], 4) if v["tot"] else "", note])

print("pres50 rows", len(agg), "| senate50 races", len(races))

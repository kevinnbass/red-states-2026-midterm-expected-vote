"""Collect this repository's data from the analysis folders (run once by the maintainer; kept for transparency).

- data/inputs/: presidential_1992_2024.csv and <ST>/statewide_results.csv + README.md (the contract files expected.py reads).
- data/raw/<ST>/: every downloaded source file of 10 MB or less, as fetched (provenance.csv lists them all).
- data/raw/shared/: AP results feeds and MIT Election Data and Science Lab files used by several states.
- data/SOURCES.csv: one row per source file: repo path (blank when not copied because of size), URL, fetch time, bytes, sha256.
  Files over 10 MB are listed with their URL and sha256 so they can be fetched again and checked (src/fetch_sources.py).
usage: assemble_repo.py <repo_root>
"""
import csv, hashlib, os, shutil, sys

ROOT = sys.argv[1]
E = "/mnt/data/projects/election"
STATES = ["OH", "KS", "IA", "AK", "MS", "SC", "IN", "TX"]
LIMIT = 10 * 1024 * 1024
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rows = []


def put(src, rel, url, utc="", what=""):
    b = os.path.getsize(src)
    h = sha(src)
    if b <= LIMIT:
        dst = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        path = rel
    else:
        path = ""
    rows.append({"file": path, "name": os.path.basename(rel), "url": url, "fetched_utc": utc, "bytes": b, "sha256": h, "what": what})


# contract inputs
inp = os.path.join(ROOT, "data", "inputs")
os.makedirs(inp, exist_ok=True)
shutil.copy2(f"{E}/derived/states_expected/presidential_1992_2024.csv", inp)
for st in STATES:
    d = f"{E}/derived/states_expected/{st}"
    os.makedirs(os.path.join(inp, st), exist_ok=True)
    for f in ("statewide_results.csv", "README.md", "statewide_results_helper.csv"):
        if os.path.exists(os.path.join(d, f)):
            shutil.copy2(os.path.join(d, f), os.path.join(inp, st, f))
# per-state raw downloads
for st in STATES[:-1]:
    d = f"{E}/raw/states_history/{st}"
    prov = {}
    if os.path.exists(f"{d}/provenance.csv"):
        for r in csv.DictReader(open(f"{d}/provenance.csv")):
            prov[r["file"]] = r
    for dirpath, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, d)
            pr = prov.get(rel) or prov.get(f) or {}
            if pr.get("http") and pr["http"] not in ("200", ""):
                continue  # error pages kept on disk are not sources
            put(p, f"data/raw/{st}/{rel}", pr.get("url", ""), pr.get("utc", ""), f"{st} source file")
# shared
for p, url, what in [
    (f"{E}/raw/results/president/1976-2024-president.csv", "https://doi.org/10.7910/DVN/42MVDX", "MIT Election Data and Science Lab, U.S. President 1976-2024"),
    (f"{E}/raw/results/senate/1976-2024-senate-state.tab", "https://doi.org/10.7910/DVN/PEJ5QU", "MIT Election Data and Science Lab, U.S. Senate statewide 1976-2024 (comma-separated)"),
    (f"{E}/raw/results/gov2022/x/ks22_cleaned.csv", "https://github.com/MEDSL/2022-elections-official", "MIT Election Data and Science Lab 2022 precinct returns, Kansas"),
    (f"{E}/raw/results/clerk/statistics2002.pdf", "https://clerk.house.gov/member_info/electionInfo/2002election.pdf", "House Clerk, Statistics of the Congressional Election of Nov. 5, 2002 (South Carolina check)"),
]:
    put(p, f"data/raw/shared/{os.path.basename(p)}", url, "", what)
for d, tag in ((f"{E}/raw/ap_npr_20261108T0505Z/states", "ap_npr_20261108T0505Z"), (f"{E}/raw/ap_npr_states_20261108", "ap_npr_20261108T0426Z")):
    for f in sorted(os.listdir(d)):
        if f.endswith(".json"):
            put(os.path.join(d, f), f"data/raw/shared/{tag}/{f}", f"https://apps.npr.org/2026-election-results/data/states/{f}", "",
                "AP results via NPR's election feed (unofficial)")
# governor races 1994-2022 (Wikipedia pages as fetched, for the 50-state pool)
gd = f"{E}/raw/gov50_wikipedia_20261108"
gprov = {r["file"]: r for r in csv.DictReader(open(f"{gd}/provenance.csv"))}
for f in sorted(os.listdir(gd)):
    pr = gprov.get(f, {})
    if f == "provenance.csv" or (pr.get("http") and pr["http"] != "200"):
        continue
    put(os.path.join(gd, f), f"data/raw/shared/gov50_wikipedia/{f}", pr.get("url", ""), pr.get("utc", ""), "Wikipedia governor election page (wikitext)")
with open(os.path.join(ROOT, "data", "SOURCES.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["file", "name", "url", "fetched_utc", "bytes", "sha256", "what"])
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} sources; copied {sum(1 for r in rows if r['file'])}; listed only (over 10 MB) {sum(1 for r in rows if not r['file'])}; "
      f"copied bytes {sum(r['bytes'] for r in rows if r['file']):,}")

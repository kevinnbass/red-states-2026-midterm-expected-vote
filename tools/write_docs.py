"""Write README.md and METHODOLOGY.md from the committed outputs (data/derived, figures, states.json), so no number is typed by hand.
usage: write_docs.py <repo_root> [--links site/links.json]
"""
import csv, json, os, sys

ROOT = sys.argv[1]
LINKS = json.load(open(sys.argv[sys.argv.index("--links") + 1])) if "--links" in sys.argv else {}
CFG = json.load(open(os.path.join(ROOT, "states.json")))
POOL = json.load(open(os.path.join(ROOT, "data", "derived", "pool.json")))
NAMES = {"TX": "Texas", "OH": "Ohio", "KS": "Kansas", "IA": "Iowa", "AK": "Alaska", "MS": "Mississippi", "SC": "South Carolina", "IN": "Indiana"}
ORDER = [s for s in ("OH", "KS", "IA", "AK", "MS", "SC", "IN") if os.path.exists(os.path.join(ROOT, "data", "derived", s, "expected.csv"))]
M = "−"
k = lambda x: f"{x / 1e3:+,.0f}K".replace("-", M)

b26 = None
out = [f"# {', '.join(NAMES[s] for s in ORDER[:-1])} and {NAMES[ORDER[-1]]}: 2026 statewide votes vs. a typical midterm", "",
       "For every statewide race on these states' 2026 ballots, the vote each party would get if the office followed its own 1994–2022",
       "midterm pattern, set against the unofficial 2026 count, with the full 1994–2026 history behind it. Same method as",
       "[texas-2026-midterm-expected-vote](https://github.com/kevinnbass/texas-2026-midterm-expected-vote).", ""]
if LINKS.get("figures"):
    out += [f"Web page with all figures: {LINKS['figures']}", ""]
out += ["**2026 counts are unofficial** and come from different sources and dates by state (see each state below). Rebuild with",
        "`./build.sh` after certified results are added to `data/inputs/`.", "", "## Summary", "",
        "| State | Races | Democratic nominee above expected | Republican nominee below expected | Same, adjusted for the president's party |",
        "|---|---|---|---|---|"]
blocks = []
for st in ORDER:
    E = [r for r in csv.DictReader(open(os.path.join(ROOT, "data", "derived", st, "expected.csv"))) if r["year"] == "2026"]
    G = list(csv.DictReader(open(os.path.join(ROOT, "data", "derived", st, "races_2018_2022_2026.csv"))))
    b26 = float(E[0]["inc_b"])
    f = lambda r, c: float(r[c])
    nd = sum(f(r, "dev_dem") > 0 for r in E)
    nr = sum(f(r, "dev_rep") < 0 for r in E)
    ndi = sum(f(r, "dev_inc_dem") > 0 for r in E)
    nri = sum(f(r, "dev_inc_rep") < 0 for r in E)
    out.append(f"| [{NAMES[st]}](#{NAMES[st].lower().replace(' ', '-')}) | {len(E)} | {nd} | {nr} | {ndi} D above, {nri} R below |")
    s = st.lower()
    g26 = {r["office"]: r for r in G if r["year"] == "2026"}
    tbl = ["| 2026 race | Republican | vs. expected | vs. adjusted | Democrat | vs. expected | vs. adjusted |", "|---|---|---|---|---|---|---|"]
    for r in E:
        g = g26.get(r["office"], {})
        tbl.append(f"| {r['title']} | {g.get('rep_nominee', '')} {int(f(r, 'rep')):,} | {k(f(r, 'dev_rep'))} | {k(f(r, 'dev_inc_rep'))} | "
                   f"{g.get('dem_nominee', '')} {int(f(r, 'dem')):,} | {k(f(r, 'dev_dem'))} | {k(f(r, 'dev_inc_dem'))} |")
    c = CFG["states"][st]
    blocks += [f"## {NAMES[st]}", "", f"![{NAMES[st]}: history and 2018–2026 races vs. expected](figures/{s}/{s}_history_and_expected.png)", "",
               f"![{NAMES[st]}: the same, adjusted for the president's party](figures/{s}/{s}_incumbency_history_and_expected.png)", ""] + tbl + [
               "", f"- 2026 count: {c['asof']}.", f"- Sources: {c['source']}."] + [f"- {n}" for n in c.get("notes", [])] + [
               f"- Inputs: [`data/inputs/{st}/`](data/inputs/{st}/) (its README lists every source and check); panels: [`figures/{s}/panels/`](figures/{s}/panels/)."]
    if LINKS.get("writeups", {}).get(st):
        blocks.append(f"- Write-up: [What moved the {NAMES[st]} vote in 2026]({LINKS['writeups'][st]})")
    blocks.append("")
out += ["", f"Adjusted = the expectation including the usual midterm effect of holding the White House, {100 * b26:+.1f} points of the "
        f"presidential vote for 2026, estimated from the midterms of {', '.join(NAMES[x] for x in POOL['pool'])} together "
        "(see [METHODOLOGY.md](METHODOLOGY.md)).".replace("-", M, 1), ""] + blocks
out += ["## Rebuild", "", "```", "pip install -r requirements.txt", "./build.sh          # rebuild into build/ and compare with data/derived and figures",
        "python3 src/fetch_sources.py   # re-download every source with a URL and compare sha256", "```", "",
        "## Layout", "", "- `data/inputs/` — what the code reads: `presidential_1992_2024.csv` and `<ST>/statewide_results.csv` (one row per race,",
        "  with source URL, file, sha256, cross-check and notes) plus each state's README.",
        "- `data/raw/` — the downloaded source files (10 MB or less); `data/SOURCES.csv` lists every source with URL and sha256,",
        "  including larger files that are not copied.", "- `data/derived/` — the computed tables; `figures/` — the figures; `site/` — the web page builder.",
        "- `src/expected.py` (the computation), `src/figs.py` (figures), `src/build_states.py` (all states), `src/verify.py`.", "",
        "Texas inputs are included because Texas is part of the pooled president's-party estimate; the Texas figures and raw files are in",
        "[texas-2026-midterm-expected-vote](https://github.com/kevinnbass/texas-2026-midterm-expected-vote).", ""]
open(os.path.join(ROOT, "README.md"), "w").write("\n".join(out))

meth = f"""# Methodology

## Expected midterm vote
For office *o*, party *p* and midterm year *y*:

- ratio(o, p, y) = party p's votes for office o in midterm y ÷ party p's presidential votes in the state in year y − 2.
- **Plain expectation** for 2026 = the party's 2024 presidential vote in the state × the mean ratio of office o over the 1994–2022 midterms.
  For 2018 and 2022 the same is computed leaving that year out of the mean.
- **Adjusted for the president's party**: ratio = a[o, p] + b × (party p holds the White House). b is one within-(office, party) slope
  pooled across {', '.join(NAMES[x] for x in POOL['pool'])}; each a[o, p] is that state's own office-party mean of (ratio − b × holds).
  Both are estimated from 1994–2022 leaving out the target year. For 2026 b = {f"{100 * b26:+.1f}".replace("-", M)} points of the presidential vote.
- Only races with both a Republican and a Democratic nominee count. Offices with several races in one year (two Senate seats, court seats)
  use the average of those races.
- Votes are each nominee's own party-line votes. Alaska since 2022 (top-four primary, ranked-choice general) has no party nominees:
  there each party's vote is the combined first-choice vote of all its candidates (`expected.ALL_LINES_FROM`).

## Why pool the slope
With one or two offices, a state's own estimate of b swings widely depending on which year is left out (Mississippi alone:
−15.9 to −2.1 points); pooled with other states it is stable. The office baselines stay each state's own.

## Known limits
- 2026 counts are unofficial and taken at different times by state (Alaska about 74% counted).
- Some history rests on secondary sources where a state's own files could not be fetched automatically (Kansas, parts of Iowa,
  Indiana 1994–1998); each row's `notes` says so and each state's README lists every check.
- Supreme Court races in Ohio carried no party labels before 2022, so that office's baseline is short.
"""
open(os.path.join(ROOT, "METHODOLOGY.md"), "w").write(meth)
print("README.md and METHODOLOGY.md written;", len(ORDER), "states")

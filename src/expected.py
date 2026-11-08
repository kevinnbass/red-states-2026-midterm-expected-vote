"""Expected midterm vote for every statewide office on a state's 2026 ballot (any state).

Method (identical to the Texas analysis, github.com/kevinnbass/texas-2026-midterm-expected-vote):
  ratio(o, p, y)   = party p's vote for office o in midterm y / party p's presidential vote in the state in y - 2
  plain expected   = presidential vote two years earlier x mean ratio over the 1994-2022 midterms, leaving out year y
  president's-party expected = presidential vote x (a[o,p] + b * holds_white_house), with b the pooled within-(office, party)
                     slope and a the office-party mean of (ratio - b * holds), both estimated from 1994-2022 without year y.
Several races of one office in one year (court seats, a regular and a special Senate race) are averaged. Only races with both
a Republican and a Democratic nominee count.

Inputs: <inputs>/<ST>/statewide_results.csv (contract in README) and <inputs>/presidential_1992_2024.csv.
Usage: python3 expected.py <inputs_dir> <ST> <out_dir>  -> expected.csv, races_2018_2022_2026.csv
"""
import csv, os, re, statistics as st, sys

MIDTERMS = [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026]
PRES_PARTY = {1994: "D", 1998: "D", 2002: "R", 2006: "R", 2010: "D", 2014: "D", 2018: "R", 2022: "D", 2026: "R"}


# Alaska's top-four primary and ranked-choice general (from 2022) has no party nominees: several Republicans can be on the
# November ballot. From that year on, each party's vote is the combined first-choice vote of all its candidates.
ALL_LINES_FROM = {"AK": 2022}


def load(inputs, state):
    rows = [r for r in csv.DictReader(open(os.path.join(inputs, state, "statewide_results.csv")))
            if r["rep_votes"].strip() and r["dem_votes"].strip() and int(r["year"]) in MIDTERMS]
    for r in rows:
        if state in ALL_LINES_FROM and int(r["year"]) >= ALL_LINES_FROM[state]:
            for p, P in (("rep", "Republicans"), ("dem", "Democrats")):
                a = r.get(f"{p}_votes_all_lines", "").strip()
                if a and int(a) != int(r[f"{p}_votes"]):
                    r[f"{p}_votes"] = a
                    r[f"{p}_candidate"] = f"{r[p + '_candidate']} and other {P} (first choice)"
        r["year"], r["rep_votes"], r["dem_votes"] = int(r["year"]), int(r["rep_votes"]), int(r["dem_votes"])
    pres = {int(r["year"]): (int(r["rep_votes"]), int(r["dem_votes"]))
            for r in csv.DictReader(open(os.path.join(inputs, "presidential_1992_2024.csv"))) if r["state"] == state}
    return rows, pres


def one_party(inputs, state):
    """Midterm office-years of the 2026 offices whose race had only one major-party nominee (left out of the baselines)."""
    keys = {r["office_key"] for r in csv.DictReader(open(os.path.join(inputs, state, "statewide_results.csv"))) if r["year"] == "2026"}
    out = {}
    for r in csv.DictReader(open(os.path.join(inputs, state, "statewide_results.csv"))):
        y = int(r["year"])
        if r["office_key"] in keys and y in MIDTERMS and y <= 2022:
            rv, dv = r["rep_votes"].strip(), r["dem_votes"].strip()
            if bool(rv) != bool(dv):
                out.setdefault((r["office_key"], y), "no D nominee" if rv else "no R nominee")
            elif not rv and not dv and r.get("total_votes", "").strip():
                out.setdefault((r["office_key"], y), "nonpartisan")
    return out


def offices_2026(rows):
    seen, out = set(), []
    for r in rows:
        if r["year"] == 2026 and r["office_key"] not in seen:
            seen.add(r["office_key"])
            out.append((r["office_key"], r["office_title"]))
    return out


def build(rows, pres, pool_hist=None):
    E = []
    for key, title in offices_2026(rows):
        for y in MIDTERMS:
            rs = [r for r in rows if r["office_key"] == key and r["year"] == y]
            if not rs:
                continue
            pr, pd = pres[y - 2]
            rep, dem = st.mean(r["rep_votes"] for r in rs), st.mean(r["dem_votes"] for r in rs)
            E.append({"office": key, "title": title, "year": y, "rep": rep, "dem": dem, "n_races": len(rs),
                      "pres_rep": pr, "pres_dem": pd, "ratio_rep": rep / pr, "ratio_dem": dem / pd})
    for key, _ in offices_2026(rows):
        hist = [r for r in E if r["office"] == key and r["year"] <= 2022]
        for r in (x for x in E if x["office"] == key):
            base = [h for h in hist if h["year"] != r["year"]]
            r["n_hist"] = len(base)
            for p in ("rep", "dem"):
                if base:
                    avg = sum(h[f"ratio_{p}"] for h in base) / len(base)
                    r[f"avg_ratio_{p}"], r[f"expected_{p}"] = avg, r[f"pres_{p}"] * avg
                    r[f"dev_{p}"] = r[p] - r[f"expected_{p}"]
                else:
                    r[f"avg_ratio_{p}"] = r[f"expected_{p}"] = r[f"dev_{p}"] = None
    add_incumbency(E, pool_hist)
    return E


def add_incumbency(E, pool_hist=None):
    """pool_hist: optional office-year rows of other states (office keys prefixed by state); when given, the slope b is
    estimated from this state's and those states' groups together, while each office-party intercept stays this state's own."""
    for target in sorted({r["year"] for r in E}):
        hist = [r for r in E if r["year"] <= 2022 and r["year"] != target]
        groups = {}
        for r in hist:
            for p, P in (("rep", "R"), ("dem", "D")):
                groups.setdefault((r["office"], p), []).append((1 if PRES_PARTY[r["year"]] == P else 0, r[f"ratio_{p}"]))
        slope_groups = dict(groups)
        for r in (pool_hist or []):
            if r["year"] <= 2022 and r["year"] != target:
                for p, P in (("rep", "R"), ("dem", "D")):
                    slope_groups.setdefault((r["office"], p), []).append((1 if PRES_PARTY[r["year"]] == P else 0, r[f"ratio_{p}"]))
        num = den = 0.0
        for xs in slope_groups.values():
            mx = sum(x for x, _ in xs) / len(xs)
            my = sum(v for _, v in xs) / len(xs)
            num += sum((x - mx) * (v - my) for x, v in xs)
            den += sum((x - mx) ** 2 for x, _ in xs)
        b = num / den if den else None
        for r in (x for x in E if x["year"] == target):
            r["inc_b"] = b
            for p, P in (("rep", "R"), ("dem", "D")):
                xs = groups.get((r["office"], p))
                if b is None or not xs:
                    r[f"expected_inc_{p}"] = r[f"dev_inc_{p}"] = None
                    continue
                a = sum(v - b * x for x, v in xs) / len(xs)
                s = 1 if PRES_PARTY[target] == P else 0
                r[f"expected_inc_{p}"] = r[f"pres_{p}"] * (a + b * s)
                r[f"dev_inc_{p}"] = r[p] - r[f"expected_inc_{p}"]


def races_grid(rows):
    """Actual R/D votes for each 2026 race in 2018, 2022 and 2026 (2018/2022 = that office's races, averaged)."""
    out = []
    multi26 = {k for k, _ in offices_2026(rows) if sum(1 for r in rows if r["year"] == 2026 and r["office_key"] == k) > 1}
    for r26 in (r for r in rows if r["year"] == 2026):
        race = r26["race_name"] if r26["office_key"] in multi26 else r26["office_title"]
        race = re.sub(r"\s*\((?:special, )?[A-Z][a-z]{2}\.? \d{1,2}, \d{4}\)$", "", race)  # drop a trailing election date
        for y in (2018, 2022):
            rs = [r for r in rows if r["office_key"] == r26["office_key"] and r["year"] == y]
            if not rs:
                continue
            if len(rs) == 1:
                out.append({"race_2026": race, "office": r26["office_key"], "year": y, "rep_nominee": rs[0]["rep_candidate"],
                            "rep_votes": rs[0]["rep_votes"], "dem_nominee": rs[0]["dem_candidate"], "dem_votes": rs[0]["dem_votes"],
                            "basis": rs[0]["status"] + (" (secondary source)" if "SECONDARY" in rs[0].get("notes", "").upper() else "")})
            else:
                out.append({"race_2026": race, "office": r26["office_key"], "year": y, "rep_nominee": "", "rep_votes": round(st.mean(r["rep_votes"] for r in rs)),
                            "dem_nominee": "", "dem_votes": round(st.mean(r["dem_votes"] for r in rs)),
                            "basis": "average of " + ", ".join(r["race_name"] for r in rs)})
        out.append({"race_2026": race, "office": r26["office_key"], "year": 2026, "rep_nominee": r26["rep_candidate"], "rep_votes": r26["rep_votes"],
                    "dem_nominee": r26["dem_candidate"], "dem_votes": r26["dem_votes"], "basis": "unofficial"})
    return out


COLS = ["office", "title", "year", "n_races", "pres_rep", "pres_dem", "rep", "dem", "ratio_rep", "ratio_dem", "n_hist", "avg_ratio_rep",
        "avg_ratio_dem", "expected_rep", "expected_dem", "dev_rep", "dev_dem", "inc_b", "expected_inc_rep", "expected_inc_dem", "dev_inc_rep", "dev_inc_dem"]


def fmt(k, v):
    if v is None:
        return ""
    if isinstance(v, float):
        return round(v, 4) if ("ratio" in k or k == "inc_b") else round(v)
    return v


def main():
    inputs, state, out = sys.argv[1], sys.argv[2], sys.argv[3]
    pool = sys.argv[sys.argv.index("--pool") + 1].split(",") if "--pool" in sys.argv else []
    os.makedirs(out, exist_ok=True)
    rows, pres = load(inputs, state)
    pool_hist = []
    for other in pool:
        if other == state:
            continue
        orows, opres = load(inputs, other)
        for r in build(orows, opres):
            r["office"] = f"{other}:{r['office']}"
            pool_hist.append(r)
    E = build(rows, pres, pool_hist)
    with open(os.path.join(out, "expected.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in E:
            w.writerow({k: fmt(k, r.get(k)) for k in COLS})
    with open(os.path.join(out, "one_party_races.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["office", "year", "label"])
        w.writerows(sorted((k[0], k[1], v) for k, v in one_party(inputs, state).items()))
    G = races_grid(rows)
    with open(os.path.join(out, "races_2018_2022_2026.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["race_2026", "office", "year", "rep_nominee", "rep_votes", "dem_nominee", "dem_votes", "basis"])
        w.writeheader()
        w.writerows(G)
    print(f"{state}: {len(E)} office-years, {len({r['office'] for r in E})} offices, {len(G)} grid rows")


if __name__ == "__main__":
    main()

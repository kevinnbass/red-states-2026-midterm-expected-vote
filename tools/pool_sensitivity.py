"""How much does the choice of pool for the president's-party slope b change the adjusted 2026 results?

Pools (b is always estimated leaving out the target year; each office keeps its own state's baseline):
  own          the state alone, every statewide office in its 1994-2022 history (not only the offices on the 2026 ballot)
  published    the published version: the eight states, offices on each state's 2026 ballot
  eight_all    the eight states, every statewide office in their histories
  senate50     U.S. Senate races in all 50 states (MEDSL), plus the state's own offices
  gov50        governor races in all states (if governors50.csv is given), plus the state's own offices
  sen_gov50    Senate + governor races in all states, plus the state's own offices
  everything   Senate + governor races in all states, plus every statewide office of the eight states
Each pool also runs with races where a third candidate took 15% or more left out ("_no3rd").

usage: pool_sensitivity.py <inputs_dir> <pools_dir> <out_dir>
  inputs_dir: data/inputs (eight states' statewide_results.csv); pools_dir: pres50.csv, senate50.csv, governors50.csv if present
"everything" is the pool the published figures use (expected.pool_all); the script checks that its rows match exactly.
Writes b_by_pool.csv, races_by_pool.csv and summary.md.
"""
import csv, os, statistics as stt, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import expected as X  # noqa: E402

INP, POOLS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
GOV = os.path.join(POOLS, "governors50.csv") if os.path.exists(os.path.join(POOLS, "governors50.csv")) else None
os.makedirs(OUT, exist_ok=True)
EIGHT = ["TX", "OH", "KS", "IA", "AK", "MS", "SC", "IN"]
SHOW = ["OH", "KS", "IA", "AK", "MS", "SC", "IN", "TX"]
MID = [y for y in X.MIDTERMS if y <= 2022]

pres50 = {(r["state"], int(r["year"])): (int(r["rep_votes"]), int(r["dem_votes"])) for r in csv.DictReader(open(f"{POOLS}/pres50.csv"))}
MAIN = {"OH": "governor", "KS": "governor", "IA": "governor", "AK": "governor", "MS": "us_senate", "SC": "governor", "IN": "secretary_of_state",
        "TX": "governor"}


def hist_rows(state, office, races, third_cut=None):
    """office-year ratio rows from races [(year, rep, dem, other_share)], both parties present; several races in a year averaged."""
    out, by = [], {}
    for y, rv, dv, oth in races:
        if y in MID and rv and dv and (third_cut is None or oth is None or oth < third_cut):
            by.setdefault(y, []).append((rv, dv))
    for y, v in by.items():
        pr, pd = pres50[(state, y - 2)]
        out.append({"office": f"{state}:{office}", "year": y, "ratio_rep": stt.mean(a for a, _ in v) / pr, "ratio_dem": stt.mean(b for _, b in v) / pd})
    return out


def state_rows(st):
    rows = list(csv.DictReader(open(os.path.join(INP, st, "statewide_results.csv"))))
    loaded, _ = X.load(INP, st)  # applies the Alaska rule
    out = {}
    for r in loaded:
        tot = int(r["total_votes"]) if str(r.get("total_votes", "")).strip() else None
        oth = (tot - r["rep_votes"] - r["dem_votes"]) / tot if tot else None
        out.setdefault(r["office_key"], []).append((r["year"], r["rep_votes"], r["dem_votes"], oth))
    return out


def senate50(third_cut=None):
    by = {}
    for r in csv.DictReader(open(f"{POOLS}/senate50.csv")):
        if r["rep_votes"] and r["dem_votes"]:
            oth = float(r["top_other_share"]) if r["top_other_share"] else None
            by.setdefault(r["state"], []).append((int(r["year"]), int(r["rep_votes"]), int(r["dem_votes"]), oth))
    return by


def gov50():
    by = {}
    if not GOV:
        return by
    for r in csv.DictReader(open(GOV)):
        if r["rep_votes"].strip() and r["dem_votes"].strip():
            rv, dv = int(r["rep_votes"]), int(r["dem_votes"])
            tot = int(r["total_votes"]) if r["total_votes"].strip() else None
            by.setdefault(r["state"], []).append((int(r["year"]), rv, dv, (tot - rv - dv) / tot if tot else None))
    return by


def add_inc_by_party(E, pool_hist):
    """as expected.add_incumbency, but with a separate slope for each party (b_rep from Republican groups, b_dem from Democratic)."""
    for target in sorted({r["year"] for r in E}):
        hist = [r for r in E if r["year"] <= 2022 and r["year"] != target]
        groups, sg = {}, {}
        for src, dst in ((hist, groups), (hist + [r for r in pool_hist if r["year"] <= 2022 and r["year"] != target], sg)):
            for r in src:
                for p, P in (("rep", "R"), ("dem", "D")):
                    dst.setdefault((r["office"], p), []).append((1 if X.PRES_PARTY[r["year"]] == P else 0, r[f"ratio_{p}"]))
        bp = {}
        for p in ("rep", "dem"):
            num = den = 0.0
            for (o, pp), xs in sg.items():
                if pp != p:
                    continue
                mx = sum(x for x, _ in xs) / len(xs)
                my = sum(v for _, v in xs) / len(xs)
                num += sum((x - mx) * (v - my) for x, v in xs)
                den += sum((x - mx) ** 2 for x, _ in xs)
            bp[p] = num / den if den else None
        for r in (x for x in E if x["year"] == target):
            r["inc_b"] = bp["rep"]
            r["inc_b_dem"] = bp["dem"]
            for p, P in (("rep", "R"), ("dem", "D")):
                xs, b = groups.get((r["office"], p)), bp[p]
                if b is None or not xs:
                    r[f"expected_inc_{p}"] = r[f"dev_inc_{p}"] = None
                    continue
                a = sum(v - b * x for x, v in xs) / len(xs)
                r[f"expected_inc_{p}"] = r[f"pres_{p}"] * (a + b * (1 if X.PRES_PARTY[target] == P else 0))
                r[f"dev_inc_{p}"] = r[p] - r[f"expected_inc_{p}"]


S8 = {st: state_rows(st) for st in EIGHT}
SEN, GV = senate50(), gov50()


def pool_rows(name, target, cut):
    """history rows for the slope, excluding the target state's 2026-ballot offices (those come from E itself)."""
    rows, _ = X.load(INP, target)
    own26 = {k for k, _ in X.offices_2026(rows)}
    own_extra = [h for off, races in S8[target].items() if off not in own26 for h in hist_rows(target, off, races, cut)]
    others8 = [h for st in EIGHT if st != target for off, races in S8[st].items() for h in hist_rows(st, off, races, cut)]
    sen = [h for st, races in SEN.items() if st != target for h in hist_rows(st, "us_senate", races, cut)]
    gov = [h for st, races in GV.items() if st != target for h in hist_rows(st, "governor", races, cut)]
    # the eight states' own files are the better source for their Senate and governor rows: drop those from the 50-state lists
    sen_x8 = [h for h in sen if h["office"].split(":")[0] not in EIGHT]
    gov_x8 = [h for h in gov if h["office"].split(":")[0] not in EIGHT]
    own8_sen = [h for h in others8 if h["office"].endswith(":us_senate")]
    own8_gov = [h for h in others8 if h["office"].endswith(":governor")]
    return {"own": own_extra,
            "eight_all": own_extra + others8,
            "senate50": own_extra + sen_x8 + own8_sen,
            "gov50": own_extra + gov_x8 + own8_gov,
            "sen_gov50": own_extra + sen_x8 + gov_x8 + own8_sen + own8_gov,
            "everything": own_extra + others8 + sen_x8 + gov_x8}[name]


POOLNAMES = ["own", "published", "eight_all", "senate50"] + (["gov50", "sen_gov50", "everything"] if GV else ["everything"])
brows, rrows = [], []
for target in SHOW:
    rows, pres = X.load(INP, target)
    for cut, tag in ((None, ""), (0.15, "_no3rd"), (None, "_byparty")):
        for pn in POOLNAMES:
            if pn == "published":
                if cut is not None or tag:
                    continue
                ph = []
                for o in EIGHT:
                    if o == target:
                        continue
                    orows, opres = X.load(INP, o)
                    for r in X.build(orows, opres):
                        r["office"] = f"{o}:{r['office']}"
                        ph.append(r)
                E = X.build(rows, pres, ph)
            else:
                E = X.build(rows, pres)
                if cut is not None:  # drop the target's own strong-third-candidate years too
                    keep = {(off, y) for off, races in S8[target].items() for (y, rv, dv, oth) in races if oth is None or oth < cut}
                    E = [r for r in E if r["year"] == 2026 or (r["office"], r["year"]) in keep]
                (add_inc_by_party if tag == "_byparty" else X.add_incumbency)(E, pool_rows(pn, target, cut))
            bs = sorted(100 * r["inc_b"] for r in E if r.get("inc_b") is not None)
            b26 = next(100 * r["inc_b"] for r in E if r["year"] == 2026)
            b26d = next((100 * r["inc_b_dem"] for r in E if r["year"] == 2026 and r.get("inc_b_dem") is not None), None)
            groups = len({h["office"] for h in (pool_rows(pn, target, cut) if pn != "published" else [])}) + len({r["office"] for r in E})
            brows.append({"state": target, "pool": pn + tag, "b2026": round(b26, 2), "b2026_dem": round(b26d, 2) if b26d is not None else "",
                          "b_min": round(bs[0], 2), "b_max": round(bs[-1], 2), "office_groups": groups})
            for r in E:
                if r["year"] == 2026 and r.get("dev_inc_rep") is not None:
                    rrows.append({"state": target, "pool": pn + tag, "office": r["office"], "rep": round(r["rep"]), "dem": round(r["dem"]),
                                  "expected_inc_rep": round(r["expected_inc_rep"]), "expected_inc_dem": round(r["expected_inc_dem"]),
                                  "dev_inc_rep": round(r["dev_inc_rep"]), "dev_inc_dem": round(r["dev_inc_dem"])})
# the "everything" pool must be exactly what the figures use
for target in SHOW:
    a = sorted((h["office"], h["year"], round(h["ratio_rep"], 12), round(h["ratio_dem"], 12)) for h in pool_rows("everything", target, None))
    b = sorted((h["office"], h["year"], round(h["ratio_rep"], 12), round(h["ratio_dem"], 12)) for h in X.pool_all(INP, target, POOLS)[0])
    assert a == b, f"{target}: comparison pool differs from expected.pool_all"
# compact table: one row per state and pool, main race gaps and race counts
crows = []
for target in SHOW:
    for b in (x for x in brows if x["state"] == target):
        rs = [r for r in rrows if r["state"] == target and r["pool"] == b["pool"]]
        m = next(r for r in rs if r["office"] == MAIN[target])
        crows.append({"state": target, "pool": b["pool"], "b2026": b["b2026"], "b2026_dem": b.get("b2026_dem", ""), "main_office": MAIN[target],
                      "main_dev_inc_rep": m["dev_inc_rep"], "main_dev_inc_dem": m["dev_inc_dem"], "races": len(rs),
                      "dem_above": sum(r["dev_inc_dem"] > 0 for r in rs), "rep_below": sum(r["dev_inc_rep"] < 0 for r in rs)})
for fn, rows in (("b_by_pool.csv", brows), ("races_by_pool.csv", rrows), ("comparison.csv", crows)):
    with open(os.path.join(OUT, fn), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
print(f"pools: {POOLNAMES}; b rows {len(brows)}; race rows {len(rrows)}")

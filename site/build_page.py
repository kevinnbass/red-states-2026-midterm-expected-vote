"""Build the standalone figures page for every state in states.json (site/template.html -> <out>/artifact.html, index.html).

Every number on the page is computed here from build_states.py's outputs, so the page cannot disagree with the figures.
The figures are copied next to the page (figures/<st>/...).
usage: build_page.py <run_dir> <inputs_dir> <out_dir> [--links links.json]
  run_dir:    build_states.py output (<ST>/expected.csv, races_2018_2022_2026.csv, fig/, pool.json)
  inputs_dir: folder with <ST>/statewide_results.csv
  links.json: optional {"repo": url, "writeups": {"OH": url, ...}, "texas": url, "texas_figures": url}
"""
import csv, html, json, os, re, shutil, sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MINUS = "−"
RUN, INPUTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LINKS = json.load(open(sys.argv[sys.argv.index("--links") + 1])) if "--links" in sys.argv else {}
CFG = json.load(open(os.path.join(ROOT, "states.json")))
POOL = json.load(open(os.path.join(RUN, "pool.json")))
ORDER = [s for s in CFG["states"] if os.path.exists(os.path.join(RUN, s, "expected.csv"))]
NAMES = {"TX": "Texas", "OH": "Ohio", "KS": "Kansas", "IA": "Iowa", "AK": "Alaska", "MS": "Mississippi", "SC": "South Carolina", "IN": "Indiana"}
e = html.escape


def sg(x, nd=0):
    return f"{x:+,.{nd}f}".replace("-", MINUS)


def kk(x):
    return sg(x / 1e3) + "K"


V, DATA = {}, {"overview": []}
os.makedirs(os.path.join(OUT, "figures"), exist_ok=True)
tabs, panels, srcs, asof_states, summ = [], [], [], [], []
tot_d = tot_r = tot_n = 0
for i, st in enumerate(ORDER):
    c, name, s = CFG["states"][st], NAMES[st], st.lower()
    E = [r for r in csv.DictReader(open(os.path.join(RUN, st, "expected.csv"))) if r["year"] == "2026"]
    G = list(csv.DictReader(open(os.path.join(RUN, st, "races_2018_2022_2026.csv"))))
    order = []
    for r in G:
        if r["year"] == "2026" and r["race_2026"] not in order:
            order.append(r["race_2026"])
    off = {r["race_2026"]: r["office"] for r in G}
    g26 = {r["race_2026"]: r for r in G if r["year"] == "2026"}
    ex = {r["office"]: r for r in E}
    races, rows = [], []
    offices = []
    for race in order:
        if off[race] not in offices:
            offices.append(off[race])
    for o in offices:  # several seats of one office are averaged by the method: one row per office
        x = ex[o]
        seats = [r for r in order if off[r] == o]
        race = x["title"] if len(seats) > 1 else seats[0]
        f = lambda k: float(x[k])
        ra, da = f("rep"), f("dem")
        rec = {"race": re.sub(r"\s*\(.*\)$", "", race) + (f" ({len(seats)} seats, average)" if len(seats) > 1 else ""), "ra": ra, "da": da,
               "inc": {"r": 100 * (ra / f("expected_inc_rep") - 1), "d": 100 * (da / f("expected_inc_dem") - 1),
                       "re": f("expected_inc_rep"), "de": f("expected_inc_dem")}}
        races.append(rec)
        who = "; ".join(f"{g26[r]['rep_nominee']} (R) · {g26[r]['dem_nominee']} (D)" for r in seats)
        rows.append(f"<tr><td class='l'><span class='rn'>{e(rec['race'])}</span><span class='who'>{e(who)}</span></td>"
                    f"<td>{int(ra):,}</td><td>{int(f('expected_inc_rep')):,}</td><td class='dv'>{kk(ra - f('expected_inc_rep'))}</td>"
                    f"<td class='sep'>{int(da):,}</td><td>{int(f('expected_inc_dem')):,}</td><td class='dv'>{kk(da - f('expected_inc_dem'))}</td></tr>")
    DATA["overview"].append({"name": name, "races": races})
    nd = sum(r["inc"]["d"] > 0 for r in races)
    nr = sum(r["inc"]["r"] < 0 for r in races)
    tot_d, tot_r, tot_n = tot_d + nd, tot_r + nr, tot_n + len(races)
    summ.append((name, nd, nr, len(races)))
    # figures
    od = os.path.join(OUT, "figures", s)
    os.makedirs(os.path.join(od, "panels"), exist_ok=True)

    def fig(rel):
        shutil.copy2(os.path.join(RUN, st, "fig", rel), os.path.join(od, rel))
        w, h = Image.open(os.path.join(od, rel)).size
        return f"figures/{s}/{rel}", w, h

    cards = []
    for k, inc in ((1, True),):  # only the expectation adjusted for the president's party
        t = "_incumbency" if inc else ""
        views = [("Whole figure", f"{s}{t}_history_and_expected.png" if inc else f"{s}_history_and_expected.png"),
                 ("Left: 1994–2026", f"panels/{s}_history{t}.png"),
                 ("Right: 2018–2026 races", f"panels/{s}_expected{t}_2018_2026.png")]
        what = "adjusted for the president's party" if inc else "plain expectation"
        btns, first = [], None
        for j, (lab, rel) in enumerate(views):
            src, w, h = fig(rel)
            alt = f"{name}, Figure {k} ({what}): {lab.lower()}. {nd if not inc else sum(r['inc']['d'] > 0 for r in races)} of {len(races)} Democratic nominees above expected."
            cap = f"{name} · Figure {k}, {what} · {lab}"
            if j == 0:
                first = (src, w, h, alt, cap)
            btns.append(f'<button type="button" aria-pressed="{"true" if j == 0 else "false"}" data-src="{src}" data-w="{w}" data-h="{h}" '
                        f'data-alt="{e(alt, quote=True)}" data-cap="{e(cap, quote=True)}">{e(lab)}</button>')
        src, w, h, alt, cap = first
        cards.append(f'<figure class="figcard"><div class="fc-head"><p class="chart-title">{name}: actual vs. expected votes, adjusted for the president’s party</p>'
                     f'<div class="views" role="group" aria-label="View">{"".join(btns)}</div></div>'
                     f'<img class="fig" src="{src}" width="{w}" height="{h}" alt="{e(alt, quote=True)}" loading="lazy">'
                     f'<button type="button" class="full" data-src="{src}" data-cap="{e(cap, quote=True)}">View full size</button></figure>')
    wr = LINKS.get("writeups", {}).get(st)
    nd_i = sum(r["inc"]["d"] > 0 for r in races)
    nr_i = sum(r["inc"]["r"] < 0 for r in races)
    lead = (f"Democratic nominees ran above the expected vote in {nd} of {len(races)} statewide race{'s' if len(races) > 1 else ''} and "
            f"Republican nominees below it in {nr} of {len(races)}.")
    notes = "".join(f"<li>{e(n)}</li>" for n in c.get("notes", []))
    panels.append(f"""<div class="statepanel" id="p-{s}" role="tabpanel" aria-labelledby="t-{s}"{"" if i == 0 else " hidden"}>
    <div class="text"><h3>{name}</h3><p>{lead}{f' <a href="{wr}">What moved the {name} vote →</a>' if wr else ''}</p></div>
    {"".join(cards)}
    <div class="tblwrap wide"><table class="races">
      <caption class="sr">{name} 2026: actual and expected votes by race</caption>
      <thead><tr class="grp"><th></th><th colspan="3"><span class="sw r"></span>Republican</th><th colspan="3" class="sep"><span class="sw d"></span>Democrat</th></tr>
      <tr><th class="l">2026 race</th><th>Actual</th><th>Expected</th><th>Actual − expected</th><th class="sep">Actual</th><th>Expected</th><th>Actual − expected</th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>
    <div class="text"><ul class="plain small"><li>{e(c['asof'][0].upper() + c['asof'][1:])}.</li>{notes}</ul></div>
  </div>""")
    tabs.append(f'<button type="button" role="tab" id="t-{s}" data-st="{st}" aria-controls="p-{s}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{name}</button>')
    srcs.append(f"<li><b>{name}:</b> {e(c['source'])}.</li>")
    asof_states.append(f"{name}: {e(c['asof'])}.")

PLAB = [("own", "This state only"), ("published", "First version: 8 states, offices on the 2026 ballot"),
        ("senate50", "Senate races in all 50 states, plus this state"), ("everything", "All states (used in the figures)"),
        ("everything_byparty", "All states, one slope per party")]
cmp_path = os.path.join(RUN, "..", "pool_comparison", "comparison.csv")
CMP = {(r["state"], r["pool"]): r for r in csv.DictReader(open(cmp_path))} if os.path.exists(cmp_path) else {}
OFFN = {"governor": "Governor", "us_senate": "Senate", "secretary_of_state": "Secretary of State"}
if CMP:
    head = "".join(f"<th>{e(l)}</th>" for _, l in PLAB)
    body = []
    for st in ORDER + [x for x in ("TX",) if x not in ORDER]:
        cells = []
        for k, _ in PLAB:
            r = CMP[(st, k)]
            bt = f"b {float(r['b2026']):+.1f}".replace("-", MINUS) + (f" R, {float(r['b2026_dem']):+.1f} D".replace("-", MINUS) if r["b2026_dem"] else "")
            cells.append(f"<td><span class='g'>R {kk(int(r['main_dev_inc_rep']))} · D {kk(int(r['main_dev_inc_dem']))}</span>"
                         f"<span class='bb'>{bt}; {r['dem_above']} D above, {r['rep_below']} R below, of {r['races']}</span></td>")
        body.append(f"<tr><td class='l'><span class='rn'>{NAMES[st]}</span><span class='who'>{OFFN[r['main_office']]}</span></td>{''.join(cells)}</tr>")
    V["pool_table"] = (f'<div class="tblwrap wide"><table class="pools"><caption class="sr">Main race gap against the adjusted expectation under '
                       f'each pool</caption><thead><tr><th class="l">State, main race</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')
    bp = [(float(r["b2026"]), float(r["b2026_dem"])) for (st, k), r in CMP.items() if k == "everything_byparty"]
    lo = lambda xs: f"{min(xs):+.1f}".replace("-", MINUS)
    hi = lambda xs: f"{max(xs):+.1f}".replace("-", MINUS)
    V["pool_party_note"] = (f"Estimated separately for each party (last column), the effect is {lo([a for a, _ in bp])} to {hi([a for a, _ in bp])} points "
                            f"for Republicans and {lo([b for _, b in bp])} to {hi([b for _, b in bp])} for Democrats, depending on the state's own offices.")
else:
    V["pool_table"] = V["pool_party_note"] = ""
pool_names = POOL["description"]
b26 = next(float(r["inc_b"]) for r in csv.DictReader(open(os.path.join(RUN, ORDER[0], "expected.csv"))) if r["year"] == "2026")
V["style"] = open(os.path.join(HERE, "style.css.part"), encoding="utf-8").read().replace("</style>", open(os.path.join(HERE, "extra.css"), encoding="utf-8").read() + "</style>")
V["kicker"] = " · ".join(NAMES[s] for s in ORDER) + " · Nov. 3, 2026"
V["dek"] = (f"For each statewide race on the 2026 ballot, the vote each party would get if the office followed its own 1994–2022 midterm "
            f"pattern, with the usual midterm loss for the party holding the White House, set against the unofficial count. Across {tot_n} races, the Democratic nominee ran above that expected vote in "
            f"<b>{tot_d}</b> and the Republican nominee below it in <b>{tot_r}</b>.")
V["asof"] = "2026 counts are unofficial and differ by state in how complete they are; see each state and the method notes."
V["ov_h2"] = (f"Democratic nominees ran above expectation in {tot_d} of {tot_n} races; Republican nominees ran below it in {tot_r}")
V["ov_p"] = " ".join(f"{n}: {d} of {t} above, {r} of {t} below." for n, d, r, t in summ)
V["state_tabs"], V["state_panels"] = "".join(tabs), "\n  ".join(panels)
V["pool_names"], V["b26"] = pool_names, f"{100 * b26:+.1f}".replace("-", MINUS)
V["asof_states"] = " ".join(asof_states)
V["sources"] = "".join(srcs) + ("<li><b>Presidential baselines (all states):</b> MIT Election Data and Science Lab, U.S. President 1976–2024 "
                                 "(doi:10.7910/DVN/42MVDX).</li>")
lk = []
if LINKS.get("repo"):
    lk.append(f'<a href="{LINKS["repo"]}">Data, code and full-size figures on GitHub<span>Every source file or the link to get it, the method, '
              f'and the code that rebuilds every number and figure on this page.</span></a>')
for st in ORDER:
    u = LINKS.get("writeups", {}).get(st)
    if u:
        lk.append(f'<a href="{u}">What moved the {NAMES[st]} vote in 2026<span>Races, counties, votes cast and the Senate-governor split.</span></a>')
if LINKS.get("texas_figures"):
    lk.append(f'<a href="{LINKS["texas_figures"]}">Texas 2026: actual vs. expected votes<span>The same figures for Texas.</span></a>')
V["links"] = "\n    ".join(lk) or "<p>Links are added when the companion pages are published.</p>"
V["footer"] = "Data: state election offices, AP via NPR, MIT Election Data and Science Lab, OpenElections. 2026 results unofficial."
V["data_json"] = json.dumps(DATA, separators=(",", ":")).replace("</", "<\\/")
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
miss = sorted(set(re.findall(r"\{\{(\w+)\}\}", tpl)) - set(V))
assert not miss, miss
page = re.sub(r"\{\{(\w+)\}\}", lambda m: V[m.group(1)], tpl)
open(os.path.join(OUT, "artifact.html"), "w", encoding="utf-8").write(page)
head, body = page.split("<!-- page -->", 1)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head.strip() + "\n</head>\n<body>" + body.rstrip() + "\n</body>\n</html>\n")
print(f"page: {len(page):,} bytes; states {ORDER}; races {tot_n}; D above {tot_d}; R below {tot_r}")

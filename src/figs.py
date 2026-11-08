"""Figures for any state (same design as the Texas figures): history of each office's midterm vote vs. the presidential
vote two years earlier, and the grid of 2026 races with expected-vote shadow bars; plain and president's-party versions;
each pair spliced into one image.

Usage: python3 figs.py <expected.csv> <races_2018_2022_2026.csv> <out_dir> --state OH --asof "<2026 update>"
                       --source "<results source>" [--note "<extra footnote>"]...
"""
import argparse, csv, math, os, re, textwrap
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#7a7974", "#e4e3df"
REP, DEM, REP_L, DEM_L = "#e34948", "#2a78d6", "#f6c3c2", "#b7d3f6"
YEARS = [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026]
PRES_PARTY = {1994: "D", 1998: "D", 2002: "R", 2006: "R", 2010: "D", 2014: "D", 2018: "R", 2022: "D", 2026: "R"}
B_SCOPE = [", estimated from this state's 1994–2022 midterms"]  # main() may change it when the slope is pooled across states
NAMES = {"TX": "Texas", "OH": "Ohio", "KS": "Kansas", "IA": "Iowa", "AK": "Alaska", "MS": "Mississippi", "SC": "South Carolina",
         "IN": "Indiana"}


def font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    return next((n for n in ("Inter", "Noto Sans", "DejaVu Sans") if n in names), "sans-serif")


def column(ax, fig, x, bottom, top, w, color, radius_px=3, **kw):
    if top == bottom:
        return
    fig.canvas.draw()
    (x0, y0), (x1, y1) = ax.transData.transform((0, 0)), ax.transData.transform((1, 1))
    ux, uy = 1 / abs(x1 - x0), 1 / abs(y1 - y0)
    lo, hi = min(bottom, top), max(bottom, top)
    ax.add_patch(FancyBboxPatch((x - w / 2, lo), w, hi - lo, boxstyle=f"round,pad=0,rounding_size={radius_px * ux}",
                                mutation_aspect=uy / ux, facecolor=color, edgecolor="none", **kw))
    sq = min(hi - lo, radius_px * 1.5 * uy)
    yb = lo if top >= bottom else hi - sq
    ax.add_patch(Rectangle((x - w / 2, yb), w, sq, facecolor=color, edgecolor="none", **kw))


def fl(v):
    return float(v) if v not in ("", None) else None


def pct(x):
    return f"{x:+.0f}%".replace("-", "−")


def offices(E):
    out = []
    for r in E:
        if (r["office"], r["title"]) not in out:
            out.append((r["office"], r["title"]))
    return out


def grid_shape(n, max_cols):
    ncol = min(max_cols, n)
    return ncol, math.ceil(n / ncol)


def fig_history(E, st, source, notes, out_png, inc=False, dpi=170, one_party=None):
    offs = offices(E)
    by = defaultdict(dict)
    for r in E:
        by[r["office"]][int(r["year"])] = r
    vals = []
    for r in E:
        for p in ("rep", "dem"):
            vals.append(100 * (fl(r[f"ratio_{p}"]) - 1))
            if inc and fl(r[f"expected_inc_{p}"]) is not None:
                vals.append(100 * (fl(r[f"expected_inc_{p}"]) / fl(r[f"pres_{p}"]) - 1))
    lo = 20 * math.floor((min(vals) - 6) / 20)
    hi = 20 * math.ceil((max(vals) + 8) / 20)
    plt.rcParams.update({"font.family": font(), "font.size": 10})
    ncol, nrow = grid_shape(len(offs), 2)
    W = 17 if ncol == 2 else 10
    name = NAMES[st]
    if inc:
        title = f"{name} statewide midterm votes vs. each party's presidential vote two years earlier, adjusted for the president's party"
        sub = (f"Solid bars: % change in the party's vote for the office from its {name} presidential vote two years earlier. Shadow bars: "
               "the change expected for that office and party given whether it held the White House, estimated without that year. "
               "Letter under each year: the president's party. * 2026 unofficial.")
    else:
        title = f"{name} statewide midterm votes vs. each party's presidential vote two years earlier"
        sub = (f"% change in each party's vote for the office from its {name} presidential vote two years earlier, 1994–2026. "
               "Dashed lines: 1994–2022 average. * 2026 unofficial.")
    tfs = 18 if ncol == 2 else 15
    tl = textwrap.wrap(title, 100 if ncol == 2 else 70)
    sl = textwrap.wrap(sub, 165 if ncol == 2 else 100)
    bs = sorted({round(100 * fl(r["inc_b"]), 1) for r in E if fl(r.get("inc_b")) is not None})
    note = (f"Source: {source}. Presidential baselines: MIT Election Data and Science Lab. Republican and Democratic nominees only "
            "(party-line votes). Offices with several races in a year use their average.")
    if inc and bs:
        note = (f"Expected change = the office's baseline ratio for that party + an adjustment when the party holds the White House "
                f"({bs[0]:+.1f} to {bs[-1]:+.1f} points of the presidential vote, depending on the year left out){B_SCOPE[0]}, "
                "leaving out the year shown. " + note)
    nl = textwrap.wrap(" ".join([note] + notes), 220 if ncol == 2 else 130)
    cellh = 3.45 if inc else 3.3
    head = 0.25 + 0.31 * len(tl) * tfs / 17 + 0.21 * len(sl) + 0.5
    foot = 0.2 + 0.155 * len(nl)
    H = head + cellh * nrow + foot
    fig = plt.figure(figsize=(W, H), dpi=dpi, facecolor=SURFACE)
    top, bottom = 1 - head / H, foot / H
    cell = (top - bottom) / nrow
    left0, colw, axw = (0.05, 0.48, 0.42 if inc else 0.40) if ncol == 2 else (0.09, 0.0, 0.80 if inc else 0.76)
    for k, (key, title) in enumerate(offs):
        r_, c_ = divmod(k, ncol)
        ax = fig.add_axes([left0 + c_ * colw, top - (r_ + 1) * cell + cell * (0.24 if inc else 0.2), axw, cell * (0.62 if inc else 0.66)],
                          facecolor=SURFACE)
        ax.set_xlim(-0.6, len(YEARS) - 0.4)
        ax.set_ylim(lo, hi + 4)
        ax.yaxis.grid(True, color=GRID, lw=0.7)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left", "bottom"):
            ax.spines[sp].set_visible(False)
        ax.axhline(0, color="#9a9994", lw=0.9, zorder=4)
        ax.tick_params(axis="both", length=0, colors=INK2, labelsize=8.8)
        ticks = list(range(lo, hi + 1, 20))
        ax.set_yticks(ticks)
        ax.set_yticklabels([(f"+{t}%" if t > 0 else f"{t}%".replace("-", "−")) if t else "0" for t in ticks])
        w, gap, off = (0.28, 0.12, 0.09) if inc else (0.34, 0.03, 0)
        lab26 = {}
        hist = [by[key][y] for y in YEARS if y in by[key] and y <= 2022]
        for i, y in enumerate(YEARS):
            if y not in by[key]:
                ax.text(i, 3, (one_party or {}).get((key, y), "no race"), ha="center", va="bottom", fontsize=7.5, color=MUTED)
                continue
            rr = by[key][y]
            for xc, p, col, light in ((i - w / 2 - gap / 2, "rep", REP, REP_L), (i + w / 2 + gap / 2, "dem", DEM, DEM_L)):
                v = 100 * (fl(rr[f"ratio_{p}"]) - 1)
                if inc and fl(rr[f"expected_inc_{p}"]) is not None:
                    e = 100 * (fl(rr[f"expected_inc_{p}"]) / fl(rr[f"pres_{p}"]) - 1)
                    column(ax, fig, xc + off, 0, e, w, light, zorder=1)
                    ax.add_patch(Rectangle((xc + off - w / 2, min(0, e)), w, abs(e), fill=False, edgecolor=col, lw=0.8, ls=(0, (3, 2)), zorder=1.5))
                    if y == 2026:
                        lab26[p] = (v, e)
                if y == 2026:
                    column(ax, fig, xc, 0, v, w, light, zorder=2)
                    ax.add_patch(Rectangle((xc - w / 2, min(0, v)), w, abs(v), fill=False, edgecolor=col, lw=1.1, hatch="///", zorder=2.5))
                    if not inc:
                        ax.text(xc, v + (1.5 if v >= 0 else -1.5), pct(v), ha="center", va="bottom" if v >= 0 else "top", fontsize=8.2,
                                fontweight="semibold", color=INK, zorder=5, bbox=dict(boxstyle="round,pad=0.12", fc=SURFACE, ec="none"))
                else:
                    column(ax, fig, xc, 0, v, w, col, zorder=2)
        if not inc and hist:
            ar = 100 * (sum(fl(h["ratio_rep"]) for h in hist) / len(hist) - 1)
            ad = 100 * (sum(fl(h["ratio_dem"]) for h in hist) / len(hist) - 1)
            ax.axhline(ar, color=REP, lw=1.0, ls=(0, (4, 3)))
            ax.axhline(ad, color=DEM, lw=1.0, ls=(0, (4, 3)))
            ax.text(len(YEARS) - 0.35, ar, f"R avg {ar:.0f}%".replace("-", "−"), fontsize=8.2, color=INK2, va="bottom" if ar > ad else "top", clip_on=False)
            ax.text(len(YEARS) - 0.35, ad, f"D avg {ad:.0f}%".replace("-", "−"), fontsize=8.2, color=INK2, va="bottom" if ad >= ar else "top", clip_on=False)
        ax.set_xticks(range(len(YEARS)))
        if inc:
            ax.set_xticklabels([f"{y}{'*' if y == 2026 else ''}\n{PRES_PARTY[y]}" for y in YEARS], fontsize=8.6, color=INK, linespacing=1.3)
        else:
            ax.set_xticklabels([f"{y}*" if y == 2026 else str(y) for y in YEARS], fontsize=8.8, color=INK)
        ax.set_title(title, fontsize=12, fontweight="bold", color=INK, loc="left", pad=6)
        if inc and len(lab26) == 2:
            ax.text(1.0, 1.03, f"2026: R {pct(lab26['rep'][0])} (expected {pct(lab26['rep'][1])})   D {pct(lab26['dem'][0])} (expected {pct(lab26['dem'][1])})",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=9.2, color=INK, fontweight="semibold")
    x0 = 0.05 if ncol == 2 else 0.06
    y = 1 - 0.25 / H
    fig.text(x0, y, "\n".join(tl), fontsize=tfs, fontweight="bold", color=INK, va="top", linespacing=1.15)
    y -= 0.31 * len(tl) * tfs / 17 / H
    fig.text(x0, y - 0.04 / H, "\n".join(sl), fontsize=10.5, color=INK2, va="top", linespacing=1.35)
    y -= (0.21 * len(sl) + 0.12) / H
    if inc:
        shadow = Rectangle((0, 0), 1, 1, facecolor="#e4e3df", edgecolor="#7a7974", ls=(0, (3, 2)), lw=0.9)
        handles, labels = [Rectangle((0, 0), 1, 1, color=REP), Rectangle((0, 0), 1, 1, color=DEM), shadow], ["Republican", "Democrat", "Expected (shadow)"]
    else:
        handles, labels = [Rectangle((0, 0), 1, 1, color=REP), Rectangle((0, 0), 1, 1, color=DEM)], ["Republican", "Democrat"]
    fig.legend(handles=handles, labels=labels, loc="upper left", bbox_to_anchor=(x0 - 0.008, y), ncol=len(labels), frameon=False,
               fontsize=10.5, labelcolor=INK)
    fig.text(x0, 0.15 / H, "\n".join(nl), fontsize=8.4, color=MUTED, va="bottom", linespacing=1.45)
    fig.savefig(out_png, dpi=dpi, facecolor=SURFACE)
    plt.close(fig)


def race_labels(races):
    SUF = ("JR", "SR", "II", "III", "IV")

    def sur(n):
        # "+" marks a party total that combines several candidates (Alaska's top-four elections; see expected.ALL_LINES_FROM)
        plus = re.search(r" and other \w+ \(first choice\)$", n) is not None
        n = re.sub(r" and other \w+ \(first choice\)$", "", n)
        n = re.sub(r"\([A-Za-z/]+\)", "", n).strip()   # party markers: (I), (R), (DEM/NON)
        n = n.split("/")[0].strip()                     # a joint ticket: the first name on it
        if "," in n:                                    # "Last, First" or "First Last, Jr."
            a, b = (x.strip() for x in n.split(",", 1))
            if b.upper().rstrip(".") not in SUF:       # "Last, First": the part before the comma
                return (a.title() if a.isupper() else a) + ("+" if plus else "")
            n = a                                       # "First Last, Jr.": drop the suffix
        p = [x for x in n.split() if x.upper().rstrip(".,") not in SUF]
        last = p[-1].rstrip(",") if p else n
        return (last.title() if last.isupper() else last) + ("+" if plus else "")
    for r in races:
        y = int(r["year"])
        base = "2026*" if y == 2026 else str(y)
        if r["rep_nominee"]:
            rn, dn = sur(r["rep_nominee"]), sur(r["dem_nominee"])
            if rn == dn:
                rn, dn = r["rep_nominee"].replace("(I)", "").strip().title(), r["dem_nominee"].strip().title()
                r["label"] = f"{base}\n{rn} (R)\nvs. {dn} (D)"
            else:
                m = f"{rn} (R) vs. {dn} (D)"
                r["label"] = f"{base}\n" + (m.replace(" vs. ", "\nvs. ") if len(m) > 22 else m)
        else:
            r["label"] = f"{base}\navg. of {r['basis'].count(',') + 1} races"


def fig_expected(E, races, st, asof, source, notes, out_png, inc=False):
    pre = "expected_inc_" if inc else "expected_"
    ex = {(r["office"], int(r["year"])): r for r in E}
    order, groups = [], defaultdict(list)
    for r in races:
        if r["race_2026"] not in order:
            order.append(r["race_2026"])
        groups[r["race_2026"]].append(r)
    mx = 0
    for r in races:
        e = ex[(r["office"], int(r["year"]))]
        mx = max([mx, float(r["rep_votes"]), float(r["dem_votes"])] + [fl(e[k + p]) or 0 for k in ("expected_", "expected_inc_") for p in ("rep", "dem")])
    unit, suf, nd = (1e6, "M", 2) if mx >= 1e6 else (1e3, "K", 0)
    ytop = mx / unit * 1.34
    step = next(s for s in (0.25, 0.5, 1, 2, 5, 10, 25, 50, 100, 200, 250, 500, 1000) if mx / unit / s <= 4)
    plt.rcParams.update({"font.family": font(), "font.size": 10})
    ncol, nrow = grid_shape(len(order), 3)
    W = {1: 8.5, 2: 12.5, 3: 18}[ncol]
    name = NAMES[st]
    title = f"{name} Statewide Races, 2018–2026: Actual vs. Expected Votes" + (", Adjusted for the President's Party" if inc else "")
    tfs = {1: 15, 2: 18, 3: 21}[ncol]
    tl = textwrap.wrap(title, {1: 46, 2: 70, 3: 110}[ncol])
    sub = (f"Votes in {'millions' if suf == 'M' else 'thousands'}. Above each pair: actual votes (bold) and actual minus expected. "
           "* 2026 results are unofficial.")
    sl = textwrap.wrap(sub, {1: 85, 2: 125, 3: 200}[ncol])
    note = ("Expected vote = the party's presidential vote in the state two years earlier × the office's average ratio of midterm vote to prior "
            "presidential vote in this state's 1994–2022 midterms (for 2018 and 2022, leaving out that year).")
    if inc:
        bs = {int(r["year"]): fl(r["inc_b"]) for r in E if fl(r.get("inc_b")) is not None}
        note = ("Expected vote = the party's presidential vote two years earlier × (the office's baseline ratio for that party + an adjustment when "
                f"the party holds the White House: {100 * bs[2026]:+.1f} points of the presidential vote for 2026{B_SCOPE[0]}, leaving out "
                "the year shown). President's party: Republicans in 2018 and 2026, Democrats in 2022.")
    nl = textwrap.wrap(" ".join([note, f"Source: {source}; 2026 unofficial ({asof}). Offices with several races in a year use their average."] + notes),
                       {1: 125, 2: 175, 3: 235}[ncol])
    head = 0.3 + 0.33 * len(tl) * tfs / 18 + 0.45 + 0.2 * len(sl) + 0.25
    foot = 0.2 + 0.16 * len(nl)
    H = head + 4.3 * nrow + foot
    fig = plt.figure(figsize=(W, H), dpi=170, facecolor=SURFACE)
    top, bottom = 1 - head / H, foot / H
    cell = (top - bottom) / nrow
    for k, race in enumerate(order):
        r_, c_ = divmod(k, ncol)
        ax = fig.add_axes([0.06 + c_ * (0.93 / ncol), top - (r_ + 1) * cell + cell * 0.25, 0.93 / ncol - 0.05, cell * 0.62], facecolor=SURFACE)
        g = sorted(groups[race], key=lambda x: int(x["year"]))
        ax.set_xlim(-0.6, len(g) - 0.4)
        ax.set_ylim(0, ytop)
        ax.yaxis.grid(True, color=GRID, lw=0.7)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color("#9a9994")
        ax.tick_params(axis="both", length=0, colors=INK2, labelsize=9)
        ticks = [i * step for i in range(int(ytop / step) + 1)]
        ax.set_yticks(ticks)
        ax.set_yticklabels([(f"{t:g}{suf}" if t else "0") for t in ticks])
        w, gap, off = 0.30, 0.10, 0.11
        for x, row in enumerate(g):
            e = ex[(row["office"], int(row["year"]))]
            for xc, act, exp, col, light in ((x - w / 2 - gap / 2, float(row["rep_votes"]) / unit, fl(e[pre + "rep"]), REP, REP_L),
                                             (x + w / 2 + gap / 2, float(row["dem_votes"]) / unit, fl(e[pre + "dem"]), DEM, DEM_L)):
                if exp is not None:
                    exp /= unit
                    column(ax, fig, xc + off, 0, exp, w, light, zorder=1)
                    ax.add_patch(Rectangle((xc + off - w / 2, 0), w, exp, fill=False, edgecolor=col, lw=0.9, ls=(0, (3, 2)), zorder=1.5))
                column(ax, fig, xc, 0, act, w, col, zorder=2)
                top_ = max(act, exp or 0)
                ax.text(xc + off / 2, top_ + ytop * 0.014, f"{act:.{nd}f}", ha="center", va="bottom", fontsize=8.6, fontweight="semibold", color=INK, zorder=3)
                if exp is not None:
                    d = round(act - exp, nd) + 0.0
                    ax.text(xc + off / 2, top_ + ytop * 0.065, f"{d:+.{nd}f}".replace("-", "−"), ha="center", va="bottom", fontsize=7.8, color=INK2, zorder=3)
        ax.set_xticks(range(len(g)))
        ax.set_xticklabels([r["label"] for r in g], fontsize=8.2, color=INK, linespacing=1.25)
        ax.set_title(race, fontsize=12.5, fontweight="bold", color=INK, pad=8)
    y = 1 - 0.3 / H
    fig.text(0.5, y, "\n".join(tl), ha="center", va="top", fontsize=tfs, fontweight="bold", color=INK, linespacing=1.15)
    y -= (0.33 * len(tl) * tfs / 18 + 0.25) / H
    shadow = Rectangle((0, 0), 1, 1, facecolor="#e4e3df", edgecolor="#7a7974", ls=(0, (3, 2)), lw=0.9)
    fig.legend(handles=[Rectangle((0, 0), 1, 1, color=REP), Rectangle((0, 0), 1, 1, color=DEM), shadow],
               labels=["Republican (actual)", "Democrat (actual)", "Expected (shadow)"], loc="center", bbox_to_anchor=(0.5, y),
               ncol=3, frameon=False, fontsize=11, labelcolor=INK, handlelength=1.4, handleheight=0.9, columnspacing=1.6)
    y -= 0.3 / H
    fig.text(0.5, y, "\n".join(sl), ha="center", va="top", fontsize=10.5, color=INK2, linespacing=1.3)
    fig.text(0.5, 0.15 / H, "\n".join(nl), ha="center", va="bottom", fontsize=8.6, color=MUTED, linespacing=1.45)
    fig.savefig(out_png, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def splice(E, st, source, notes, left_png, right_png, out_png, inc, one_party=None):
    R = Image.open(right_png).convert("RGB")
    L0 = Image.open(left_png)
    tall = out_png + ".left_tall.png"
    fig_history(E, st, source, notes, tall, inc=inc, dpi=170 * R.height / L0.height, one_party=one_party)
    L = Image.open(tall).convert("RGB")
    gut = 120
    img = Image.new("RGB", (L.width + gut + R.width, max(L.height, R.height)), (252, 252, 251))
    img.paste(L, (0, (img.height - L.height) // 2))
    img.paste(R, (L.width + gut, (img.height - R.height) // 2))
    img.save(out_png, dpi=(170, 170))
    os.replace(tall, os.path.join(os.path.dirname(out_png), "_work_" + os.path.basename(tall)))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("expected_csv")
    a.add_argument("races_csv")
    a.add_argument("out_dir")
    a.add_argument("--state", required=True)
    a.add_argument("--asof", required=True)
    a.add_argument("--source", required=True)
    a.add_argument("--note", action="append", default=[])
    a.add_argument("--b-scope", help="text after the slope, e.g. ', estimated from the 1994–2022 midterms of eight states'")
    o = a.parse_args()
    if o.b_scope:
        B_SCOPE[0] = o.b_scope
    E = list(csv.DictReader(open(o.expected_csv)))
    races = list(csv.DictReader(open(o.races_csv)))
    race_labels(races)
    st = o.state
    os.makedirs(os.path.join(o.out_dir, "panels"), exist_ok=True)
    s = st.lower()
    P = lambda n: os.path.join(o.out_dir, "panels", n)
    op = os.path.join(os.path.dirname(o.expected_csv), "one_party_races.csv")
    one = {(r["office"], int(r["year"])): r["label"] for r in csv.DictReader(open(op))} if os.path.exists(op) else {}
    fig_history(E, st, o.source, o.note, P(f"{s}_history.png"), one_party=one)
    fig_history(E, st, o.source, o.note, P(f"{s}_history_incumbency.png"), inc=True, one_party=one)
    fig_expected(E, races, st, o.asof, o.source, o.note, P(f"{s}_expected_2018_2026.png"))
    fig_expected(E, races, st, o.asof, o.source, o.note, P(f"{s}_expected_incumbency_2018_2026.png"), inc=True)
    splice(E, st, o.source, o.note, P(f"{s}_history.png"), P(f"{s}_expected_2018_2026.png"), os.path.join(o.out_dir, f"{s}_history_and_expected.png"), False, one_party=one)
    splice(E, st, o.source, o.note, P(f"{s}_history_incumbency.png"), P(f"{s}_expected_incumbency_2018_2026.png"),
           os.path.join(o.out_dir, f"{s}_incumbency_history_and_expected.png"), True, one_party=one)
    print("figures written for", st)


if __name__ == "__main__":
    main()

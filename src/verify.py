"""Check a fresh build against the committed outputs.

CSV and JSON outputs must match byte for byte. Figures must match pixel for pixel, or (with --tolerant) differ in at most
0.1% of pixels, which allows for font rendering differences between machines.
usage: verify.py <build_states_dir> <data_derived_dir> <figures_dir> [--tolerant]   (exit 0 = everything matches)
"""
import filecmp, os, sys

import numpy as np
from PIL import Image

B, DD, FG = sys.argv[1:4]
tol = "--tolerant" in sys.argv
bad = n = 0
for st in sorted(x for x in os.listdir(B) if os.path.isdir(os.path.join(B, x))):
    s = st.lower()
    for f in ("expected.csv", "races_2018_2022_2026.csv", "one_party_races.csv"):
        n += 1
        if not filecmp.cmp(os.path.join(B, st, f), os.path.join(DD, st, f), shallow=False):
            bad += 1
            print("DIFFERS", st, f)
    figs = [os.path.join("fig", x) for x in os.listdir(os.path.join(B, st, "fig")) if x.startswith(s + "_") and x.endswith(".png")]
    figs += [os.path.join("fig", "panels", x) for x in os.listdir(os.path.join(B, st, "fig", "panels"))]
    for rel in figs:
        n += 1
        a = np.asarray(Image.open(os.path.join(B, st, rel)).convert("RGB"))
        ref = os.path.join(FG, s, rel.replace("fig" + os.sep, "", 1))
        b = np.asarray(Image.open(ref).convert("RGB"))
        if a.shape != b.shape:
            bad += 1
            print("SIZE DIFFERS", ref, a.shape, b.shape)
            continue
        frac = float(np.mean(np.any(a != b, axis=2)))
        if frac > (0.001 if tol else 0.0):
            bad += 1
            print(f"PIXELS DIFFER {ref}: {100 * frac:.3f}%")
n += 1
if not filecmp.cmp(os.path.join(B, "pool.json"), os.path.join(DD, "pool.json"), shallow=False):
    bad += 1
    print("DIFFERS pool.json")
print(f"verify: {n - bad} of {n} outputs match" + (" (tolerant)" if tol else ""))
sys.exit(1 if bad else 0)

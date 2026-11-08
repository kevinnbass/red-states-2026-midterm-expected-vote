"""Build the expected-vote tables and figures for every state in states.json.

usage: build_states.py <inputs_dir> <out_dir> [ST ...]
  inputs_dir: folder with presidential_1992_2024.csv and <ST>/statewide_results.csv
  out_dir:    gets <ST>/expected.csv, <ST>/races_2018_2022_2026.csv and <ST>/fig/ (the two spliced figures + panels)
The president's-party slope is pooled across states.json "pool"; each office keeps its own state's baseline.
Figures need matplotlib and Pillow (render on a worker: /mnt/data/projects/election/venv-figs/bin/python).
"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "..", "states.json")))
NAMES = {"TX": "Texas", "OH": "Ohio", "KS": "Kansas", "IA": "Iowa", "AK": "Alaska", "MS": "Mississippi", "SC": "South Carolina",
         "IN": "Indiana"}


def main():
    inputs, out = sys.argv[1], sys.argv[2]
    sys.path.insert(0, HERE)
    import expected
    # a state counts in the pool only when it has 2026 offices with history (expected.build makes rows only for those)
    pool = [s for s in CFG["pool"] if os.path.exists(os.path.join(inputs, s, "statewide_results.csv"))
            and any(r["year"] <= 2022 for r in expected.build(*expected.load(inputs, s)))]
    missing = [s for s in CFG["pool"] if s not in pool]
    states = sys.argv[3:] or list(CFG["states"])
    names = [NAMES[s] for s in pool]
    pool_names = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    b_scope = CFG["b_scope"].format(pool_names=pool_names)
    print("pool:", ",".join(pool), "| not yet available:", ",".join(missing) or "none", flush=True)
    for st in states:
        c = CFG["states"][st]
        d = os.path.join(out, st)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "expected.py"), inputs, st, d, "--pool", ",".join(pool)], check=True)
        # office-years that had a race but whose results could not be obtained: labeled "no data", not "no race"
        # an office-year counts as "no data" only while the input file still has no row for it
        have = {(r["office_key"], int(r["year"])) for r in csv.DictReader(open(os.path.join(inputs, st, "statewide_results.csv")))}
        nd = {off: [y for y in ys if (off, y) not in have] for off, ys in c.get("no_data", {}).items()}
        if any(nd.values()):
            with open(os.path.join(d, "one_party_races.csv"), "a", newline="") as fh:
                for off, years in sorted(nd.items()):
                    for y in years:
                        fh.write(f"{off},{y},no data\n")
        cmd = [sys.executable, "-I", os.path.join(HERE, "figs.py"), os.path.join(d, "expected.csv"), os.path.join(d, "races_2018_2022_2026.csv"),
               os.path.join(d, "fig"), "--state", st, "--asof", c["asof"], "--source", c["source"], "--b-scope", b_scope]
        for n in c.get("notes", []):
            cmd += ["--note", n]
        subprocess.run(cmd, check=True)
    json.dump({"pool": pool, "missing_from_pool": missing, "b_scope": b_scope}, open(os.path.join(out, "pool.json"), "w"), indent=1)


if __name__ == "__main__":
    main()

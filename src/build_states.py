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
    pooldir = os.path.join(inputs, CFG["pool_dir"])
    states = sys.argv[3:] or list(CFG["states"])
    _, info = expected.pool_all(inputs, states[0], pooldir)
    names = [NAMES[s] for s in info["full_states"]]
    parts = ["U.S. Senate races in all 50 states"]
    if "governor" in info["extra_offices"]:
        gst = {r["state"] for r in csv.DictReader(open(os.path.join(pooldir, "governors50.csv")))}
        parts.append(f"governor races in the {len(gst)} states that elected governors in those years")
    parts.append("every statewide office in " + ", ".join(names[:-1]) + " and " + names[-1])
    description = ", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 2 else " and ".join(parts)
    offices = description
    b_scope = ", estimated from the 1994–2022 midterms of " + description + ", together"
    pool, missing = info["full_states"], []
    print("pool:", info["states"], "states:", description, flush=True)
    for st in states:
        c = CFG["states"][st]
        d = os.path.join(out, st)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "expected.py"), inputs, st, d, "--pool-all", pooldir], check=True)
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
    json.dump({"mode": "all states", "states": info["states"], "full_states": pool, "extra_offices": info["extra_offices"],
               "b_scope": b_scope, "description": description},
              open(os.path.join(out, "pool.json"), "w"), indent=1)


if __name__ == "__main__":
    main()

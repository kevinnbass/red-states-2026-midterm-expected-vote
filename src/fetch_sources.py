"""Re-download every source in data/SOURCES.csv that has a URL and compare its sha256 with the recorded one.

Live result pages change (AP feeds, state results sites before certification, pages behind Cloudflare that rewrite bytes), so a
different hash there is expected; archived files, PDFs and fixed datasets should match. Files are written to <out_dir>, never over data/.
Internet Archive captures (web.archive.org) are skipped unless --include-archive is given: fetch them slowly, one at a time.
usage: fetch_sources.py <out_dir> [--only <substring>] [--include-archive]
"""
import csv, hashlib, os, sys, urllib.request

out = sys.argv[1]
only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else ""
os.makedirs(out, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (compatible; red-states-2026-midterm-expected-vote/1.0)"}
same = diff = fail = 0
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "SOURCES.csv"))):
    if not r["url"].startswith("http") or only not in r["url"]:
        continue
    if "archive.org" in r["url"] and "--include-archive" not in sys.argv:
        continue
    dst = os.path.join(out, r["name"])
    try:
        with urllib.request.urlopen(urllib.request.Request(r["url"], headers=UA), timeout=120) as resp:
            data = resp.read()
    except Exception as ex:  # report and go on
        fail += 1
        print("FAILED", r["url"], ex)
        continue
    open(dst, "wb").write(data)
    h = hashlib.sha256(data).hexdigest()
    if h == r["sha256"]:
        same += 1
    else:
        diff += 1
        print("DIFFERENT", r["url"])
print(f"same {same}, different {diff}, failed {fail}")

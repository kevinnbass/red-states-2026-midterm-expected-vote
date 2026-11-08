# CLAUDE.md — red-states-2026-midterm-expected-vote

Expected-vote figures for seven states' 2026 statewide races (same method as texas-2026-midterm-expected-vote).

- Build and check: `./build.sh` (needs matplotlib, Pillow, numpy). `./build.sh --update` overwrites data/derived and figures; only
  after a deliberate input change, then run `tools/write_docs.py .` to regenerate README.md and METHODOLOGY.md.
- Inputs live in `data/inputs/<ST>/statewide_results.csv`; never edit a row without updating its source_url, source_sha256 and notes.
- Every number in README, METHODOLOGY and the web page is generated from the outputs; do not type numbers into them.
- Kansas: sos.ks.gov blocks automated access; do not try to work around it. Iowa: sos.iowa.gov is behind Cloudflare; use Internet
  Archive captures only, one at a time (on the maintainer's machines through `wayback-get`, never direct fetch loops).
- `src/fetch_sources.py` skips web.archive.org unless `--include-archive`.
- Neutral wording: describe results as more Democratic / more Republican; list every race; do not attribute causes.

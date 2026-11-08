#!/usr/bin/env bash
# Rebuild every table, figure and the web page from data/inputs, then compare with the committed copies.
#   ./build.sh            build into build/ and verify against data/derived/ and figures/
#   ./build.sh --update   also copy the new outputs over data/derived/ and figures/ (maintainers, after a data change)
# Needs Python 3.10+ with matplotlib and Pillow (pip install -r requirements.txt).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python3}
OUT=build
rm -rf "$OUT" 2>/dev/null || true
mkdir -p "$OUT"
"$PY" -I src/build_states.py data/inputs "$OUT/states"
"$PY" -I tools/pool_sensitivity.py data/inputs data/inputs/pool50 "$OUT/pool_comparison"
"$PY" -I site/build_page.py "$OUT/states" data/inputs "$OUT/site" $( [ -f site/links.json ] && echo --links site/links.json )
if [ "${1:-}" = "--update" ]; then
  for d in "$OUT"/states/*/; do
    st=$(basename "$d"); s=$(echo "$st" | tr 'A-Z' 'a-z')
    mkdir -p "data/derived/$st" "figures/$s/panels"
    cp "$d"/expected.csv "$d"/races_2018_2022_2026.csv "$d"/one_party_races.csv "data/derived/$st/"
    cp "$d"/fig/"$s"_*.png "figures/$s/"
    cp "$d"/fig/panels/*.png "figures/$s/panels/"
  done
  cp "$OUT/states/pool.json" data/derived/pool.json
  mkdir -p data/derived/pool_comparison && cp "$OUT"/pool_comparison/*.csv data/derived/pool_comparison/
fi
"$PY" -I src/verify.py "$OUT/states" data/derived figures

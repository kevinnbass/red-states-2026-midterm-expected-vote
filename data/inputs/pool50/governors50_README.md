# Governor general-election results, midterm Novembers 1994-2022

Built 2026-11-08 for the midterm-versus-presidential vote comparison. One row per race in `governors_midterm_1994_2022.csv` (289 rows).

## Sources
- Primary: English Wikipedia, API only (`action=parse&prop=wikitext&format=json&redirects=1`), User-Agent `election-analysis/1.0 (research)`, one request at a time with at least 1.2 s pause. Pages: `<YEAR> <State> gubernatorial election` for the 36 states that elect a governor in each midterm year, plus `2010 Utah gubernatorial special election`, plus the eight `<YEAR> United States gubernatorial elections` overview pages (used only to confirm the list of states and spot special elections: every year lists exactly the 36 states, plus Utah's special in 2010; territories are excluded). All 297 pages are saved as fetched in `/mnt/data/projects/election/raw/gov50_wikipedia_20261108/` with `provenance.csv` (utc,url,file,bytes,sha256,http); every request returned HTTP 200. `source_sha256` in the CSV is the sha256 of the saved page file.
- Parsed from the general-election `{{Election box ...}}` template (primary, runoff, polling, county, legislature-vote and city boxes were excluded). Three pages have no results box and were entered by hand from the page's own wikitable or bullet list (AR 1994, NY 2006, NY 2010; see their notes).
- Fusion: a candidate who appears under several party lines (same person, matched on first initial and surname, then eyeballed) has all lines summed in rep_votes/dem_votes and the lines listed in notes. Fusion rows: NY 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022; CT 2010, 2014, 2018, 2022. Wikipedia's own 'Total' fusion lines were used only as a check (they equal the sum of the lines).
- total_votes = the box's total line when present, else the sum of listed candidate and write-in lines (flagged in notes; 'blank ballots' lines excluded). Where the box total differs from the sum of its lines, the box total is kept and the difference is in notes.
- Ranked-choice (AK 2022, ME 2018): first-choice votes. 'rep'/'dem' = the party's nominee, not other candidates carrying the label (e.g. AK 2022 Charlie Pierce, labelled Republican, is not the nominee; AK 1998 Republican write-in Robin Taylor is top_other).

## Races counted per year
| year | rows |
|---|---|
| 1994 | 36 |
| 1998 | 36 |
| 2002 | 36 |
| 2006 | 36 |
| 2010 | 37 | (36 states + 1 Utah special)
| 2014 | 36 |
| 2018 | 36 |
| 2022 | 36 |
| total | 289 |

## Cross-checks
Rows are compared to each available source on the Republican and Democratic sides separately; `crosscheck_diff_*` = my value minus the cross-check value. Where a row has both an official `states_expected` value and an MIT value, `crosscheck_source` lists both (states_expected first), the diff columns use the first, and the MIT difference is in notes.
- `/mnt/data/projects/election/derived/states_expected/<ST>/statewide_results.csv` (office_key governor): TX, OH, IA, SC, AK all eight years; KS 2018, 2022. Compared with `rep_votes_all_lines`/`dem_votes_all_lines` where present (fusion), else `rep_votes`/`dem_votes`. Exception: AK 2022, where the file's all-lines Republican figure (144,449) adds Charlie Pierce's 11,817 (a different candidate on the Republican line); the file's own rep_votes (132,632) is compared.
- 2022 MIT precinct files (`gov2022/x/*.csv`, office GOVERNOR, one pass per file through `wrun --remote -- python3 -I`, ran on worker1): for each precinct+candidate+party key the TOTAL-mode rows are used if present, else the sum of the mode rows. Candidates are matched to my nominee by surname and every party line of that person is summed.
- 2018 MIT precinct file (`gov2018/x/STATE_precinct_general.csv`, 10,379,861 rows, one streaming pass with `csv`, office GOVERNOR only, through `wrun --remote`, ran on worker1; same TOTAL-versus-mode rule).
- Aggregate rows: some MIT files carry aggregate rows next to the precincts (ID 2022: 259 'COUNTY TOTAL' rows, 590,652 votes over all candidates; MI 2022: 14 county-total rows in Mackinac and Keweenaw, 13,392 votes; OR 2018: 9 rows, 13,367 votes). A row whose precinct name contains TOTAL/TOTALS is dropped when its county also has ordinary precinct rows. Without this ID matched at 2x (it is now within 0.4%) and OR 2018 was 0.8% off (it now matches exactly). The scripts and the earlier unfiltered runs (`xc2018_v1_no_total_filter.json`, `xc2018_v2_dropall.json`, and the 2022 equivalents) are left in the scratch folder.
- States of my 36 absent from the 2018 MIT file: IA. Absent from the 2022 MIT folder: AZ, FL, PA, TN. (The 2022 CA file stops at 1,048,575 rows, a spreadsheet limit, but its governor sums are within 0.02% of Wikipedia.) The Louisiana and local-precinct files in the 2022 folder were not used.

Results:
| source | side comparisons | exact | not exact |
|---|---|---|---|
| mit_gov2018 | 70 | 53 | 17 |
| mit_gov2022 | 64 | 40 | 24 |
| states_expected/AK | 15 | 15 | 0 |
| states_expected/IA | 16 | 16 | 0 |
| states_expected/KS | 4 | 0 | 4 |
| states_expected/OH | 16 | 16 | 0 |
| states_expected/SC | 16 | 14 | 2 |
| states_expected/TX | 16 | 13 | 3 |

Rows cross-checked: 98 of 289 (no cross-check exists for the other 191, mostly 1994-2014 rows outside TX/OH/IA/SC/AK). Rows whose every compared side matched the first listed source exactly: 76. Per year (checked / exact): 1994: 5/5, 1998: 5/5, 2002: 5/4, 2006: 5/4, 2010: 5/5, 2014: 5/5, 2018: 36/28, 2022: 32/20.

### Differences over 0.1%
| state | year | source | side | mine | cross-check | diff | diff % | likely reason |
|---|---|---|---|---|---|---|---|---|
| SC | 2002 | states_expected/SC | rep | 585,422 | 580,459 | 4,963 | 0.855 | Wikipedia box (585,422 / 521,140) differs from the scanned official SC report in states_expected (580,459 / 518,288); states_expected already records this as unresolved. Not resolved here; Wikipedia value kept. |
| SC | 2002 | states_expected/SC | dem | 521,140 | 518,288 | 2,852 | 0.550 | Wikipedia box (585,422 / 521,140) differs from the scanned official SC report in states_expected (580,459 / 518,288); states_expected already records this as unresolved. Not resolved here; Wikipedia value kept. |
| AL | 2018 | mit_gov2018 | rep | 1,022,457 | 1,021,276 | 1,181 | 0.116 | MIT precinct file is the unofficial precinct sum; Wikipedia shows a later (likely certified) total (Republican side only, 0.12%; Democratic side 0.07%). |
| KS | 2018 | states_expected/KS | rep | 453,645 | 453,030 | 615 | 0.136 | Wikipedia 453,645 / 506,727 vs states_expected 453,030 / 506,509 (states_expected and the MIT file agree with each other); likely county-canvass certification after the precinct/election-night totals. |
| KS | 2018 | mit_gov2018 | rep | 453,645 | 453,030 | 615 | 0.136 | Same as the states_expected comparison: MIT precinct sum equals the lower pre-certification figure. |
| NY | 2018 | mit_gov2018 | rep | 2,207,602 | 1,866,153 | 341,449 | 18.297 | MIT NY 2018 file is far short of the statewide total (Cuomo -9.6%, Molinaro -15.5% in all-line sum). Wikipedia's all-line totals (Cuomo 3,635,340 incl. WFP, Independence, Women's Equality; Molinaro 2,207,602 incl. Conservative, Reform) sum the same lines MIT carries; the MIT file appears incomplete (not diagnosed further). Wikipedia value kept. |
| NY | 2018 | mit_gov2018 | dem | 3,635,340 | 3,286,344 | 348,996 | 10.620 | MIT NY 2018 file is far short of the statewide total (Cuomo -9.6%, Molinaro -15.5% in all-line sum). Wikipedia's all-line totals (Cuomo 3,635,340 incl. WFP, Independence, Women's Equality; Molinaro 2,207,602 incl. Conservative, Reform) sum the same lines MIT carries; the MIT file appears incomplete (not diagnosed further). Wikipedia value kept. |
| SD | 2018 | mit_gov2018 | rep | 172,912 | 172,706 | 206 | 0.119 | MIT precinct sum below the Wikipedia figure by 0.12% / 0.18%; likely later certification. |
| SD | 2018 | mit_gov2018 | dem | 161,454 | 161,171 | 283 | 0.176 | MIT precinct sum below the Wikipedia figure by 0.12% / 0.18%; likely later certification. |
| AR | 2022 | mit_gov2022 | rep | 571,105 | 569,213 | 1,892 | 0.332 | MIT precinct sum below the Wikipedia figure by 0.33% / 0.76%; likely later certification or precinct-file gaps. |
| AR | 2022 | mit_gov2022 | dem | 319,242 | 316,827 | 2,415 | 0.762 | MIT precinct sum below the Wikipedia figure by 0.33% / 0.76%; likely later certification or precinct-file gaps. |
| CT | 2022 | mit_gov2022 | dem | 710,186 | 709,117 | 1,069 | 0.151 | Democratic side only (0.15%): Wikipedia sums Democratic 691,146 + Working Families 16,175 + Griebel-Frank for CT 2,865 = 710,186; MIT has 709,117 over the same three lines. |
| ID | 2022 | mit_gov2022 | rep | 358,598 | 357,187 | 1,411 | 0.395 | After dropping 259 'COUNTY TOTAL' aggregate rows from the MIT ID file (they double counted), MIT is 0.40% / 0.25% below Wikipedia; likely certification differences or incomplete precinct detail. |
| ID | 2022 | mit_gov2022 | dem | 120,160 | 119,863 | 297 | 0.248 | After dropping 259 'COUNTY TOTAL' aggregate rows from the MIT ID file (they double counted), MIT is 0.40% / 0.25% below Wikipedia; likely certification differences or incomplete precinct detail. |
| ME | 2022 | mit_gov2022 | dem | 376,934 | 375,332 | 1,602 | 0.427 | Democratic side only (0.43%); MIT precinct sum below the Wikipedia figure. |
| MI | 2022 | mit_gov2022 | rep | 1,960,635 | 1,948,292 | 12,343 | 0.634 | MIT MI 2022 file is 0.6% / 1.2% below the Wikipedia figure; the MIT file appears to lack some jurisdictions (not diagnosed further). Wikipedia value kept. |
| MI | 2022 | mit_gov2022 | dem | 2,430,505 | 2,400,628 | 29,877 | 1.245 | MIT MI 2022 file is 0.6% / 1.2% below the Wikipedia figure; the MIT file appears to lack some jurisdictions (not diagnosed further). Wikipedia value kept. |
| NY | 2022 | mit_gov2022 | rep | 2,762,581 | 2,788,149 | -25,568 | -0.917 | MIT is 0.9% / 0.5% ABOVE Wikipedia (Zeldin 2,788,149 vs 2,762,581; Hochul 3,156,467 vs 3,140,415) on the same party lines (Republican+Conservative; Democratic+Working Families); likely the Wikipedia box shows a pre-certification count. Not resolved. |
| NY | 2022 | mit_gov2022 | dem | 3,140,415 | 3,156,467 | -16,052 | -0.509 | MIT is 0.9% / 0.5% ABOVE Wikipedia (Zeldin 2,788,149 vs 2,762,581; Hochul 3,156,467 vs 3,140,415) on the same party lines (Republican+Conservative; Democratic+Working Families); likely the Wikipedia box shows a pre-certification count. Not resolved. |
| SC | 2022 | mit_gov2022 | rep | 988,501 | 991,882 | -3,381 | -0.341 | MIT SC file is 0.34% / 0.37% above Wikipedia; Wikipedia equals the official figure in states_expected exactly (988,501 / 692,691), so the MIT file is the odd one out (possible duplicated or non-statewide rows). |
| SC | 2022 | mit_gov2022 | dem | 692,691 | 695,280 | -2,589 | -0.372 | MIT SC file is 0.34% / 0.37% above Wikipedia; Wikipedia equals the official figure in states_expected exactly (988,501 / 692,691), so the MIT file is the odd one out (possible duplicated or non-statewide rows). |

No difference above 0.1% was traced to a parse error in my extraction (the parsed values equal the Wikipedia boxes; the candidate sets and party lines were checked by eye for every fusion row). The Wikipedia value is kept in every case. All differences of 0.1% or less but not zero:

TX 2006 states_expected/TX rep: 1,716,803 vs 1,716,792 (+11, +0.001%); TX 2006 states_expected/TX dem: 1,310,353 vs 1,310,337 (+16, +0.001%); AL 2018 mit_gov2018 dem: 694,495 vs 694,011 (+484, +0.070%); CT 2018 mit_gov2018 rep: 650,138 vs 650,132 (+6, +0.001%); CT 2018 mit_gov2018 dem: 694,510 vs 694,509 (+1, +0.000%); FL 2018 mit_gov2018 rep: 4,076,186 vs 4,076,521 (-335, -0.008%); FL 2018 mit_gov2018 dem: 4,043,723 vs 4,044,092 (-369, -0.009%); KS 2018 states_expected/KS dem: 506,727 vs 506,509 (+218, +0.043%); KS 2018 mit_gov2018 dem: 506,727 vs 506,509 (+218, +0.043%); PA 2018 mit_gov2018 rep: 2,039,882 vs 2,040,169 (-287, -0.014%); PA 2018 mit_gov2018 dem: 2,895,652 vs 2,895,848 (-196, -0.007%); TX 2018 mit_gov2018 rep: 4,656,196 vs 4,655,344 (+852, +0.018%); TX 2018 mit_gov2018 dem: 3,546,615 vs 3,545,673 (+942, +0.027%); VT 2018 mit_gov2018 rep: 151,261 vs 151,249 (+12, +0.008%); CA 2022 mit_gov2022 rep: 4,462,914 vs 4,462,336 (+578, +0.013%); CA 2022 mit_gov2022 dem: 6,470,104 vs 6,469,743 (+361, +0.006%); KS 2022 states_expected/KS rep: 477,591 vs 477,586 (+5, +0.001%); KS 2022 states_expected/KS dem: 499,849 vs 499,845 (+4, +0.001%); KS 2022 mit_gov2022 rep: 477,591 vs 477,586 (+5, +0.001%); KS 2022 mit_gov2022 dem: 499,849 vs 499,845 (+4, +0.001%); ME 2022 mit_gov2022 rep: 287,304 vs 287,087 (+217, +0.076%); NV 2022 mit_gov2022 rep: 497,377 vs 497,147 (+230, +0.046%); NV 2022 mit_gov2022 dem: 481,991 vs 481,872 (+119, +0.025%); NM 2022 mit_gov2022 rep: 324,701 vs 324,665 (+36, +0.011%); NM 2022 mit_gov2022 dem: 370,168 vs 370,125 (+43, +0.012%); OR 2022 mit_gov2022 dem: 917,074 vs 917,034 (+40, +0.004%); TX 2022 states_expected/TX rep: 4,435,558 vs 4,437,099 (-1,541, -0.035%); TX 2022 mit_gov2022 rep: 4,435,558 vs 4,437,097 (-1,539, -0.035%); TX 2022 mit_gov2022 dem: 3,553,656 vs 3,554,772 (-1,116, -0.031%).

## Blank sides
- AK 2014: dem_votes blank. no Democratic nominee in the Wikipedia results box (blank) | Democratic nominee Byron Mallott withdrew from the top of the ticket to run as lieutenant governor on Bill Walker's independent ticket, so no Democrat is on the ballot line: dem_votes left blank (Walker is top_other).
- No other row has a blank nominee side; no row had to be blanked because only a minor-party candidate carried the label.

## Other notes
- States that elect governors in presidential or odd years (including Louisiana) and territories are out of scope.
- Vermont: popular vote is reported; in years where no candidate reached a majority the legislature decides the winner (not checked per year here).
- Rhode Island 2010 and Maine 1994/1998/2006/2010 and others: an independent finished first or second; shown as top_other.
- AR 1994's only source is the page's bullet list (two candidates), so its total_votes may omit minor candidates.
- Wikipedia numbers are secondary and some pages are unreferenced; the cross-checks cover about a third of the rows.
- Wrong or superseded scratch outputs are left in `/mnt/work/gov50_helper_20261108/` (nothing was deleted). Scripts: fetch.py, parse.py, extract.py, build.py, xcheck.py, xcheck_precinct.py, final.py, readme.py.

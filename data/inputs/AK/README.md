# Alaska statewide results, midterm years 1994-2026

Built 2026-11-08. Raw files and hashes: /mnt/data/projects/election/raw/states_history/AK/ (provenance.csv). Output: statewide_results.csv (23 rows).

## Offices
2026 ballot statewide: Governor/Lt. Governor, U.S. Senate (Sullivan seat), U.S. House (at-large, statewide). All three collected. Senate races occurred in 1998, 2002, 2010, 2014, 2022 (none in 1994, 2006, 2018). No special elections in November.

## Sources per year (numbers of record = Division of Elections)
- 2026: elections.alaska.gov/enr/26GENR/results/ElectionSummaryReportRPT.pdf (generated 11/4/2026 1:09:44 PM, 400 of 401 precincts). The results page says "Page last updated November 4, 2026 at 2:45 am". UNOFFICIAL. Ranked-choice tabulation has NOT happened; the Division schedules it for November 18, 2026. First-choice votes recorded. Cross-check: the Division's own precinct CSV sums to the identical totals (diff 0); no independent second source was available. The Division's "Combined Report" html (11.5.26) is behind a captcha and was not fetched (the saved file is the captcha page, http 405).
- 2022: official Election Summary Report (11/30/2022) for first-choice votes; RCV Detailed Reports (11/23/2022, labeled unofficial) for final rounds (Senate and House). No governor RCV report exists (404); Dunleavy won a first-round majority.
- 2018, 2014, 2006, 2002, 1998: Division GEMS official results pages (results18.htm, results.htm, Core/Archive/02GENR, 98GENR/results.htm).
- 2010: governor and House from Division resultsOF.htm ("without US Senate race"); Senate from the Wayback capture (2014-08-20) of the Division's removed results.htm, fetched through wayback-get; Murkowski write-in count from resultsWI.htm (12/28/10).
- 1994: Division statewide summary result94.php (recount figures). The page is captcha-gated for scripts, so the numbers came from a search-engine extract and no file is saved. Cross-check matched Wikipedia (87,157 R / 87,693 D).

## Rules applied
- rep_votes/dem_votes: first-choice votes of the leading Republican and the Democratic nominee. rep_votes_all_lines = sum of all Republican-labelled candidates in that race (only differs in 2022 and 2026; Alaska has no fusion lines). Others in notes.
- 2014 governor: dem_votes blank (Walker independent, Mallott the Democratic running mate); 2010 Senate: Miller as Republican, Murkowski write-in (101,091) in notes; 2026 House independent Bill Hill and 2022 governor independent Walker not substituted.
- 2026 governor Democratic ticket is coded DEM/NON on the report (Kreiss-Tomkins/Johnson); recorded as the Democratic line.
- 2026 Senate: "Sullivan, Daniel J. Jr." has no party shown and is not counted as Republican.

## Gaps
- 1994 U.S. House: no row (official page not retrievable; precinct PDF could not be summed reliably). Wikipedia lists Young 118,537, Smith 68,172, Whitmore 21,277, total 208,240 (unverified).
- 1994 governor: no source file or hash saved (see above); total_votes 213,435 includes 277 write-ins taken from Wikipedia.
- 2022 and 2026 final ranked-choice rounds: 2026 not yet run; 2022 governor needed none.

## Discrepancies with cross-checks
- 2022 Senate (over 0.5%): Division summary 113,495 R (Murkowski) / 27,145 D (Chesbro), total 261,705. MIT Election Lab file has 114,118 / 28,233, total 263,526 (diff -623, -0.55%; -1,088, -3.9%). The Division's own RCV report (11/23/2022) has round 1 at 113,800 / 28,185. Official 11/30 summary retained; the sources reflect different count dates or definitions.
- 2022 House RCV final: Division 11/23 report Peltola 136,893 vs Palin 112,255; Wikipedia 137,263 vs 112,471 (0.3%); Wikipedia first-choice matches the official summary.
- 2014 House: official 142,572 / 114,602; Wikipedia 142,260 / 114,317 (0.22%, 0.25%).
- 2010 Senate total: archived official page 255,962 vs MIT 255,503 (0.18%); Miller and McAdams agree exactly.
- All other race rows agree with their cross-check exactly (MIT for Senate, Wikipedia election boxes for governor and House).
- 2018 folder note: results.htm in 18GENR is a stale 09/19/18 template with zeros; results18.htm is the official page.

## Method notes
elections.alaska.gov sends an incomplete certificate chain; downloads used the correct GlobalSign intermediate (from the certificate's own AIA URL) as an added trust anchor, with verification kept on.

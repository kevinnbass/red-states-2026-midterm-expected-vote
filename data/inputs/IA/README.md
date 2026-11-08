# Iowa statewide results, midterm years 1994-2026 (statewide_results.csv)

Built by `build_statewide_results.py` from `rows_data.py` (values read from the saved files in /mnt/data/projects/election/raw/states_history/IA/; every download is in provenance.csv with sha256). One row per race. `rep_votes` / `dem_votes` are each nominee's votes on his or her own party line; `*_all_lines` equal them (no Iowa nominee here appeared on another party's line, so no combined totals differ). `total_votes` = sum of all candidates plus write-ins/scattering, excluding under- and over-votes (same convention as the MIT Senate file). A blank candidate/vote cell means that party had no nominee.

## Status of the numbers (read this first)
The Iowa SOS site (sos.iowa.gov) sits behind a Cloudflare challenge that refuses every automated request, and I did not try to defeat it. Official canvass PDFs were therefore obtained only as Internet Archive captures through the host's wayback-fetchd queue (30-minute backoffs between files). Rows by source quality:

| Year | Source of the numbers | Status in this file |
|---|---|---|
| 1994 | SOS 1994 General Canvass Summary (scanned PDF, web.archive.org capture). Read from page images; every race's candidates + scattering equal the printed race total. | official, number of record |
| 1998 | Senate: OpenElections (agrees with MIT). Governor: Wikipedia only. Other offices: NOT FILLED. The guessed URL 1998gencanv.pdf is 404; the real file is pdf/10-8.pdf, requested, pending. | secondary |
| 2002 | SOS "Canvass Summary FINAL" (2002-12-02; Internet Archive capture), statewide Totals rows for Senate, Secretary of State, Auditor, Treasurer, Agriculture, Attorney General; all equal OpenElections and (Senate) MIT exactly. Governor is not in that file: OpenElections (matches Wikipedia); SOS governor file not yet found. | official except Governor (secondary) |
| 2006 | OpenElections, same. No SOS PDF URL found yet. | secondary |
| 2010 | OpenElections, same. (The 2010 `canvsummary.pdf` on the SOS site is the PRIMARY election report; saved as IA_2010_PRIMARY_canvsummary_not_general.pdf and not used.) SOS gensummaryorr.pdf requested, pending. | secondary |
| 2014 | SOS 2014 General canvass summary PDF plus govcanvsummary.pdf for Governor (text layers), statewide TOTAL row of each contest. | official |
| 2018 | OpenElections; totals from Wikipedia election boxes. SOS PDF (2018/general/canvsummary.pdf) requested, pending. | secondary |
| 2022 | SOS 2022 General canvass summary PDF plus govcanvsummary.pdf for Governor (text layers). | official |
| 2026 | Unofficial. Governor, U.S. Senate, Secretary of State, Attorney General: AP via NPR (file /mnt/data/projects/election/raw/ap_npr_20261108T0505Z/states/IA.json, AP records updated 2026-11-07 ~17:29Z, eevp 0.985-0.990, 1656 of 1656 precincts). Auditor, Treasurer, Agriculture: Iowa SOS Clarity feed (AP does not carry them). | unofficial |

Rows marked SECONDARY in `notes` use a source that is not the SOS number of record; the coordinator will rerun the builder when the PDFs arrive. Secondary-source values agreed with every cross-check available (below).

## 2026
Statewide offices on the 2026 ballot (from the Clarity feed, election 127077, "2026 General Election"): U.S. Senator, Governor and Lt. Governor, Secretary of State, Auditor of State, Treasurer of State, Secretary of Agriculture, Attorney General. These are exactly the seven requested; none added or dropped.
Clarity "Last updated": **11/4/2026 12:25:40 PM CST** (file Last-Modified Wed 4 Nov 2026 18:25:20 GMT), 95 of 99 counties reporting. It was fetched twice (2026-11-08T04:32Z and again after the coordinator's request); the content is byte-identical, so the SOS site has not updated since 11/4. For the Clarity-sourced offices, those numbers are 4 counties short of complete. AP-minus-Clarity differences for the four AP offices are 130-220 votes per candidate (about 0.03%).
AP totals (Governor, SoS, AG) cover only the two major candidates AP lists; write-ins and minor candidates are not in those totals.

## Cross-checks and discrepancies
- Cross-check diff columns = source value minus cross-check value (0 = exact match). Cross-checks used: MIT Election Lab Senate file (Senate 1998, 2002, 2010, 2014); Wikipedia election boxes (Governor 1994, 2002, 2006, 2010; 2014 Auditor and AG; all 2018 races; all 2022 races except Governor).
- Every candidate-vote cross-check matches exactly. No candidate-vote discrepancy exists over 0.5%.
- Total-vote notes: 2022 Secretary of Agriculture: canvass total 1,194,707 vs Wikipedia 1,202,707 (0.67%; Wikipedia looks mistyped, canvass candidate lines + write-ins + under/over reproduce the printed 1,230,416). 2022 Attorney General: Wikipedia total omits 801 write-ins. 2018 OpenElections has no write-in rows, so the Wikipedia total is used. 2006/2010 OpenElections TOTAL rows include under-votes, so totals here were recomputed from candidate rows and agree with Wikipedia's Governor and MIT's Senate totals.
- No second source found (cross-check left blank): 1994 Secretary of State, Auditor, Treasurer, Agriculture, Attorney General; 2014 Secretary of State, Treasurer, Agriculture (Wikipedia pages missing or wrong); all 2026 rows for the Clarity-sourced offices; 2002/2006/2010 down-ballot offices (only OpenElections so far).

## Gaps
- 1998: Secretary of State, Auditor, Treasurer, Agriculture, Attorney General not filled (waiting for the SOS PDF). Wikipedia pages for those races do not exist.
- No Senate race in 1994, 2006, 2018 (none on the ballot). No special elections in the window (special = 0 everywhere).
- Uncontested sides: 2006 Auditor (no Democrat), 2006 Treasurer (no Republican), 2006 Attorney General (no Republican); 2018 Attorney General (no Republican; Libertarian Marco Battaglia had 262,131). In 2006, 2018 these rows have one party blank.
- The 2006 down-ballot OpenElections values came from a hand-cleaned text conversion (per OpenElections README), so verify them against the SOS PDF when it arrives.
- Governor Lt. Governor names are given where the source gave them; 1998 and 1994 running mates only partly captured.

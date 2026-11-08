# Ohio statewide results, midterm years 1994-2026 (compiled 2026-11-08 UTC)

Output: `statewide_results.csv` (one row per race). Raw files and provenance: `/mnt/data/projects/election/raw/states_history/OH/` (`provenance.csv` lists every download: utc, url, file, bytes, sha256, http).

## The main limitation: the Ohio Secretary of State site could not be used
ohiosos.gov and publicfiles.ohiosos.gov (and liveresults.ohiosos.gov) answer every automated request with an HTTP 403 Cloudflare bot challenge ("Enable JavaScript and cookies to continue"), also with a browser-style User-Agent. Ohio is already on the project's permanent no-automation list (src/browser/visits.py). I did not try to get past the challenge. Instead the official SOS files were taken from Internet Archive captures of the same ohiosos.gov / sos.state.oh.us pages and workbooks (fetched through the host's wayback-get queue; the queue was in a 30-minute machine-wide backoff for most of the session, which limited how many captures could be fetched). Where no SOS file could be fetched (2006 and the 2026 count), the number comes from a named secondary copy and the row's notes say so; 2006 is the SOS statewide precinct file as republished by OpenElections. **Every row's `source_sha256` is the hash of the file named in `source_file`.**

## Sources used per year
| year | numbers of record | cross-check |
|---|---|---|
| 1994 | SOS "General Election: November 8, 1994" official tabulation page (Internet Archive capture, sos_archive/) | Wikipedia election boxes; MIT Senate file |
| 1998 | SOS "Overview: November 3, 1998" official tabulation page (Internet Archive capture) | Wikipedia; MIT Senate file |
| 2002 | SOS "Recapulation, November 5, 2002" page (Internet Archive capture) | OpenElections 2002 county file summed over 88 counties; Wikipedia |
| 2006 | Ohio SOS official 2006 statewide precinct file as republished by OpenElections (gen06statewide.csv; the SOS page captures were not retrieved) | Wikipedia; MIT Senate file |
| 2010 | SOS 2010 general-election results pages for each office ("Amended Official Results" where so headed; Internet Archive captures of the original sos.state.oh.us pages, Total row) | Wikipedia election boxes; MIT Senate file |
| 2014 | SOS official results workbook results.xlsx (Internet Archive capture 2020-06-12) | OpenElections county file; Wikipedia |
| 2018 | SOS "Official Canvass (As Amended by the Miami County Board of Elections)" workbook 2018-11-06_statewidecounty_miami.xlsx (Internet Archive capture 2025-03-06) | MEDSL 2018 Ohio precinct rows; Wikipedia (Senate) |
| 2022 | SOS official canvass workbook statewide-races-summary.xlsx (Internet Archive capture 2022-12-29) | MEDSL 2022 Ohio precinct file; Wikipedia |
| 2026 (unofficial) | AP/NPR race feed already saved at /mnt/data/projects/election/raw/ap_npr_states_20261108/OH.json (Governor, Senate special, AG, Secretary of State); Wikipedia pages for Auditor and Supreme Court | Wikipedia vs AP where both exist |

Wikipedia is the only source for a number of record in just three places, all flagged in the notes: 2026 Auditor and the two 2026 Supreme Court races.

## 2026 (unofficial) and last-updated time
The Ohio SOS unofficial results site is blocked (above), so **no SOS "last updated" time exists in this data**. The AP feed last updated Governor and Senate on 2026-11-06 21:33:13 UTC and AG/Secretary of State a few seconds later (97.7% of precincts reporting); the Wikipedia Auditor page says "est. 98% in". 2026 numbers are therefore an AP count, not the SOS count, and will move.

Offices on the 2026 ballot (confirmed from the AP feed and the Wikipedia 2026 pages, not from the SOS site): Governor/Lieutenant Governor (joint ticket), Attorney General, Secretary of State, Auditor of State, Treasurer of State, U.S. Senate (special election for the Vance seat, `special=1`), and two Ohio Supreme Court seats (Brunner seat and Hawkins seat). There is no Chief Justice race (Kennedy was elected in 2022) and no separately elected Lieutenant Governor, so nothing was added or dropped from the requested list.

## What is filled (R+D = both party vote columns present)
| office | 1994 | 1998 | 2002 | 2006 | 2010 | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| governor | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D |
| attorney_general | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D |
| secretary_of_state | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D |
| auditor | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D |
| treasurer | R+D | R+D | R+D | R+D | R+D | R+D | R+D | R+D | names only |
| us_senate | R+D | R+D | - | R+D | R+D | - | R+D | R+D | R+D |
| supreme_court | total only/total only | total only/total only/total only | total only/total only | total only/total only | total only/total only/total only | total only/total only | total only/total only | R+D/R+D/R+D | R+D/R+D |

(supreme_court cells with "total only" have no party label in the official source, so only the race total is filled and the candidates and their votes are in `notes`.)

## Gaps
- U.S. Senate: no Ohio Senate election in 2002 or 2014 (checked against the MIT file, which has no Ohio rows for those years).
- Ohio Supreme Court, 1994-2018: the general-election ballot was nonpartisan and none of the official sources gives party affiliation, so `rep_*`/`dem_*` are blank; candidate names and votes are in `notes`. 2022 and 2026 carry party labels. The 2006, 2010 and 2014 Supreme Court totals have no second source with votes.
- Ohio Supreme Court 2010 seat with term beginning Jan 2, 2011 was uncontested (Pfeifer alone, 2,384,122); recorded as total only.
- 2026 Treasurer: the nominees are known (Jay Edwards R, Seth Walsh D) but no vote counts were found (Wikipedia gives only percentages; AP feed lacks the race), so the vote columns are blank.
- 2026 Auditor and Supreme Court: single source (Wikipedia, citing an about 98% count); no cross-check.
- Running mates: 2006 governor rows list the head of ticket only (the source files do not name running mates).
- Ohio does not appear to have fusion voting: no candidate name appears on more than one party line in any file used, so `*_votes_all_lines` equals `*_votes`. I did not verify the statute.

## Discrepancies with the cross-check (nonzero differences, primary minus cross-check)
- 1998 treasurer (TREASURER OF STATE): R diff -10 (0.00%), D diff +0 (0.00%) vs Wikipedia election box (1998_Ohio_State_Treasurer_election.w
- 2006 us_senate (U.S. Senate (Nov 7, 2006)): R diff +55 (0.00%), D diff +116 (0.01%) vs MIT Election Lab 1976-2024-senate-state.tab

Over 0.5%: none.

Notes on specific differences:
- 2018: SOS also posted an earlier, un-amended "Official Canvass" workbook (saved as sos_archive/xlsx_2018_gen_statewidecounty.xlsx) that is lower than the amended workbook used here by about 3,900 R and 2,100 D votes in every statewide race (0.1-0.2%) because Miami County's amended returns were added afterwards. The CSV uses the amended figures (they equal MEDSL and, for the Senate and Supreme Court, Wikipedia). The MIT Election Lab Senate file carries the un-amended Senate figures (R 2,053,963, D 2,355,923).
- 1998 Treasurer: SOS page says Deters 1,719,133; Wikipedia says 1,719,143 (10 votes, Wikipedia typo likely).
- 2006 U.S. Senate: the SOS precinct file (via OpenElections) gives Brown 2,257,485 / DeWine 1,761,092; the MIT file has 2,257,369 / 1,761,037 (0.005%).
- Several Wikipedia "total" rows do not equal the sum of the candidate lines (e.g. 1994 auditor, 2010 attorney general); `total_votes` here is always the sum of the candidate lines in the source and the notes flag the Wikipedia total when it differs.
- 2018 Auditor: Wikipedia's own pages disagree with each other for Space (2,008,925 vs 2,008,295); the second equals the amended SOS workbook.

## Method notes
- `total_votes` = sum of every candidate line the primary source lists for the office. Sources that carry no write-in lines (1994/1998/2002 pages list only the candidates shown, 2006 precinct file, 2014 workbook) therefore exclude write-ins; the 2010 pages (Write In column where present), 2018 and 2022 workbooks include them.
- `status` is `official` for every historical row (certified results), `unofficial` for 2026.
- Hygiene: the output folder also holds a stray `statewide_results.csv.new` (an earlier draft written before I settled on one write; I cannot delete under /mnt). It is superseded by `statewide_results.csv`. Likewise `raw/states_history/OH/medsl/oh18.csv` is an earlier extract that accidentally included rows from other states whose county names contain "OHIO"; use `oh18_OH_only.csv`.
- Cross-check diffs are primary minus cross-check, in votes.

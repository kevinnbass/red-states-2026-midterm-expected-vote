# Indiana statewide results (SoS, Auditor, Treasurer, U.S. Senate), midterm years 1994-2026

Output: statewide_results.csv (33 rows). Raw files and provenance.csv: /mnt/data/projects/election/raw/states_history/IN/

## Offices on the 2026 ballot (from the state's 2026 ENR file statewideElectionsC_B.json)
Statewide: Secretary of State, State Comptroller (Auditor of State), Treasurer of State. No U.S. Senate, Governor or Attorney General race in 2026. (Also U.S. House, legislature, judicial and local, not collected.) The Auditor office is titled "State Comptroller (Auditor of State)" in 2026; office_key stays `auditor`.

## Sources by year
- 2002, 2006, 2010, 2014, 2018, 2022: Indiana Election Division / Secretary of State "Historical Election Results" (indianavoters.in.gov/ENRHistorical), CSV export per year (General). Statewide rows only; total_votes = sum of all statewide candidate rows including write-ins. Page says "These results are final" (page text "Last Updated August 19, 2016" is the same on every year's page, not per-year). Number of record.
- 1994, 1998: the state publishes nothing online before 2002 (its own page says so: federal results before 2002 are at the Clerk of the House). SoS, Auditor and Treasurer come from Capitol & Washington (capitolandwashington.com), a secondary aggregator, status `unofficial`. Each race's candidate votes sum exactly to its stated race total, and the same site matches the state official file exactly wherever both exist, but these 1994/1998 numbers are NOT confirmed against a state document. U.S. Senate 1994/1998 from the MIT Election Lab file; the major-party totals also appear in the Wikipedia pages.
- 2026: state ENR site https://enr.indianavoters.in.gov/site/data/ (settings.json, OffCatC_<id>_B.json), unofficial, Certified=F. 4,831 of 5,067 precincts reporting. Last updated: site settings WriteTime 2026-11-07T23:07:07 (VersionCode 20261107_230206); race files written 23:04-23:05 (same date). The site does not state a time zone. I fetched it 2026-11-08 ~04:30 UTC, so the count may have moved since; settings were re-fetched once and unchanged (enr2026_settings_recheck.json).

## Cross-checks
- Capitol & Washington pages cover: SoS 1994/98/2002/2010/2022; Auditor 1994/98/2006/2014; Treasurer 1994/98/2002/2006/2014/2022. For the state-sourced years among them (2002-2022), R and D candidate votes and race totals agree exactly (0 difference).
- U.S. Senate 2006-2022 vs MIT Election Lab: 2006, 2010 exact; 2018 state is higher: R +0.306%, D +0.159% (MIT 1,158,000 / 1,023,553; state 1,161,546 / 1,025,178; the state file's race total 2,287,947 vs MIT 2,282,565, +0.24%); 2022 R +0.021%, D +0.010%. No difference exceeds 0.5%. I use the state numbers.
- 2026: no independent source. Internal check only: the 92 county rows in each office file sum to the statewide totals (diff 0).

## Gaps (crosscheck column blank = no second source obtained)
- No second source obtained (crosscheck columns blank): SoS, Auditor, Treasurer 1994 and 1998 (single secondary source); Auditor 2002, 2010, 2018, 2022; Treasurer 2010, 2018; SoS 2006, 2014, 2018. Not searched for these: Wikipedia election boxes or OpenElections (a search found no OpenElections Indiana repository; not confirmed).
- U.S. Senate: none in 2002 or 2014 (no race); none in 2026. 2006 has no Democratic nominee (Lugar unopposed by a Democrat; two write-ins listed, one "W/I (Democratic)" with 294 votes, not treated as the nominee), dem_votes blank. 1994/1998 are not special elections; no special Senate elections in these years.
- Every office-year in the other cells had both an R and a D nominee. No nominee appeared on more than one party line (no fusion in Indiana), so *_all_lines equals the own-line votes.
- Raw files enr_initApp.js and enr_jsonDataFetcher.js are HTTP 400 error bodies from a wrong path (logged 400 in provenance.csv); enr_initApp_site.js / enr_jsonDataFetcher_site.js are the real files. hist_2002/2006/2010/2014.html are the same filter page. wp_*_sos/_elections/_aud/_tre files are Wikipedia 404 pages (no such articles).
- status values: official (2002-2022), unofficial (2026 and 1994/1998 secondary data; the contract allows only official/unofficial, so 1994/98 are flagged unofficial and explained in notes).

## Discrepancies over 0.5%
None.

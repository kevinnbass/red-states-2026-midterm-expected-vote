# South Carolina statewide results, midterm years 1994-2026

Output: statewide_results.csv (82 rows). Raw files and provenance.csv: /mnt/data/projects/election/raw/states_history/SC/

## Sources (number of record = SC State Election Commission)
- 1994, 1998, 2002: Election Commission "Election Report" PDFs (scvotes.gov/wp-content/uploads/2022/08/). Scanned images; read from rendered page images (1994 headers have stacked-letter names; state-total row for Governor and Lt Governor is run together and was read from a 250 dpi crop). No OCR software used.
- 2006: Election Report 2005-2006 PDF (text layer).
- 2010, 2014, 2018, 2022, 2026: Clarity/ENR detail.xml (enr-scvotes.org), latest published version of each: 2010 v40477, 2014 v149816, 2018 v242328, 2022 v313728, 2026 v386034.
- 2026 is UNOFFICIAL. Snapshot timestamp in the file: 11/6/2026 6:25:28 PM EST (all 2,312 precincts reported). ENR current_ver was still 386034 when checked 2026-11-08T04:39Z. Not certified.

## 2026 ballot
Statewide offices on the 2026 ballot (ENR): Governor/Lt Governor (joint), Secretary of State, Treasurer, Attorney General, Comptroller General, Superintendent of Education, Commissioner of Agriculture, U.S. Senate. Adjutant General was NOT on it (appointed since 2019) so there is no 2026 row. Senate nominee for R is Darline Graham (confirmed by news reports).

## Cross-checks
- 2006: OpenElections county file; 2018 and 2022: OpenElections precinct files (summed party lines): exact agreement on R and D for every office.
- 2010, 2014: Wikipedia election boxes (which cite the same ENR) for all offices except Senate; exact agreement. Senate 1998, 2002, 2010, 2014 (regular and special): MIT Election Lab file.
- 1994 and 1998 Governor: Wikipedia; exact agreement (Wikipedia 1994 omits John Peeples (U) 8,003).
- Wikipedia boxes were parsed partly by regex; for 2010 Governor Sheheen and the 1994 Theodore figures were confirmed by direct grep.
- No second source found for: 1994 and 1998 down-ballot offices, 2002 down-ballot offices, 2026 (news items quote earlier, lower snapshots that are not comparable). Those rows have blank crosscheck columns. I did read each total row twice from page images but that is not independent.

## Discrepancies (over 0.5%)
- 2002 Governor: official report R 580,459 / D 518,288 vs Wikipedia 585,422 / 521,140 (R -0.85%, D -0.55%).
- 2002 U.S. Senate: official report R 595,218 / D 484,422 vs MIT 600,010 / 487,359 (R -0.80%, D -0.60%).
Both are the same direction and size, so Wikipedia/MIT may carry later-corrected totals, but this is not confirmed. I kept the report's numbers (rows verified against rendered images). Smaller: 1998 Senate vs MIT R -106 (0.02%), D -586 (0.10%).

## Fusion
Recorded in rep_votes/dem_votes (own party line) with *_all_lines the combined total:
2014 Senate Hutto (D 456,726 + Working Families 24,207); 2018 Treasurer Glenn (+28,777 WFM); 2018 AG Anastopoulo (+35,112 WFM); 2022 Superintendent Ellis (+52,995 Alliance). 2006 Working Families nominees were added to the ballot but the report prints only party lines; any such votes are inside the D totals as printed.

## Gaps / empty sides
- No Democratic nominee: 1998 Agriculture; 2002 Adjutant General; 2006 Attorney General; 2010 Treasurer, Adjutant General; 2014 Treasurer, Adjutant General, Agriculture (Edmond ran United Citizens); 2018 Comptroller, Superintendent, Agriculture; 2022 Treasurer (Alliance candidate Work), Attorney General, Comptroller, Agriculture.
- No Republican side missing in any row.
- Adjutant General elected through 2014 only (none 2018+). U.S. Senate: races in 1998, 2002, 2010, 2014 (two), 2022, 2026 only; none 1994, 2006, 2018. Lt Governor separate through 2014; joint ticket from 2018 (stored under governor).
- Total_votes = sum of every line in the race including write-ins.
- 1994 names Bunch (Lt Gov), Hendrix, Childers, Weinberg, Baker were read from stacked-letter headers; spelling may be off by a letter.
- Housekeeping: three early downloads (SC 2008/2010/2014 detailxml zips) were misfiled by a shared helper script into the AK folder (/mnt/data/projects/election/raw/states_history/AK/) and their rows are in AK provenance.csv; they were re-downloaded here. Error-page files wp/wp_1994|1998|2002_SC_elections.wikitext (HTTP 404) remain because deletion is blocked.

## 2002 check (main session, 2026-11-08)
- The 2002 report's 46 county rows sum exactly to its printed state totals (Governor D 518,288 / R 580,459; U.S. Senate D 484,422 / R 595,218), so the gap is not a reading error.
- The House Clerk's "Statistics of the Congressional Election of November 5, 2002" (official, from the state's certified results; saved as raw/results/clerk/statistics2002.pdf, sha256 e041d83f...) gives Graham 600,010, Sanders 487,359, Adams 8,228, Kocher 6,648, write-in 667. Kocher and write-ins are identical to the report; Adams is +26; only the two major-party columns are higher (R +4,792, D +2,937).
- Governor (Wikipedia, secondary) differs by a similar amount (R +4,963, D +2,852). The same set of ballots appears to be missing from the report's precinct tables for both races; the source of the difference is not documented.
- Kept: the report's numbers, so that all 2002 offices rest on the same ballots. Effect: one of up to eight baseline years, about 0.6-0.85% in that year, so under 0.1% on a 2026 expected vote.

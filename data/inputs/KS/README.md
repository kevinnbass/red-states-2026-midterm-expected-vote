# Kansas statewide results (partial) - 2026-11-08

## Main problem
The Kansas Secretary of State site (sos.ks.gov, CloudFront) answers 403 "Request blocked" to curl with a browser-style
User-Agent, and the election driver (`drive.py`) refuses the host permanently ("by hand only", Kevin 2026-10-14/15).
I did not work around it (no Internet Archive copies, no other tools). So NO row here comes from the SOS canvass.
Kevin needs to download the SOS general-election canvass files by hand (1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, and the
2026 unofficial site) into /mnt/data/projects/election/raw/states_history/KS/.

## What is in statewide_results.csv and where it came from
- 2014 Secretary of State, Attorney General, Treasurer, Insurance Commissioner: OpenElections precinct file, 2014-11-04,
  using only its "Last, First" candidate rows (the file also holds a second, "First Last" set of rows that does not add to the
  county totals; including it double counts). R and D match Wikipedia exactly (0.00%). total_votes includes write-ins
  (differs from Wikipedia total by 0.03%).
- 2018 Governor, Secretary of State, Attorney General, Treasurer: OpenElections precinct file, 2018-11-06, all candidate-row
  variants summed. All are 0.03-0.14% below Wikipedia (OpenElections slightly undercounts).
- U.S. Senate 1998, 2002, 2010, 2014, 2022: MIT Election Lab file (local). 2014 R/Orman cross-checked exactly to
  OpenElections. Others have no second source. No Senate race in 1994, 2006, 2018 (Kansas classes: 1996/2002/2008/2014/2020 and
  1998/2004/2010/2016/2022). 2002 and 2014 have no Democratic nominee (2014: independent Greg Orman, 368,372, not recorded as D).
  MIT's 2022 Libertarian is split over three spellings; irrelevant to R/D.
- status is "official" but note the source is secondary, not the canvass. Crosscheck "Wikipedia" values were read from page text via
  WebFetch summaries (saved as wikipedia_crosscheck_values.csv, not raw pages).

## Gaps
- No rows at all: 1994, 1998 (state offices), 2002, 2006, 2010 (state offices), 2022 (state offices), 2026 (everything). OpenElections KS has
  no statewide general files for those years.
- 2014 Governor: OpenElections precinct sums are incomplete or duplicated (Brownback 422,616 vs 433,196 Wikipedia; Umbehr 44,698 vs 35,206), so omitted.
  Wikipedia values (433,196 / 401,100 / total 869,502) are only a lead.
- 2018 Insurance Commissioner: OpenElections misses ~22% of Vicki Schmidt's votes (500,391 vs 644,293 Wikipedia), so omitted.
- 2026: election was 2026-11-03; no results found online (search), SOS unofficial site not reachable. No "last updated" time exists.
  Ballot offices were not confirmed from 2026 results; from Ballotpedia/search snippets Governor, AG, Treasurer, Insurance Commissioner were on the
  ballot (SoS open seat race exists per Wikipedia page title) plus U.S. Senate (Marshall); I did not add or drop any office.

## Discrepancies over 0.5%
None among included rows. Omitted rows above (2014 Governor, 2018 Insurance) had large OpenElections discrepancies.
Provenance of every file: provenance.csv in the raw folder.

## Rows added by the main session (2026-11-08, tools/ks_fill.py)
The helper's file is kept as statewide_results_helper.csv; statewide_results.csv = its rows plus these:
- 2022 Governor (Schmidt R 477,586 / Kelly D 499,845), Attorney General (Kobach / Mann), Secretary of State (Schwab / Repass): MIT Election
  Data and Science Lab 2022 precinct returns (https://github.com/MEDSL/2022-elections-official; local raw/results/gov2022/x/ks22_cleaned.csv)
  summed statewide. SECONDARY source, with no second source checked yet. MEDSL's Kansas file has no Treasurer or Insurance Commissioner race.
- 2026 Governor, U.S. Senate, Attorney General, Secretary of State: AP via NPR, fetched 2026-11-08 about 05:05Z, unofficial (98.9% of the
  expected vote). AP's feed has no Treasurer or Insurance Commissioner race, so those offices have no 2026 row.
Still missing: everything 1994-2010 for state offices, 2014 Governor, and 2018/2022 Treasurer and Insurance Commissioner. Those need the
Secretary of State's canvass files (Kevin's decision).

## Official Secretary of State files (main session, 2026-11-08, tools/ks_official.py)
sos.ks.gov refuses the home address at CloudFront; Kevin added its CloudFront blocks (108.157.150.0/24, 18.154.219.0/24) to the
ProtonWG split tunnel, and the official general-election vote totals were then downloaded one at a time (provenance.csv):
2006, 2014, 2018, 2022 (PDF text layers) and 2010 (scanned PDF, page 1 read from a rendered image; every value checked against its
printed percentage, which the report truncates). These replace the secondary rows for 2010-2022 and add 2006 and 2010 state offices,
2014 Governor and 2018/2022 Insurance Commissioner and 2022 Treasurer. The secondary values they replace matched within 20 votes.
statewide_results_pre_official.csv keeps the file as it was before this step; ks_2010_from_images.csv holds the 2010 rows.
Not available: the online index starts in 2004; 1994, 1998 and 2002 general-election files are not posted (requests redirect), and the
Douglas County copy of the 2002 totals has been taken down (the saved file is its home page, marked _NOT_PDF.html). U.S. Senate 1998
stays on the MIT Election Lab file.

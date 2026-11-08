# Ohio, Kansas, Iowa, Alaska, Mississippi, South Carolina and Indiana: 2026 statewide votes vs. a typical midterm

For every statewide race on these states' 2026 ballots, the vote each party would get if the office followed its own 1994–2022
midterm pattern, adjusted for the usual midterm loss of the party holding the White House, set against the unofficial 2026 count,
with the full 1994–2026 history behind it. Same method as[texas-2026-midterm-expected-vote](https://github.com/kevinnbass/texas-2026-midterm-expected-vote).

Web page with all figures: https://claude.ai/artifact/P9vUFZhAxmd5hYCTHubMUd

**2026 counts are unofficial** and come from different sources and dates by state (see each state below). Rebuild with
`./build.sh` after certified results are added to `data/inputs/`.

## Summary

| State | Races | Democratic nominee above expected | Republican nominee below expected |
|---|---|---|---|
| [Ohio](#ohio) | 6 | 6 | 5 |
| [Kansas](#kansas) | 4 | 3 | 3 |
| [Iowa](#iowa) | 7 | 7 | 3 |
| [Alaska](#alaska) | 3 | 1 | 3 |
| [Mississippi](#mississippi) | 1 | 1 | 1 |
| [South Carolina](#south-carolina) | 8 | 8 | 4 |
| [Indiana](#indiana) | 3 | 3 | 3 |

Expected = the office's own 1994–2022 baseline in the state plus the usual midterm effect of holding the White House, −11.0 points of the presidential vote for 2026, estimated from the 1994–2022 midterms of U.S. Senate races in all 50 states, governor races in the 37 states that elected governors in those years and every statewide office in Alaska, Iowa, Indiana, Kansas, Mississippi, Ohio, South Carolina and Texas (see [METHODOLOGY.md](METHODOLOGY.md)).

### How much the pool for the president's-party effect matters

Main race, actual minus adjusted expected votes (R / D), and the effect b used for 2026 (points of the presidential vote):

| State | This state only | First version (8 states) | Senate, all 50 states | All states (used) | All states, slope per party |
|---|---|---|---|---|---|
| Ohio (governor) | −251K / +584K (b −15.2) | −345K / +659K (b −10.4) | −289K / +614K (b −13.2) | −335K / +651K (b −11.0) | −416K / +586K (b −6.8 R / −15.1 D) |
| Kansas (governor) | +95K / −41K (b −11.1) | +92K / −39K (b −10.4) | +102K / −46K (b −13.0) | +94K / −41K (b −11.0) | +79K / −52K (b −6.8 R / −15.1 D) |
| Iowa (governor) | −77K / +166K (b −17.3) | −116K / +196K (b −10.4) | −98K / +183K (b −13.6) | −113K / +194K (b −11.0) | −137K / +176K (b −6.8 R / −15.1 D) |
| Alaska (governor) | −26K / −32K (b +2.5) | −13K / −42K (b −10.4) | −11K / −43K (b −12.4) | −12K / −42K (b −11.0) | −17K / −46K (b −6.8 R / −15.1 D) |
| Mississippi (us_senate) | −15K / +199K (b −9.0) | −10K / +196K (b −10.4) | +0K / +189K (b −13.1) | −8K / +194K (b −11.0) | −23K / +185K (b −6.8 R / −15.1 D) |
| South Carolina (governor) | +44K / +67K (b −8.8) | +60K / +56K (b −10.4) | +77K / +44K (b −12.3) | +64K / +53K (b −11.0) | +26K / +27K (b −6.8 R / −15.1 D) |
| Indiana (secretary_of_state) | −238K / +148K (b −12.9) | −264K / +166K (b −10.4) | −236K / +147K (b −13.1) | −258K / +162K (b −11.0) | −302K / +132K (b −6.8 R / −15.1 D) |
| Texas (governor) | +95K / +1,795K (b −7.5) | +213K / +1,706K (b −10.4) | +260K / +1,671K (b −11.6) | +234K / +1,690K (b −11.0) | +70K / +1,566K (b −6.8 R / −15.1 D) |

## Ohio

![Ohio: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/oh/oh_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Governor and Lieutenant Governor | Vivek Ramaswamy / Rob McColley 2,039,730 | 2,374,232 | −335K | Amy Acton / David Pepper 2,404,178 | 1,753,469 | +651K |
| Attorney General | Keith Faber 2,256,710 | 2,355,464 | −99K | John Kulewicz 2,285,117 | 1,807,586 | +478K |
| Secretary of State | Robert Sprague 2,129,981 | 2,320,052 | −190K | Allison Russo 2,287,160 | 1,742,203 | +545K |
| Auditor of State | Frank LaRose 2,310,105 | 2,348,415 | −38K | Annette Blackwell 2,237,955 | 1,717,575 | +520K |
| U.S. Senate | Jon Husted 2,077,748 | 2,337,085 | −259K | Sherrod Brown 2,301,042 | 2,048,630 | +252K |
| Ohio Supreme Court | Dan Hawkins (incumbent) 2,207,874 | 1,984,887 | +223K | Marilyn Zayas 2,315,779 | 1,967,725 | +348K |

- 2026 count: AP count fetched Nov. 8, 2026, about 98% of the expected vote (Auditor and Supreme Court: Wikipedia, at about 98% counted).
- Sources: Ohio Secretary of State (results pages 1994–2002 and 2010, workbooks 2014–2022, from Internet Archive captures); OpenElections (2006, the Secretary of State's precinct file); AP via NPR (2026); Wikipedia (2026 Auditor and Supreme Court).
- The 2026 Treasurer race has no published vote count yet and is left out. Supreme Court races had no party labels on the ballot before 2022, so that office's baseline is 2022 only; the two 2026 seats are averaged. The 2026 U.S. Senate race is a special election for the rest of the term.
- Inputs: [`data/inputs/OH/`](data/inputs/OH/) (its README lists every source and check); panels: [`figures/oh/panels/`](figures/oh/panels/).
- Write-up: [What moved the Ohio vote in 2026](https://claude.ai/artifact/TxTiFtkTipZ7qrnZkY5Dod)

## Kansas

![Kansas: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/ks/ks_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Attorney General | Kris Kobach 539,297 | 548,292 | −9K | Chris Mann 552,753 | 493,662 | +59K |
| Governor | Ty Masterson 543,612 | 449,466 | +94K | Cindy Holscher 551,250 | 591,763 | −41K |
| Secretary of State | Pat Proctor 524,555 | 527,717 | −3K | Jennifer Day 515,738 | 502,228 | +14K |
| U.S. Senate | Roger Marshall 505,558 | 532,667 | −27K | Adam Hamilton 561,143 | 363,819 | +197K |

- 2026 count: AP count fetched Nov. 8, 2026, about 99% of the expected vote.
- Sources: MIT Election Data and Science Lab (U.S. Senate; 2022 state offices); OpenElections (2014 and 2018 state offices); AP via NPR (2026).
- The Kansas Secretary of State's canvass files could not be fetched automatically, so the state offices rest on secondary sources and have only 2014–2022 history (Governor: 2018 and 2022). Treasurer and Insurance Commissioner are left out (no 2026 count in the AP feed). U.S. Senate 2002 and 2014: no Democratic nominee.
- Inputs: [`data/inputs/KS/`](data/inputs/KS/) (its README lists every source and check); panels: [`figures/ks/panels/`](figures/ks/panels/).
- Write-up: [What moved the Kansas vote in 2026](https://claude.ai/artifact/XmjgDi7jHMVqSthtag5cwZ)

## Iowa

![Iowa: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/ia/ia_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Governor and Lieutenant Governor | Zach Lahn 607,591 | 720,893 | −113K | Rob Sand 757,506 | 563,396 | +194K |
| Secretary of State | Paul Pate 711,986 | 656,586 | +55K | Ryan Peterman 625,997 | 553,865 | +72K |
| Auditor of State | Chris Cournoyer 660,159 | 693,210 | −33K | Taylor Wettach 666,632 | 550,452 | +116K |
| Treasurer of State | Roby Smith 664,948 | 586,494 | +78K | John Norwood 655,763 | 632,301 | +23K |
| Secretary of Agriculture | Mike Naig 701,882 | 701,001 | +1K | Chris Jones 629,249 | 523,067 | +106K |
| Attorney General | Brenna Bird 657,607 | 564,314 | +93K | Nate Willems 681,255 | 640,314 | +41K |
| U.S. Senate | Ashley Hinson 630,808 | 778,945 | −148K | Josh Turek 686,641 | 498,550 | +188K |

- 2026 count: AP count fetched Nov. 8, 2026, about 99% of the expected vote (Auditor, Treasurer and Agriculture from the state results site of Nov. 4, 95 of 99 counties).
- Sources: Iowa Secretary of State canvass (1994, 2014, 2022); OpenElections (1998 Senate, 2002–2018, secondary); Wikipedia (some Governor rows, secondary); AP via NPR and the state's results site (2026).
- The Iowa Secretary of State's site refuses automated requests, so some years rest on secondary sources until archived copies of the canvass arrive; 1998 down-ballot offices are not yet filled.
- Inputs: [`data/inputs/IA/`](data/inputs/IA/) (its README lists every source and check); panels: [`figures/ia/panels/`](figures/ia/panels/).
- Write-up: [What moved the Iowa vote in 2026](https://claude.ai/artifact/XshXMj9obj9VhsfrsGJF3N)

## Alaska

![Alaska: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/ak/ak_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Governor (joint ticket with Lieutenant Governor) | Wilson/Shower (R) and other Republicans (first choice) 107,500 | 119,691 | −12K | Kreiss-Tomkins/Johnson (DEM/NON) 103,837 | 146,166 | −42K |
| U.S. House (at-large) | Begich, Nick 105,647 | 152,232 | −47K | Hafner, Eric 15,550 | 125,380 | −110K |
| U.S. Senate | Sullivan, Dan S. and other Republicans (first choice) 107,171 | 165,827 | −59K | Peltola, Mary 102,962 | 84,175 | +19K |

- 2026 count: Division report of Nov. 4, 2026, 1:09 pm; about 74% of the expected vote counted (AP), absentee ballots still being counted.
- Sources: Alaska Division of Elections.
- From 2022 Alaska uses a top-four primary and a ranked-choice general election, with no party nominees: each party's vote for 2022 and 2026 is the combined first-choice vote of its candidates (ranked-choice tabulation for 2026 is set for Nov. 18). A + after a name marks that combined vote.
- 2026 U.S. House: independent Bill Hill (86,023) is not counted as Democratic. 2010 U.S. Senate: Lisa Murkowski's write-in votes (101,091) are not counted as Republican. 2014 Governor: no Democratic nominee (the Walker/Mallott independent ticket is not counted). 2022 Governor: independent Bill Walker (54,668) is not counted as Democratic. 2026 U.S. Senate: Daniel J. Sullivan Jr. (no party, 3,600) is not counted as Republican.
- Inputs: [`data/inputs/AK/`](data/inputs/AK/) (its README lists every source and check); panels: [`figures/ak/panels/`](figures/ak/panels/).
- Write-up: [What moved the Alaska vote in 2026](https://claude.ai/artifact/EYRgFH2onscg5JJcSncTgY)

## Mississippi

![Mississippi: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/ms/ms_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| U.S. Senate | Cindy Hyde-Smith 465,356 | 472,926 | −8K | Scott Colom 467,930 | 273,660 | +194K |

- 2026 count: AP count fetched Nov. 8, 2026, about 97% of the expected vote.
- Sources: MIT Election Data and Science Lab (U.S. Senate 1994–2022); AP via NPR (2026).
- Only the U.S. Senate is on Mississippi's 2026 statewide ballot. The 2018 special Senate election (decided in a Nov. 27 runoff) is left out; 2002 had no Democratic nominee.
- Inputs: [`data/inputs/MS/`](data/inputs/MS/) (its README lists every source and check); panels: [`figures/ms/panels/`](figures/ms/panels/).
- Write-up: [What moved the Mississippi vote in 2026](https://claude.ai/artifact/4V6xZVmCcHVQhwD1fDFpKd)

## South Carolina

![South Carolina: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/sc/sc_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Governor | Alan Wilson / Mike Reichenbach 1,051,010 | 986,568 | +64K | Jermaine Johnson / Sam Skardon 960,269 | 907,366 | +53K |
| Secretary of State | Mark Hammond 1,073,652 | 1,113,516 | −40K | Jason Belton 952,186 | 777,040 | +175K |
| State Treasurer | Curtis Loftis 1,062,666 | 1,048,553 | +14K | Vincent Coe 959,539 | 957,277 | +2K |
| Attorney General | David Stumbo 1,059,358 | 1,080,844 | −21K | Richard Hricik 964,921 | 876,162 | +89K |
| Comptroller General | Mike Burkhold 1,048,553 | 967,746 | +81K | Tiffany Boozer 965,075 | 889,785 | +75K |
| State Superintendent of Education | Ellen Weaver 1,032,516 | 880,774 | +152K | Sylvia Wright 976,406 | 907,111 | +69K |
| Commissioner of Agriculture | Cody Simpson 1,042,601 | 1,056,425 | −14K | DeShawn Blanding 922,961 | 782,799 | +140K |
| U.S. Senate | Darline Graham 951,896 | 1,005,983 | −54K | Annie Andrews 1,043,712 | 808,947 | +235K |

- 2026 count: state results file of Nov. 6, 2026, 6:25 pm EST, all precincts reporting.
- Sources: South Carolina State Election Commission (Election Reports 1994–2006, election-night reporting files 2010–2026).
- Governor and Lieutenant Governor run as one ticket from 2018. Some offices had no Democratic nominee in some years; those years are left out of that office's baseline.
- Inputs: [`data/inputs/SC/`](data/inputs/SC/) (its README lists every source and check); panels: [`figures/sc/panels/`](figures/sc/panels/).
- Write-up: [What moved the South Carolina vote in 2026](https://claude.ai/artifact/QR3PRnaGkL9an8j9cXzMbf)

## Indiana

![Indiana: history and 2018–2026 races vs. expected, adjusted for the president's party](figures/in/in_incumbency_history_and_expected.png)

| 2026 race | Republican | Expected | Actual − expected | Democrat | Expected | Actual − expected |
|---|---|---|---|---|---|---|
| Secretary of State | Max Engling 826,017 | 1,084,369 | −258K | Beau Bayh 1,004,067 | 842,016 | +162K |
| Auditor of State | Elise Nieshalla 906,914 | 1,094,055 | −187K | Jessica Bailey 956,408 | 827,032 | +129K |
| Treasurer of State | Daniel Elliott 977,791 | 1,110,030 | −132K | Coumba Kebe 938,209 | 836,672 | +102K |

- 2026 count: state results file of Nov. 7, 2026, 11:05 pm, 4,831 of 5,067 precincts reporting.
- Sources: Indiana Election Division (2002–2022 and 2026); Capitol & Washington (state offices 1994–1998, secondary); MIT Election Data and Science Lab (U.S. Senate 1994–1998).
- The Auditor of State is titled State Comptroller from 2026.
- Inputs: [`data/inputs/IN/`](data/inputs/IN/) (its README lists every source and check); panels: [`figures/in/panels/`](figures/in/panels/).
- Write-up: [What moved the Indiana vote in 2026](https://claude.ai/artifact/4VcgQGmKS1dT6We2xXuTpm)

## Rebuild

```
pip install -r requirements.txt
./build.sh          # rebuild into build/ and compare with data/derived and figures
python3 src/fetch_sources.py   # re-download every source with a URL and compare sha256
```

## Layout

- `data/inputs/` — what the code reads: `presidential_1992_2024.csv` and `<ST>/statewide_results.csv` (one row per race,
  with source URL, file, sha256, cross-check and notes) plus each state's README.
- `data/raw/` — the downloaded source files (10 MB or less); `data/SOURCES.csv` lists every source with URL and sha256,
  including larger files that are not copied.
- `data/derived/` — the computed tables; `figures/` — the figures; `site/` — the web page builder.
- `src/expected.py` (the computation), `src/figs.py` (figures), `src/build_states.py` (all states), `src/verify.py`.

Texas inputs are included because Texas is part of the pooled president's-party estimate; the Texas figures and raw files are in
[texas-2026-midterm-expected-vote](https://github.com/kevinnbass/texas-2026-midterm-expected-vote).

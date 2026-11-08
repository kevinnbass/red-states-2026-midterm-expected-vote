# Methodology

## Expected midterm vote
For office *o*, party *p* and midterm year *y*:

- ratio(o, p, y) = party p's votes for office o in midterm y ÷ party p's presidential votes in the state in year y − 2.
- **Plain expectation** for 2026 = the party's 2024 presidential vote in the state × the mean ratio of office o over the 1994–2022 midterms.
  For 2018 and 2022 the same is computed leaving that year out of the mean.
- **Adjusted for the president's party**: ratio = a[o, p] + b × (party p holds the White House). b is one within-(office, party) slope
  pooled across Texas, Ohio, Kansas, Iowa, Alaska, Mississippi, South Carolina, Indiana; each a[o, p] is that state's own office-party mean of (ratio − b × holds).
  Both are estimated from 1994–2022 leaving out the target year. For 2026 b = −10.4 points of the presidential vote.
- Only races with both a Republican and a Democratic nominee count. Offices with several races in one year (two Senate seats, court seats)
  use the average of those races.
- Votes are each nominee's own party-line votes. Alaska since 2022 (top-four primary, ranked-choice general) has no party nominees:
  there each party's vote is the combined first-choice vote of all its candidates (`expected.ALL_LINES_FROM`).

## Why pool the slope
With one or two offices, a state's own estimate of b swings widely depending on which year is left out (Mississippi alone:
−15.9 to −2.1 points); pooled with other states it is stable. The office baselines stay each state's own.

## Known limits
- 2026 counts are unofficial and taken at different times by state (Alaska about 74% counted).
- Some history rests on secondary sources where a state's own files could not be fetched automatically (Kansas, parts of Iowa,
  Indiana 1994–1998); each row's `notes` says so and each state's README lists every check.
- Supreme Court races in Ohio carried no party labels before 2022, so that office's baseline is short.

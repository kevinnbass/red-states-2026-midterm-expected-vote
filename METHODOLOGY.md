# Methodology

## Expected midterm vote
For office *o*, party *p* and midterm year *y*:

- ratio(o, p, y) = party p's votes for office o in midterm y ÷ party p's presidential votes in the state in year y − 2.
- **Expected vote** = the party's presidential vote two years earlier × (a[o, p] + b × (party p holds the White House)), from
  ratio = a[o, p] + b × holds. b is one within-(office, party) slope
  pooled across U.S. Senate races in all 50 states, governor races in the 37 states that elected governors in those years and every statewide office in Alaska, Iowa, Indiana, Kansas, Mississippi, Ohio, South Carolina and Texas; each a[o, p] is that state's own office-party mean of
  (ratio − b × holds).
  Both are estimated from 1994–2022 leaving out the target year. (`expected.csv` also keeps the unadjusted columns, the plain mean
  ratio, for reference; the figures and pages use only the adjusted expectation.) For 2026 b = −11.0 points of the presidential vote.
- Only races with both a Republican and a Democratic nominee count. Offices with several races in one year (two Senate seats, court seats)
  use the average of those races.
- Votes are each nominee's own party-line votes. Alaska since 2022 (top-four primary, ranked-choice general) has no party nominees:
  there each party's vote is the combined first-choice vote of all its candidates (`expected.ALL_LINES_FROM`).

## Why pool the slope, and over all states
With one or two offices, a state's own estimate of b swings widely depending on which year is left out (Mississippi alone:
−15.9 to −2.1 points; Alaska's own history gives the wrong sign); pooled over every state with data it is stable. The office
baselines stay each state's own. `data/derived/pool_comparison/` shows every 2026 result under each alternative pool (this state
only; the first version's eight states; Senate races in all 50 states; all states; all states with one slope per party; each also
without races where a third candidate took 15% or more), built by `tools/pool_sensitivity.py`, which also checks that its
"everything" pool is exactly the one the figures use.

## Known limits
- 2026 counts are unofficial and taken at different times by state (Alaska about 74% counted).
- Some history rests on secondary sources where a state's own files could not be fetched automatically (Kansas, parts of Iowa,
  Indiana 1994–1998); each row's `notes` says so and each state's README lists every check.
- Supreme Court races in Ohio carried no party labels before 2022, so that office's baseline is short.

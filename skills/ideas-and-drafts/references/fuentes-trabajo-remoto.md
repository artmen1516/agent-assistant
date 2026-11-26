# Remote job vacancy sources — verification

Base for the idea `Remote job search — monitoring and reporting`
(senior/lead/staff, 100% remote, MX/US/CA). These boards change without notice:
re-verify counts before building on them.

## With working API/RSS

- **RemoteOK** — `https://remoteok.com/api`
  JSON, ~100 vacancies per fetch. The first element of the array is a legal notice, discard it.
  Requests attribution with a link to Remote OK (required by their ToS).
- **We Work Remotely** — `https://weworkremotely.com/categories/remote-programming-jobs.rss`
  RSS per category (~25 items each); more categories (full-stack, devops, design).
  The `<region>` element carries the allowed zone.
- **Himalayas** — `https://himalayas.app/jobs/rss`
  RSS with the ~20 most recent. `<himalayasJobs:locationRestriction>` carries ONE country per vacancy:
  the MX/US/CA filter is direct against that field.
- **Jobicy** — `https://jobicy.com/api/v2/remote-jobs?count=50`
  JSON and the only one with normalized seniority (`jobLevel`: Senior, Director…)
  plus `jobGeo`. Parameters: `count`, `industry`, `geo`.

## Account-based / manual (high value, US/CA sponsorship-friendly)

- **VanHack** — US/CA roles, sponsorship-friendly, account required. High value for relocation-grade and remote US/CA roles.
- **LinkedIn Jobs** — no public API and scraping goes against their terms (blocks and suspends). Realistic route: saved searches + email alerts (that email can be parsed), plus manual review.
- **Wellfound** — startups, salary sometimes visible; manual review.
- **YC Work at a Startup** — manual review.
- **Hacker News "Who is hiring"** — manual review or targeted parsing of the thread.

## Degraded or without API

- **Remotive** — its public API (`/api/remote-jobs`) became limited: ignores `limit`/`search`/`category` and returns ~14 vacancies total. Do not use as primary source; if it recovers, it was `?category=software-dev&limit=N`.

## Geography filter (practical rule)

- "USA only" requires work authorization in the US: exclude by default.
- Accepted: Worldwide, Anywhere, Americas, LATAM, North America, Mexico,
  and explicit mentions of hiring in Mexico (EOR or local entity).
- "Europe only" or other continent: exclude.

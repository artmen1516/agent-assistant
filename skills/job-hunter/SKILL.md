---
name: job-hunter
description: "Use when running or tuning the daily remote job search cron."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [job-search, cron, remote, career]
    related_skills: [researcher, specialist-roster]
---

# Job hunter

Daily cron that scans remote job boards, dedupes, filters by Arturo's criteria, scores, and delivers top matches to Telegram + appends to the vault log.

## When to Use

- Running/tuning the daily job search.
- Adding a new source (LinkedIn emails, VanHack).
- Adjusting criteria (roles, geo, salary floor, score threshold).

## Script

`~/.hermes/scripts/job-hunter.py` — fetches RemoteOK, WWR, Himalayas, Jobicy (API/RSS), normalizes, dedupes by URL and (company,title), hard-filters (role, seniority, geo), scores deterministically (0-10), appends passing postings to `job-search-log.md` (status `Found`), prints top 5 (score > 8) to stdout.

State: `~/.hermes/job-hunter/seen.json` (dedupe), `runs.log` (debug).

## Criteria (from projects/job-search.md)

- Roles: Senior/Staff/Lead/Principal SWE, AI Engineer, Full Stack, Backend, Platform, DevOps/Cloud, ML, Forward Deployed, Solutions.
- Geo: Worldwide/Anywhere/Americas/LATAM/North America/Mexico/remote; exclude USA-only (no sponsorship), Europe, Asia, etc.
- Seniority: senior/staff/lead/principal; exclude junior/mid/entry/intern.
- Employment preferred over contract (contract penalized in scoring).
- Salary floor: USD 130k base (CA US), C$130k (BC CA), 90k+ MXN/month gross (MX remote).
- Score threshold for notification: > 8 (top 5).

## Cron

Daily 07:30 America/Los_Angeles. Hybrid mode: script `job-hunter.py` runs first (cheap, deterministic), its stdout is injected as context, then the agent enriches/filters and delivers top 5. Toolsets: web. Deliver to Telegram home channel. Empty output = no delivery.

## Adding sources

- LinkedIn: saved searches + email alerts; parse email (not scraping). Add a fetch_linkedin() that reads recent job-alert emails.
- VanHack: account-based; manual import or authenticated scrape. Add fetch_vanhack().

## Tuning

- Score threshold: edit `> 8` in main().
- Top N: edit `[:5]`.
- Add roles/stack/geo tokens in the constants at top of script.

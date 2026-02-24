# Parking Pricing Data — TODO

## Phase 1: Project Setup
- [ ] Choose tech stack (suggested: Python + Playwright + SQLite + Streamlit)
- [ ] Initialize `pyproject.toml` / `requirements.txt` with dependencies
- [ ] Set up project directory structure (`scrapers/`, `db/`, `dashboard/`)
- [ ] Set up `.gitignore` (venv, DB files, etc.)

## Phase 2: Data Modeling
- [ ] Define schema for scraped records:
  - `source` (ParkWhiz)
  - `lot_id`, `lot_name`, `address`
  - `search_location` (city or lat/lng queried)
  - `price` (USD), `duration_hours`
  - `availability` (spots remaining, if available)
  - `scraped_at` timestamp
- [ ] Create SQLite DB + table migrations (`db/schema.sql`)
- [ ] Write a simple DB helper (`db/database.py`) for inserts and queries

## Phase 3: ParkWhiz Scraper
- [ ] Investigate ParkWhiz's network requests (check for internal API calls via DevTools)
- [ ] If API exists: build a direct HTTP client scraper
- [ ] If no API: build a Playwright browser scraper
  - [ ] Accept a search location (city / address) as input
  - [ ] Extract lot name, address, price per duration, availability
  - [ ] Handle pagination / dynamic loading
- [ ] Save results to DB
- [ ] Add error handling and retry logic

## Phase 4: Scraper Runner
- [ ] Build a `run_scrapers.py` CLI entry point
  - [ ] Accept `--location` argument
  - [ ] Run scraper and persist results
- [ ] Add logging (structured, with timestamps)

## Phase 5: Dashboard
- [ ] Build a Streamlit dashboard (`dashboard/app.py`)
  - [ ] Table view: all scraped records with filters (location, date range)
  - [ ] Price-over-time chart: track how prices change across scrape runs
  - [ ] Last-scraped timestamp + record counts (health indicators)
- [ ] Run dashboard locally with `streamlit run dashboard/app.py`

## Phase 6: Scheduling (Optional)
- [ ] Add a cron job or `apscheduler` loop to run scrapers on a schedule
- [ ] Add alerting if a scrape run fails or returns 0 results

## Open Questions
- [ ] Which locations / search queries should we scrape first?
- [ ] How often should we scrape (rate limiting / ToS considerations)?
- [ ] Do we need proxies or user-agent rotation?

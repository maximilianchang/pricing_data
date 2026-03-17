# Cloud Pipeline Plan

## Architecture Overview
Cloud Scheduler (daily) → Cloud Run Job → Firestore

The scrapers use SeleniumBase with a real browser, so the Cloud Run container needs Chrome bundled in a custom Docker image.

---

## GCP Project
- [ ] Create a new GCP project (e.g. `parking-pricing-pipeline`)
- [ ] Enable APIs: Cloud Run, Cloud Scheduler, Firestore, Artifact Registry
- [ ] Create a service account with Firestore write + Cloud Run invoker roles

---

## Datastore (Firestore)
- [ ] Use Firestore in Native mode
- [ ] Collection: `listings`
- [ ] Document schema:
  - `source` (str) — "spothero" | "parkwhiz"
  - `name` (str)
  - `price_usd` (str)
  - `pricing_type` (str) — "hourly" | "monthly"
  - `location` (str) — e.g. "San Francisco, CA"
  - `scraped_at` (timestamp)
- [ ] Write a `db.py` helper with an `insert_listings(listings, source, pricing_type, location)` function

---

## Cloud Run Job (Scraper)
- [ ] Build a custom Docker image:
  - Base: `python:3.12-slim`
  - Install Chrome + ChromeDriver (required by SeleniumBase)
  - Install project dependencies
- [ ] Write an entrypoint `run.py` that runs both scrapers for configured locations and writes results to Firestore
- [ ] Push image to Artifact Registry
- [ ] Deploy as a Cloud Run Job

---

## Scheduling
- [ ] Create a Cloud Scheduler job to trigger the Cloud Run Job daily
- [ ] Add Cloud Logging for run status + result counts

# Parking Pricing Data — TODO

## Done
- [x] ParkWhiz scraper (hourly + monthly)
- [x] SpotHero scraper (hourly + monthly)

## Next: Data Collection Project
Schedule and store scraped data in a dedicated Google Cloud project/tenant.

### Google Cloud Setup
- [ ] Create a new GCP project for this data pipeline
- [ ] Set up service account + credentials

### Storage
- [ ] Define schema: `source`, `name`, `price_usd`, `pricing_type` (hourly/monthly), `location`, `scraped_at`
- [ ] Provision a database (Cloud SQL or BigQuery)

### Scheduler
- [ ] Deploy scraper as a Cloud Run job or Compute Engine instance
- [ ] Schedule with Cloud Scheduler (hourly snapshot + monthly)
- [ ] Add logging with Cloud Logging

### Coverage Expansion
- [ ] Add more cities beyond SF
- [ ] Add more sources:
  - [ ] Way.com
  - [ ] AirportParking.com
  - [ ] Parking management company sites (LAZ, SP+, Impark, etc.)

### Open Questions
- [ ] Which cities to prioritize?
- [ ] How often to snapshot (rate limit / ToS considerations)?
- [ ] Parking management sites likely need custom scrapers per operator — how to scale?

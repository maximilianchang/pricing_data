from datetime import datetime, timezone, timedelta
from seleniumbase import SB
from google.cloud import firestore
from scrapers.parkwhiz import search_hourly, search_monthly

LOCATION = "San Francisco, CA"
CITY = "san-francisco"
STATE = "ca"
PST = timezone(timedelta(hours=-8))


def save(db: firestore.Client, listings: list[dict], pricing_type: str) -> None:
    col = db.collection("listings")
    scraped_at = datetime.now(timezone.utc)
    for listing in listings:
        price = listing.get("price_usd") or listing.get("price_usd_per_month")
        col.add({
            "source": "parkwhiz",
            "name": listing.get("name"),
            "price_usd": price,
            "pricing_type": pricing_type,
            "location": LOCATION,
            "scraped_at": scraped_at,
        })


def main():
    db = firestore.Client()

    # Hourly: today 6pm–9pm PST
    today = datetime.now(PST).replace(hour=18, minute=0, second=0, microsecond=0)
    start = today
    end = today.replace(hour=21)

    with SB(uc=True, headless=True) as sb:
        hourly = search_hourly(sb, city=CITY, state=STATE, start=start, end=end)
        print(f"Hourly: {len(hourly)} listings")
        save(db, hourly, "hourly")

    with SB(uc=True, headless=True) as sb:
        monthly = search_monthly(sb, city=CITY, state=STATE)
        print(f"Monthly: {len(monthly)} listings")
        save(db, monthly, "monthly")


if __name__ == "__main__":
    main()

import argparse
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


def run_hourly(db: firestore.Client) -> None:
    today = datetime.now(PST).replace(hour=18, minute=0, second=0, microsecond=0)
    start = today
    end = today.replace(hour=21)
    with SB(chromium_arg="--headless,--disable-gpu,--window-size=1024,768,--no-sandbox") as sb:
        listings = search_hourly(sb, city=CITY, state=STATE, start=start, end=end)
        print(f"Hourly: {len(listings)} listings")
        save(db, listings, "hourly")


def run_monthly(db: firestore.Client) -> None:
    with SB(chromium_arg="--headless,--disable-gpu,--window-size=1024,768,--no-sandbox") as sb:
        listings = search_monthly(sb, city=CITY, state=STATE)
        print(f"Monthly: {len(listings)} listings")
        save(db, listings, "monthly")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["hourly", "monthly"], required=True)
    args = parser.parse_args()

    db = firestore.Client()
    if args.mode == "hourly":
        run_hourly(db)
    else:
        run_monthly(db)


if __name__ == "__main__":
    main()

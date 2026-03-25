import argparse
from datetime import datetime, timezone, timedelta
from seleniumbase import SB
from google.cloud import firestore
from scrapers.parkwhiz import search_hourly, search_monthly

PST = timezone(timedelta(hours=-8))


def load_cities(db: firestore.Client) -> list[dict]:
    docs = db.collection("cities").where("enabled", "==", True).stream()
    return [doc.to_dict() for doc in docs]


def save(db: firestore.Client, listings: list[dict], pricing_type: str, location: str) -> None:
    col = db.collection("listings")
    scraped_at = datetime.now(timezone.utc)
    for listing in listings:
        price = listing.get("price_usd") or listing.get("price_usd_per_month")
        col.add({
            "source": "parkwhiz",
            "name": listing.get("name"),
            "price_usd": price,
            "pricing_type": pricing_type,
            "location": location,
            "scraped_at": scraped_at,
        })


def run_hourly(db: firestore.Client, cities: list[dict]) -> None:
    today = datetime.now(PST).replace(hour=18, minute=0, second=0, microsecond=0)
    start = today
    end = today.replace(hour=21)
    for city_data in cities:
        city, state, location = city_data["city"], city_data["state"], city_data["location"]
        try:
            with SB(chromium_arg="--headless,--disable-gpu,--window-size=1024,768,--no-sandbox") as sb:
                listings = search_hourly(sb, city=city, state=state, start=start, end=end)
                print(f"[{location}] Hourly: {len(listings)} listings")
                save(db, listings, "hourly", location)
        except Exception as e:
            print(f"[{location}] Hourly failed: {e}")


def run_monthly(db: firestore.Client, cities: list[dict]) -> None:
    for city_data in cities:
        city, state, location = city_data["city"], city_data["state"], city_data["location"]
        try:
            with SB(chromium_arg="--headless,--disable-gpu,--window-size=1024,768,--no-sandbox") as sb:
                listings = search_monthly(sb, city=city, state=state)
                print(f"[{location}] Monthly: {len(listings)} listings")
                save(db, listings, "monthly", location)
        except Exception as e:
            print(f"[{location}] Monthly failed: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["hourly", "monthly"], required=True)
    args = parser.parse_args()

    db = firestore.Client()
    cities = load_cities(db)
    print(f"Loaded {len(cities)} cities")

    if args.mode == "hourly":
        run_hourly(db, cities)
    else:
        run_monthly(db, cities)


if __name__ == "__main__":
    main()

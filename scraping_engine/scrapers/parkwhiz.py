from datetime import datetime, timezone, timedelta
from urllib.parse import urlencode
from seleniumbase import SB
from bs4 import BeautifulSoup


def build_parkwhiz_url(
    city: str,
    state: str,
    start: datetime,
    end: datetime,
) -> str:
    """
    Build a ParkWhiz search URL.

    Args:
        city:  City name, hyphenated (e.g. "san-francisco", "new-york")
        state: Two-letter state code (e.g. "ca", "ny")
        start: Timezone-aware start datetime
        end:   Timezone-aware end datetime

    Returns:
        Full ParkWhiz map search URL with encoded query params.
    """
    location_slug = f"{city}-{state}-parking"

    def fmt(dt: datetime) -> str:
        offset = dt.strftime("%z")  # e.g. "-0800"
        return dt.strftime("%Y-%m-%dT%H:%M:%S") + offset[:3] + ":" + offset[3:]

    params = urlencode({"start": fmt(start), "end": fmt(end)})
    return f"https://www.parkwhiz.com/p/{location_slug}/map/?{params}"


def parse_listings(page_source: str) -> list[dict]:
    """Parse parking listings from ParkWhiz page source."""
    soup = BeautifulSoup(page_source, "html.parser")
    listings = []
    for container in soup.select("div.listing-container"):
        listing = {
            "name": _text(container.select_one("div.location-name")),
            "address": _text(container.select_one("div.address")),
            "price_usd": _parse_price(container.select_one("div.listing-price")),
        }
        if any(listing.values()):
            listings.append(listing)
    return listings


def _parse_price(el) -> float | None:
    """
    Parse ParkWhiz's split price format:
        <div class="listing-price ..."><sup>$</sup>23<sup>32</sup></div>
    The first <sup> is the currency symbol, the bare text node is dollars,
    and the last <sup> is cents. Returns a float e.g. 23.32.
    """
    if not el:
        return None
    sups = el.find_all("sup")
    dollars_text = "".join(
        node for node in el.children
        if hasattr(node, "__class__") and node.__class__.__name__ == "NavigableString"
    ).strip()
    cents_text = sups[-1].get_text(strip=True) if len(sups) >= 2 else "00"
    try:
        return float(f"{dollars_text}.{cents_text}")
    except ValueError:
        return None


def _text(el) -> str | None:
    return el.get_text(strip=True) if el else None


if __name__ == "__main__":
    tz = timezone(timedelta(hours=-8))  # PST
    url = build_parkwhiz_url(
        city="san-francisco",
        state="ca",
        start=datetime(2026, 2, 25, 18, 0, 0, tzinfo=tz),
        end=datetime(2026, 2, 25, 21, 0, 0, tzinfo=tz),
    )

    with SB(uc=True, test=True) as sb:
        sb.activate_cdp_mode(url)
        sb.sleep(3)

        page_source = sb.get_page_source()
        listings = parse_listings(page_source)

        print(f"Found {len(listings)} listings")
        for listing in listings:
            print(listing)

        if not listings:
            with open("parkwhiz_source.html", "w") as f:
                f.write(page_source)
            print("No listings parsed — raw source saved to parkwhiz_source.html")

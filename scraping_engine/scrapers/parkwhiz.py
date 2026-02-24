from datetime import datetime, timezone, timedelta
from urllib.parse import urlencode
from seleniumbase import SB
from bs4 import BeautifulSoup


def search_hourly(sb: SB, city: str, state: str, start: datetime, end: datetime) -> list[dict]:
    """
    Scrape hourly parking listings from ParkWhiz.

    Args:
        sb:    Active SeleniumBase instance
        city:  City name, hyphenated (e.g. "san-francisco")
        state: Two-letter state code (e.g. "ca")
        start: Timezone-aware start datetime
        end:   Timezone-aware end datetime
    """
    def fmt(dt: datetime) -> str:
        offset = dt.strftime("%z")
        return dt.strftime("%Y-%m-%dT%H:%M:%S") + offset[:3] + ":" + offset[3:]

    url = f"https://www.parkwhiz.com/p/{city}-{state}-parking/map/?{urlencode({'start': fmt(start), 'end': fmt(end)})}"

    sb.activate_cdp_mode(url)
    sb.sleep(3)

    soup = BeautifulSoup(sb.get_page_source(), "html.parser")
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


def search_monthly(sb: SB, city: str, state: str) -> list[dict]:
    """
    Scrape monthly parking listings from ParkWhiz.

    Args:
        sb:    Active SeleniumBase instance
        city:  City name, hyphenated (e.g. "san-francisco")
        state: Two-letter state code (e.g. "ca")
    """
    url = f"https://www.parkwhiz.com/p/{city}-{state}-monthly-parking/"

    sb.activate_cdp_mode(url)
    sb.sleep(3)

    soup = BeautifulSoup(sb.get_page_source(), "html.parser")
    listings = []
    for container in soup.select("div.listing-container"):
        listing = {
            "name": _text(container.select_one("div.wrap-ellipses")),
            "address": _text(container.select_one("div.text-color-medium-grey")),
            "price_usd_per_month": _parse_monthly_price(container.select_one("div.text-size-xs-28")),
        }
        if any(listing.values()):
            listings.append(listing)
    return listings


def _parse_monthly_price(el) -> float | None:
    """
    Parse ParkWhiz monthly price format:
        <div class="... text-size-xs-28 ..."><div>starting at</div>$400</div>
    Extracts the direct text node and strips the leading $.
    """
    if not el:
        return None
    price_text = "".join(
        node for node in el.children
        if hasattr(node, "__class__") and node.__class__.__name__ == "NavigableString"
    ).strip().lstrip("$")
    try:
        return float(price_text)
    except ValueError:
        return None


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

    with SB(uc=True, test=True) as sb:
        hourly = search_hourly(
            sb,
            city="san-francisco",
            state="ca",
            start=datetime(2026, 2, 25, 18, 0, 0, tzinfo=tz),
            end=datetime(2026, 2, 25, 21, 0, 0, tzinfo=tz),
        )
        print(f"Hourly: {len(hourly)} listings")
        for listing in hourly:
            print(listing)

        monthly = search_monthly(sb, city="san-francisco", state="ca")
        print(f"Monthly: {len(monthly)} listings")
        for listing in monthly:
            print(listing)

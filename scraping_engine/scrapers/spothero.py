from datetime import datetime
from urllib.parse import urlencode
from seleniumbase import SB
from bs4 import BeautifulSoup


def search_hourly(
    sb: SB,
    search_string: str,
    latitude: float,
    longitude: float,
    start: datetime,
    end: datetime,
) -> list[dict]:
    def fmt(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M")

    url = "https://spothero.com/search?" + urlencode({
        "kind": "address",
        "latitude": latitude,
        "longitude": longitude,
        "search_string": search_string,
        "starts": fmt(start),
        "ends": fmt(end),
        "view": "dl",
    })

    sb.activate_cdp_mode(url)
    sb.sleep(3)

    page_source = sb.get_page_source()
    soup = BeautifulSoup(page_source, "html.parser")
    listings = []

    for container in soup.find_all("div", class_="FacilitySummary-container"):
        title_tag = container.find(attrs={"data-testid": "FacilitySummary-title"})
        price_tag = container.find(class_="FacilitySummary-FormattedPrice")
        if title_tag and price_tag:
            listings.append({
                "name": title_tag.get_text(strip=True),
                "price_usd": price_tag.get_text(separator="", strip=True),
            })

    if not listings:
        with open("spothero_source.html", "w") as f:
            f.write(page_source)
        print("No listings parsed — raw source saved to spothero_source.html")

    return listings


def search_monthly(
    sb: SB,
    search_string: str,
    latitude: float,
    longitude: float,
    start: datetime,
) -> list[dict]:
    url = "https://spothero.com/search?" + urlencode({
        "kind": "address",
        "monthly": "true",
        "latitude": latitude,
        "longitude": longitude,
        "search_string": search_string,
        "starts": start.strftime("%Y-%m-%dT00:00"),
        "view": "dl",
    })

    sb.activate_cdp_mode(url)
    sb.sleep(3)

    page_source = sb.get_page_source()
    soup = BeautifulSoup(page_source, "html.parser")
    listings = []

    for container in soup.find_all("div", class_="FacilitySummary-container"):
        title_tag = container.find(attrs={"data-testid": "FacilitySummary-title"})
        price_tag = container.find(class_="FacilitySummary-FormattedPrice")
        if title_tag and price_tag:
            listings.append({
                "name": title_tag.get_text(strip=True),
                "price_usd": price_tag.get_text(separator="", strip=True),
            })

    if not listings:
        with open("spothero_source.html", "w") as f:
            f.write(page_source)
        print("No listings parsed — raw source saved to spothero_source.html")

    return listings


if __name__ == "__main__":
    with SB(uc=True, test=True) as sb:
        listings = search_hourly(
            sb,
            search_string="San Francisco, CA",
            latitude=37.7749295,
            longitude=-122.4194155,
            start=datetime(2026, 2, 23, 22, 0),
            end=datetime(2026, 2, 24, 1, 0),
        )
        print(f"Found {len(listings)} hourly listings")
        for listing in listings:
            print(listing)

        monthly_listings = search_monthly(
            sb,
            search_string="San Francisco, CA",
            latitude=37.7749295,
            longitude=-122.4194155,
            start=datetime(2026, 2, 23),
        )
        print(f"Found {len(monthly_listings)} monthly listings")
        for listing in monthly_listings:
            print(listing)

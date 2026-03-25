"""
One-time script to seed the Firestore `cities` collection.
Run: python seed_cities.py
"""
from google.cloud import firestore

CITIES = [
    {"location": "Atlanta, GA",        "city": "atlanta",        "state": "ga"},
    {"location": "Austin, TX",         "city": "austin",         "state": "tx"},
    {"location": "Baltimore, MD",      "city": "baltimore",      "state": "md"},
    {"location": "Boston, MA",         "city": "boston",         "state": "ma"},
    {"location": "Charlotte, NC",      "city": "charlotte",      "state": "nc"},
    {"location": "Chicago, IL",        "city": "chicago",        "state": "il"},
    {"location": "Cincinnati, OH",     "city": "cincinnati",     "state": "oh"},
    {"location": "Cleveland, OH",      "city": "cleveland",      "state": "oh"},
    {"location": "Columbus, OH",       "city": "columbus",       "state": "oh"},
    {"location": "Dallas, TX",         "city": "dallas",         "state": "tx"},
    {"location": "Denver, CO",         "city": "denver",         "state": "co"},
    {"location": "Detroit, MI",        "city": "detroit",        "state": "mi"},
    {"location": "Houston, TX",        "city": "houston",        "state": "tx"},
    {"location": "Indianapolis, IN",   "city": "indianapolis",   "state": "in"},
    {"location": "Kansas City, MO",    "city": "kansas-city",    "state": "mo"},
    {"location": "Las Vegas, NV",      "city": "las-vegas",      "state": "nv"},
    {"location": "Los Angeles, CA",    "city": "los-angeles",    "state": "ca"},
    {"location": "Louisville, KY",     "city": "louisville",     "state": "ky"},
    {"location": "Memphis, TN",        "city": "memphis",        "state": "tn"},
    {"location": "Miami, FL",          "city": "miami",          "state": "fl"},
    {"location": "Milwaukee, WI",      "city": "milwaukee",      "state": "wi"},
    {"location": "Minneapolis, MN",    "city": "minneapolis",    "state": "mn"},
    {"location": "Nashville, TN",      "city": "nashville",      "state": "tn"},
    {"location": "New Orleans, LA",    "city": "new-orleans",    "state": "la"},
    {"location": "New York City, NY",  "city": "new-york-city",  "state": "ny"},
    {"location": "Oakland, CA",        "city": "oakland",        "state": "ca"},
    {"location": "Oklahoma City, OK",  "city": "oklahoma-city",  "state": "ok"},
    {"location": "Orlando, FL",        "city": "orlando",        "state": "fl"},
    {"location": "Philadelphia, PA",   "city": "philadelphia",   "state": "pa"},
    {"location": "Phoenix, AZ",        "city": "phoenix",        "state": "az"},
    {"location": "Pittsburgh, PA",     "city": "pittsburgh",     "state": "pa"},
    {"location": "Portland, OR",       "city": "portland",       "state": "or"},
    {"location": "Raleigh, NC",        "city": "raleigh",        "state": "nc"},
    {"location": "Richmond, VA",       "city": "richmond",       "state": "va"},
    {"location": "St. Louis, MO",      "city": "st-louis",       "state": "mo"},
    {"location": "Salt Lake City, UT", "city": "salt-lake-city", "state": "ut"},
    {"location": "San Antonio, TX",    "city": "san-antonio",    "state": "tx"},
    {"location": "San Francisco, CA",  "city": "san-francisco",  "state": "ca"},
    {"location": "Seattle, WA",        "city": "seattle",        "state": "wa"},
    {"location": "Tampa, FL",          "city": "tampa",          "state": "fl"},
    {"location": "Washington, DC",     "city": "washington",     "state": "dc"},
    {"location": "Arlington, VA",      "city": "arlington",      "state": "va"},
    {"location": "Durham, NC",         "city": "durham",         "state": "nc"},
    {"location": "El Paso, TX",        "city": "el-paso",        "state": "tx"},
    {"location": "Fort Worth, TX",     "city": "fort-worth",     "state": "tx"},
    {"location": "Sacramento, CA",     "city": "sacramento",     "state": "ca"},
    {"location": "San Diego, CA",      "city": "san-diego",      "state": "ca"},
]


def main():
    db = firestore.Client()
    col = db.collection("cities")
    for entry in CITIES:
        doc_id = f"{entry['city']}-{entry['state']}"
        col.document(doc_id).set({**entry, "enabled": True})
        print(f"Seeded {doc_id}")
    print(f"\nDone — {len(CITIES)} cities seeded.")


if __name__ == "__main__":
    main()

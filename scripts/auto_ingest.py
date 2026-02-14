import json
import random
import wikipedia
import requests
import warnings
from geopy.geocoders import Nominatim
from pathlib import Path

warnings.filterwarnings("ignore")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mysteries.json"
geolocator = Nominatim(user_agent="geomyst")

TOPICS = [
    "lost cities",
    "abandoned places",
    "ancient ruins",
    "forgotten infrastructure",
    "strange archaeological discoveries",
    "historic observatories"
]


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def try_get_coordinates(title):
    """
    Try to fetch coordinates. If not found, return None.
    """
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageprops",
            "format": "json"
        }

        r = requests.get(url, params=params, timeout=10).json()
        pages = r["query"]["pages"]
        page = next(iter(pages.values()))

        wikidata_id = page.get("pageprops", {}).get("wikibase_item")
        if not wikidata_id:
            return None

        wd_url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
        wd = requests.get(wd_url, timeout=10).json()

        entity = wd["entities"][wikidata_id]
        claims = entity.get("claims", {})

        if "P625" in claims:
            coord = claims["P625"][0]["mainsnak"]["datavalue"]["value"]
            return coord["latitude"], coord["longitude"]

    except Exception:
        return None

    return None


def reverse_location(lat, lon):
    try:
        loc = geolocator.reverse((lat, lon), language="en", timeout=10)
        addr = loc.raw.get("address", {})
        return addr.get("state") or addr.get("country") or "Unknown Region"
    except Exception:
        return "Unknown Region"


def generate_entry():
    topic = random.choice(TOPICS)
    print(f"Searching topic: {topic}")

    results = wikipedia.search(topic, results=10)
    if not results:
        raise Exception("No Wikipedia results found.")

    title = random.choice(results)
    print(f"Selected article: {title}")

    try:
        summary = wikipedia.summary(title, sentences=4)
    except Exception:
        summary = "Historical references to this subject exist, but detailed records remain scarce."

    coords = try_get_coordinates(title)

    if coords:
        lat, lon = coords
        state = reverse_location(lat, lon)
        print("Coordinates found.")
    else:
        # No retry. Accept mystery without location.
        lat = None
        lon = None
        state = "Unmapped"
        print("No coordinates. Stored as an unmapped mystery.")

    return {
        "id": f"auto_{random.randint(10000,99999)}",
        "title": title,
        "lat": lat,
        "lng": lon,
        "state": state,
        "year": "Unknown",
        "category": "Auto-Discovered",
        "summary": summary,
        "why_faded": "The subject persisted in fragmented records and never anchored itself to a single documented location."
    }


def main():
    print("\nGenerating new mystery...")

    data = load_data()
    entry = generate_entry()
    data.append(entry)
    save_data(data)

    print(f"Added: {entry['title']} → {entry['state']}")


if __name__ == "__main__":
    main()

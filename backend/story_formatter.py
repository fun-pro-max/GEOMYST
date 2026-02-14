import random

def format_story(entry):
    tones = [
        "Researchers noted that",
        "Archival fragments suggest",
        "Historical traces reveal that",
        "Local accounts describe how",
        "Survey records indicate"
    ]

    mystery_angles = [
        "No clear explanation exists for why it faded from documentation.",
        "Its disappearance from records remains unresolved.",
        "Scholars still debate its original purpose.",
        "The timeline surrounding it contains unexplained gaps.",
        "Its presence challenges accepted historical narratives."
    ]

    topic = entry.get("category", "Historical Anomaly")
    place = entry.get("title", "Unknown Location")
    fact_base = entry.get("summary", "Limited information survives.")
    fact = f"{random.choice(tones)} {fact_base}"
    mystery = random.choice(mystery_angles)

    return {
        "topic": topic,
        "place": place,
        "fact": fact,
        "mystery": mystery,
        "lat": entry.get("lat"),
        "lng": entry.get("lng"),
        "state": entry.get("state")
    }

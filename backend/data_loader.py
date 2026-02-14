import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mysteries.json"

def load_mysteries():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

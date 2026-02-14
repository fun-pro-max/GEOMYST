from story_formatter import format_story

import random

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel
from data_loader import load_mysteries
from story_engine import pick_story

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mysteries = load_mysteries()

class StoryRequest(BaseModel):
    state: str
    seen: list[str]

@app.get("/")
def home():
    return {"message": "GeoMyst backend running"}

@app.post("/story")
def get_story(req: StoryRequest):
    
    entry = pick_story(mysteries, req.state, req.seen)

    # Format response to match new frontend design
    formatted_story = {
        "id": entry.get("id"),
        "heading": entry.get("heading"),
        "place": entry.get("place"),
        "fact": entry.get("fact"),
        "mystery": entry.get("mystery"),
        "lat": entry.get("lat"),
        "lng": entry.get("lng"),
        "state": entry.get("state")
    }

    return formatted_story



@app.get("/random-location")
def random_location():
    mystery = random.choice(mysteries)
    return {
        "lat": mystery["lat"],
        "lng": mystery["lng"],
        "state": mystery["state"]
    }

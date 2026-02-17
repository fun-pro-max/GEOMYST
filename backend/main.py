import random
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ✅ Correct package imports
from backend.data_loader import load_mysteries
from backend.story_engine import pick_story
from backend.story_formatter import format_story

# --------------------------------------------------
# App Setup
# --------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Serve frontend files
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")


# --------------------------------------------------
# Load Data
# --------------------------------------------------

mysteries = load_mysteries()


# --------------------------------------------------
# Models
# --------------------------------------------------

class StoryRequest(BaseModel):
    state: str
    seen: list[str]


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def serve_home():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.post("/story")
def get_story(req: StoryRequest):

    entry = pick_story(mysteries, req.state, req.seen)

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
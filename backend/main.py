import random
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ✅ Package imports (important for Render)
from backend.data_loader import load_mysteries
from backend.story_engine import pick_story

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
# Paths (Render-safe absolute paths)
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve JS/CSS as static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

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

# Serve the website
@app.get("/")
def serve_home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/story")
def get_story(req: StoryRequest):

    entry = pick_story(mysteries, req.state, req.seen)

    return {
        "id": entry.get("id"),
        "heading": entry.get("heading"),
        "place": entry.get("place"),
        "fact": entry.get("fact"),
        "mystery": entry.get("mystery"),
        "lat": entry.get("lat"),
        "lng": entry.get("lng"),
        "state": entry.get("state"),
    }


@app.get("/random-location")
def random_location():
    mystery = random.choice(mysteries)
    return {
        "lat": mystery["lat"],
        "lng": mystery["lng"],
        "state": mystery["state"],
    }

# Serve PWA manifest
@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(FRONTEND_DIR / "manifest.json", media_type="application/json")


# Serve service worker at ROOT (important!)
@app.get("/sw.js")
def serve_sw():
    return FileResponse(FRONTEND_DIR / "sw.js", media_type="application/javascript")

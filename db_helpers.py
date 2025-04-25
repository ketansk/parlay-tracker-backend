from tinydb import TinyDB, Query
from datetime import datetime

# Open your persistent JSON DB
db = TinyDB("sports_tracker_data.json")

# Access different tables
parlays_table = db.table("parlays")
scores_table = db.table("live_scores")
rosters_table = db.table("rosters")
meta_table = db.table("meta")

### 🔁 PARLAYS

def save_parlay(parlay: dict):
    """Insert a new parlay into the database."""
    parlay.setdefault("status", "pending")
    parlay.setdefault("created_at", datetime.utcnow().isoformat())
    return parlays_table.insert(parlay)

def get_parlays_by_user(user_id: str):
    """Get all parlays for a specific user."""
    Parlay = Query()
    return parlays_table.search(Parlay.user_id == user_id)

def update_parlay_status(parlay_id: int, status: str):
    """Update the status of a parlay."""
    return parlays_table.update({"status": status}, doc_ids=[parlay_id])

### 📊 LIVE SCORES (API CACHE)

def cache_scores(key: str, data: dict):
    """Cache score data with a timestamp."""
    Score = Query()
    return scores_table.upsert({
        "key": key,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }, Score.key == key)

def get_cached_scores(key: str):
    """Fetch cached scores by key."""
    Score = Query()
    result = scores_table.get(Score.key == key)
    return result["data"] if result else None

### 👥 ROSTERS

def save_team_roster(team: str, players: list):
    """Save or update a team's roster."""
    Roster = Query()
    return rosters_table.upsert({
        "team": team,
        "players": players,
        "fetched_at": datetime.utcnow().isoformat()
    }, Roster.team == team)

def get_team_roster(team: str):
    """Fetch a cached team roster."""
    Roster = Query()
    result = rosters_table.get(Roster.team == team)
    return result["players"] if result else None

### 🧠 VERSIONING

def get_db_version():
    Version = Query()
    entry = meta_table.get(Version.key == "db_version")
    return entry["version"] if entry else None

def set_db_version(version: int):
    Version = Query()
    meta_table.upsert({"key": "db_version", "version": version}, Version.key == "db_version")

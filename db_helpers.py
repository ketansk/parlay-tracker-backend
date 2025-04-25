from tinydb import TinyDB, Query
from datetime import datetime
import uuid

from models import Parlay, ParlayLeg

# Open your persistent JSON DB
db = TinyDB("sports_tracker_data.json")

# Access different tables
parlays_table = db.table("parlays")
scores_table = db.table("live_scores")
rosters_table = db.table("rosters")
meta_table = db.table("meta")

### 🔁 PARLAYS


def save_parlay(parlay_data: dict):
    legs = [ParlayLeg(**leg) for leg in parlay_data["legs"]]
    parlay = Parlay(
        wager=parlay_data["wager"],
        odds=parlay_data["odds"],
        legs=legs,
        status="pending",
    )
    doc = parlay.dict()
    doc["parlay_id"] = str(uuid.uuid4())
    parlays_table.insert(doc)
    return doc


def get_parlays_by_user(user_id: str):
    results = parlays_table.search(Query().user_id == user_id)
    return [Parlay(**item) for item in results]


# Update the status of a parlay
def update_parlay_status(user_id, parlay_id, status):
    parlays_table.update(
        {"status": status},
        (Query().user_id == user_id) & (Query().parlay_id == parlay_id),
    )


# Delete a parlay
def delete_parlay(user_id, parlay_id):
    parlays_table.remove(
        (Query().user_id == user_id) & (Query().parlay_id == parlay_id)
    )


### 📊 LIVE SCORES (API CACHE)


def cache_scores(key: str, data: dict):
    """Cache score data with a timestamp."""
    Score = Query()
    return scores_table.upsert(
        {"key": key, "data": data, "timestamp": datetime.utcnow().isoformat()},
        Score.key == key,
    )


def get_cached_scores(key: str):
    """Fetch cached scores by key."""
    Score = Query()
    result = scores_table.get(Score.key == key)
    return result["data"] if result else None


### 👥 ROSTERS


def save_team_roster(team: str, players: list):
    """Save or update a team's roster."""
    Roster = Query()
    return rosters_table.upsert(
        {"team": team, "players": players, "fetched_at": datetime.utcnow().isoformat()},
        Roster.team == team,
    )


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
    meta_table.upsert(
        {"key": "db_version", "version": version}, Version.key == "db_version"
    )

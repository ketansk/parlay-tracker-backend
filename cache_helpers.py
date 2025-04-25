import os
import json
import time

ROSTER_CACHE_FILE = "roster_cache.json"
ROSTER_CACHE_DURATION = 604800  # One week in seconds


def get_cached_data(team_id):
    if not os.path.exists(ROSTER_CACHE_FILE):
        print("doesn't exist!")
        return None

    with open(ROSTER_CACHE_FILE, "r") as f:
        try:
            cache = json.load(f)
            team = cache.get(team_id)
            if team:
                if time.time() - team["timestamp"] < ROSTER_CACHE_DURATION:
                    return team["players"]
        except Exception as e:
            return None
    return None


def save_to_cache(players, team_id):
    with open(ROSTER_CACHE_FILE, "r") as f:
        cache = json.load(f)
    cache[team_id] = {"timestamp": time.time(), "players": players}
    with open(ROSTER_CACHE_FILE, "w") as f:
        json.dump(cache, f)

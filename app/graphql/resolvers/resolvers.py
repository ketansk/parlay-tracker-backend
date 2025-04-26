from datetime import date, timedelta
import os
import requests
from ariadne import QueryType, MutationType
from app.models.parlay_models import Parlay, ParlayLeg
from app.services.cache_helpers import get_cached_data, save_to_cache
from app.storage.tinydb.tinydb_helpers import save_parlay, get_parlays_by_user


query = QueryType()
mutation = MutationType()

DAY_OFFSET = 0

HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
}

BASE_URL = "https://tank01-fantasy-stats.p.rapidapi.com"


@query.field("liveGames")
def resolve_live_games(*_):
    url = f"{BASE_URL}/getNBAScoresOnly"
    game_date = date.today() + timedelta(DAY_OFFSET)
    params = {"gameDate": game_date.strftime("%Y%m%d")}
    response = requests.get(url, headers=HEADERS, params=params)
    games = response.json().get("body", {})

    return [
        {
            "id": games[game]["gameID"],
            "homeTeam": games[game]["home"],
            "awayTeam": games[game]["away"],
            "homeScore": games[game]["homePts"],
            "awayScore": games[game]["awayPts"],
            "gameClock": games[game]["gameClock"],
        }
        for game in games
    ]


@query.field("livePlayerStats")
def resolve_live_player_stats(_, info, gameId, playerIds=[]):
    url = f"{BASE_URL}/getNBABoxScore"
    params = {"gameID": gameId}
    response = requests.get(url, headers=HEADERS, params=params)
    players = response.json().get("body", {}).get("playerStats", {})
    if playerIds:
        player_id_set = set(playerIds)
    else:
        player_id_set = set(players.keys())

    return [
        {
            "id": player,
            "name": players[player].get("longName"),
            "points": players[player].get("pts"),
            "rebounds": players[player].get("reb"),
            "assists": players[player].get("ast"),
            "steals": players[player].get("stl"),
            "blocks": players[player].get("blk"),
        }
        for player in players
        if player in player_id_set
    ]


@query.field("teamRoster")
def resolve_team_roster(_, info, teamId):
    players = get_cached_data(teamId)
    if not players:
        url = f"{BASE_URL}/getNBATeamRoster"
        params = {"teamAbv": teamId}
        print("FETCHING TEAM ROSTER")
        response = requests.get(url, headers=HEADERS, params=params)
        players = response.json()["body"]["roster"]
        save_to_cache(players, teamId)

    return [
        {
            "id": p["playerID"],
            "name": p["nbaComName"],
            "position": p["pos"],
            "team": p["team"],
            "headshot": p["nbaComHeadshot"],
        }
        for p in players
    ]


@query.field("fetchParlay")
def resolve_fetch_parlay(_, info, userId: str):
    parlays = get_parlays_by_user(userId)
    return [
        {
            "wager": p.wager,
            "odds": p.odds,
            "status": p.status,
            "legs": p.legs,
        }
        for p in parlays
    ]


@mutation.field("saveParlay")
def resolve_save_parlay(_, info, parlay):
    parlay_obj = Parlay(
        {
            "user_id": parlay["user_id"],
            "wager": parlay["wager"],
            "odds": parlay["odds"],
            "status": parlay["status"],
            "legs": [ParlayLeg(**leg) for leg in parlay["legs"]],
        }
    )

    parlay_id = save_parlay(parlay_obj)

    return {"success": True, "parlay_id": parlay_id}

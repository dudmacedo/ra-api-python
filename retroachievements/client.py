import requests as request
from retroachievements import __version__
from datetime import datetime, date


_BASE_URL = "https://retroachievements.org/API/"

"""
Main class for accessing the RetroAhievements Web API
"""
class RAClient:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        self.headers = {"User-Agent": "RetroAchievements-api-python/" + __version__}

    def url_params(self, params=None):
        """
        Inserts the auth and query params into the request
        """
        if params is None:
            params = {}
        params.update({"z": self.username, "y": self.api_key})
        return params

    ### URL construction
    def _call_api(self, endpoint=None, params=None, timeout=30, headers=None):
        if endpoint is None:
            endpoint = {}
        req = request.get(
            f"{_BASE_URL}{endpoint}",
            params=self.url_params(params),
            timeout=timeout,
            headers=headers,
        )
        return req

    ### User endpoints

    """
    Get a user's minimal profile information, such as their ID, motto, most recent game ID, avatar, and points.

    Params:
        u: Username to query
    """
    def get_user_profile(self, user: str) -> dict:
        result = self._call_api("API_GetUserProfile.php?", {"u": user}).json()
        return result

    """
    Get user's recently unlocked achievements, via their username. By default, it fetches achievements unlocked in the last hour

    Params:
        user: Username to query
        minutes: Minutes to look back. Defaults to 60
    """
    def get_user_unlocks_recent(self, user: str, minutes=60) -> dict:
        result = self._call_api("API_GetUserRecentAchievements.php?", {"u": user, "m": minutes}).json()
        return result

    """
    Get user's unlocks between two given dates

    Params:
        user: Username to query
        start: Time range start
        end: Time range end
    """
    def get_user_unlocks_date_range(self, user: str, start: datetime, end: datetime) -> dict:
        result = self._call_api("API_GetAchievementsEarnedBetween.php?", {"u": user, "f": start.timestamp(), "t": end.timestamp()})
        return result

    """
    Get user's unlocks on a specific date

    Params:
        user: Username to query
        day: Date to query
    """
    def get_user_unlocks_on_date(self, user: str, day: date) -> dict:
        result = self._call_api("API_GetAchievementsEarnedOnDay.php?", {"u": user, "d": day.strftime("%Y-%m-%d")})
        return result

    """
    Get extended metadata about a game, in addition to a user's progress about that game. This is targeted via a game's unique ID and a given username

    Params:
        user: Username to query
        game_id: The target game ID
        award: Set "True" if user award metadata shoud be included
    """
    def get_user_game_progress(self, user: str, game_id: int, award: bool = False) -> dict:
        result = self.call_api("API_GetGameInfoAndUserProgress.php?", {"u": user, "g": game_id, "a": 1 if award else 0})
        return result

    """
    Get a given user's completion progress in all played games, targeted by their username

    Params:
        user: Username to query
        count: Number of records to return (default: 100, max: 500)
        offset: Number of entries to skip (default: 0)
    """
    def get_user_all_progress(self, user: str, count: int = 100, offset: int = 0) -> dict:
        result = self._call_api("API_GetUserCompletionProgress.php?", {"u": user, "c": count, "o": offset}).json()
        return result

    """
    Get metadata about the target user's site awards, via their username

    Params:
        user: The target username
    """
    def get_user_awards(self, user: str) -> dict:
        result = self._call_api("API_GetUserAwards.php?", {"u": user}).json()
        return result

    """
    Get list of achievement set claims made over the lifetime of a given user, targeted by their username

    Params:
        user: The target username
    """
    def get_user_claims(self, user: str) -> dict:
        result = self._call_api("API_GetUserClaims.php?", {"u": user}).json()
        return result

    """
    Get metadata about how a given user has performed/ranked on a given game, targeted by game ID

    Params:
        user: The target username
        game_id: The target game ID
    """
    def get_user_rank_score(self, user: str, game_id: int) -> dict:
        result = self._call_api("API_GetUserGameRankAndScore.php?", {"u": user, "g": game_id}).json()
        return result

    """
    Get a user's total hardcore and softcore points

    Params:
        user: The target username
    """
    def get_user_points(self, user: str) -> dict:        
        result = self._call_api("API_GetUserPoints.php?", {"u": user}).json()
        return result
    
    """
    Get a given user's progress on a given list of games, targeted by a list of game IDs

    Params:
        user: The target username
        games_ids: List containing one or more game IDs
    """
    def get_user_specific_games_progress(self, user: str, games_ids: list) -> dict:
        result = self._call_api("API_GetUserProgress.php?", {"u": user, "i": ",".join(games_ids)}).json()
        return result
    
    """
    Get a list of a target user's recently played games, via their username

    Params:
        user: The target username
        count: Number of records to return (default: 10, max: 50)
        offset: Number of entries to skip (default: 0)
    """
    def get_user_recently_played(self, user: str, count: int = 10, offset: int = 0) -> dict:
        result = self._call_api("API_GetUserRecentlyPlayedGames.php?", {"u": user, "c": count, "o": offset}).json()
        return result

    """
    Get summary information about a given user, targeted by username

    Params:
        user: The target username
        recent_games: Number of recent games to return (default: 0)
        recent_cheevos: Number of recent achievements to return (default: 10)
    """
    def get_user_summary(self, user: str, recent_games: int = 0, recent_cheevos: int = 10) -> dict:
        result = self._call_api("API_GetUserSummary.php?", {"u": user, "g": recent_games, "a": recent_cheevos},).json()
        return result
    
    """
    Get completion metadata about the games a given user has played. It returns two entries per each game: one for the 
    softcore completion and one for the hardcore completion. These are designated by the hardcoreMode property on each
    completion object.

    Params:
        user: The target username
    """
    def get_user_completed_games(self, user: str) -> dict:
        result = self._call_api("API_GetUserCompletedGames.php?", {"u": user}).json()
        return result
    
    """
    Get a given user's "Want to Play Games" list, targeted by their username. Results will only be returned if the target
    user is yourself, or if both you and the target user follow each other.

    Params:
        user: The target username
        count: Number of records to return (default: 100, max: 500)
        offset: Number of entries to skip (default: 0)
    """
    def get_user_want_to_play_list(self, user: str, count: int = 100, offset: int = 0) -> dict:
        result = self._call_api("API_GetUserWantToPlayList.php?", {"u": user, "c": count, "o": offset}).json()
        return result

    ### Game endpoints

    """
    Get basic metadata about a game

    Params:
        game_id: The target game ID
    """
    def get_game_summary(self, game_id: int) -> dict:        
        result = self._call_api("API_GetGame.php?", {"i": game_id}).json()
        return result

    """
    Get extended metadata about a game

    Params:
        game_id: The target game ID
    """
    def get_game_extended(self, game_id: int) -> dict:
        result = self._call_api("API_GetGameExtended.php?", {"i": game_id}).json()
        return result

    """
    Get game hashes

    Params:
        game_id: The target game ID
    """
    def get_game_hashes(self, game_id:int) -> dict:
        result = self._call_api("API_GetGameHashes.php?", {"i": game_id}).json()
        return result

    """
    Get the list of achievement ID's for a game

    Params:
        game_id: The target game ID
    """
    def get_game_achievement_count(self, game_id: int) -> dict:
        result = self._call_api("API_GetAchievementCount.php?", {"i": game_id}).json()
        return result
    
    """
    Get how many players have unlocked how many achievements for a game

    Params:
        game_id: The target game ID
        hardcore: Query hardcore unlocks (default: False)
        official: True for official achievements, False for unofficial achievements. (default: True)
    """
    def get_game_achievement_distribution(self, game_id: int, hardcore: bool = False, official: bool = True) -> dict:
        result = self._call_api("API_GetAchievementDistribution.php?", {"i": game_id, "h": 1 if hardcore else 0, "f": 3 if official else 5}).json()
        return result

    """
    Get metadata about either the latest masters for a game, or the highest points earners for a game

    Params:
        game_id: The target game ID
        masters: True for latest masters, False for non-masters high scores. (default: False)
    """
    def get_game_high_scores(self, game_id: int, masters: bool = False) -> dict:
        result = self._call_api("API_GetGameRankAndScore.php?", {"i": game_id, "t": 1 if masters else 0}).json()
        return result

    # System Endpoints

    def get_console_ids(self) -> list:
        """
        Get the complete list of console ID and name pairs on the site

        Params:
            None
        """
        result = self._call_api("API_GetConsoleIDs.php?", {}).json()
        return result

    def get_game_list(self, system: int, has_cheevos=0, hashes=0) -> dict:
        """
        Get the complete list of games for a console

        Params:
            i: The system ID to query
            f: If 1, only returns games that have achievements (default = 0)
            h: If 1, also return the supported hashes for games (default = 0)
        """
        result = self._call_api(
            "API_GetGameList.php?", {
                "i": system, "f": has_cheevos, "h": hashes}
        ).json()
        return result

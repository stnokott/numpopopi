from dataclasses import dataclass
from logging import Logger
from os import environ

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Client(object):
    def __init__(self, logger: Logger):
        logger.info("authenticating using client credentials flow")
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self._sp = sp
        if not self._validate_auth():
            raise ValueError("test query failed")
        logger.info("authenticated")
        self._logger = logger

    def _validate_auth(self) -> bool:
        markets = self._sp.available_markets()
        return bool(markets)

    def search(self, q: str):
        results = self._sp.search(q, limit=12)
        if not results:
            return []
        return [Song.from_api_response(s) for s in results["tracks"]["items"]]


@dataclass
class Song:
    name: str
    artist: str
    duration_ms: int
    img_url: str
    uri: str

    @staticmethod
    def from_api_response(data: dict) -> "Song":
        return Song(
            data["name"],
            " & ".join([art["name"] for art in data["artists"]]),
            data["duration_ms"],
            data["album"]["images"][1]["url"],
            data["uri"],
        )

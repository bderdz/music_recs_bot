import base64
from enum import Enum

from music_yoda import config
from music_yoda.utils import HttpClient


# Search type Enum
class SearchType(Enum):
    ARTIST = "artists"
    TRACK = "tracks"


class Spotify:
    API_URL: str = "https://api.spotify.com/v1"
    token: str

    def __init__(self, token: str):
        self.token = token

    # Token request
    @staticmethod
    async def get_token() -> str:
        url: str = "https://accounts.spotify.com/api/token"
        client: HttpClient = HttpClient(url=url)
        auth_string: str = config.CLIENT_ID + ":" + config.CLIENT_SECRET
        auth_bytes: bytes = auth_string.encode("utf-8")
        auth_base64: str = str(base64.b64encode(auth_bytes), "utf-8")

        headers: dict[str, str] = {
            "Authorization": "Basic " + auth_base64
        }
        body: dict[str, str] = {"grant_type": 'client_credentials'}

        response: dict[str, str] = await client.send_post(body=body, headers=headers)

        return response["access_token"]

    # Headers for request to spotify api
    def __get_auth_header(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.token}

    # Music genres request
    async def get_genres(self) -> list[str]:
        url: str = f"{self.API_URL}/recommendations/available-genre-seeds"
        headers: dict[str, str] = self.__get_auth_header()
        client: HttpClient = HttpClient(url=url)

        response: dict[str, list[str]] = await client.send_get(headers=headers)

        return [] if "error" in response else response["genres"]

    # Search query based on provided SearchType enum value (song / artist)
    # Returns 5 search results mapped to: { name, id }
    async def search(self, query: str, search_type: SearchType) -> list[dict[str, str]]:
        headers = self.__get_auth_header()
        url: str = f"{self.API_URL}/search?q={query}&limit=5"
        match search_type:
            case SearchType.ARTIST:
                url += "&type=artist"
            case SearchType.TRACK:
                url += "&type=track"

        client: HttpClient = HttpClient(url)

        response: dict = (await client.send_get(headers)).get(search_type.value)
        items: list[dict] = response.get("items")

        result: list[dict[str, str]] = list(
            map(lambda item: {
                "name": f"{item.get("name")}",
                "id": item.get("id")},
                items))

        return result

    # Recommendation query
    async def get_recs(
            self,
            genres: list[str] = None,
            artists: list[str] = None,
            tracks: list[str] = None,
            limit: int = 1) -> list[dict]:

        # Creates a URL based on the given parameters:
        # limit and add any provided seeds (genres, artists, tracks)
        url: str = f"{self.API_URL}/recommendations?limit={limit}"
        if genres:
            url += "&seed_genres=" + ",".join(genres)
        if artists:
            url += "&seed_artists=" + ",".join(artists)
        if tracks:
            url += "&seed_tracks=" + ",".join(tracks)
        # Return an empty list if no seeds are provided
        if not (genres or artists or tracks):
            return []

        client: HttpClient = HttpClient(url)
        headers = self.__get_auth_header()

        response = await client.send_get(headers=headers)

        return response.get("tracks")

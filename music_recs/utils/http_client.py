from typing import Any
from aiohttp import ClientSession, ClientResponseError


class HttpClient:
    url: str

    def __init__(self, url: str):
        self.url = url

    def set_url(self, url: str):
        self.url = url

    async def send_post(self, body: dict[str, str], headers: dict[str, str]) -> dict[str, Any]:
        async with ClientSession() as session:
            try:
                async with session.post(url=self.url, data=body, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        response.raise_for_status()

            except ClientResponseError as e:
                print(f"HTTP POST error: {e.status} - {e.message}")
                return {"error": e.status}

    async def send_get(self, headers: dict[str, str]) -> dict[str, Any]:
        async with ClientSession() as session:
            try:
                async with session.get(url=self.url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        response.raise_for_status()

            except ClientResponseError as e:
                print(f"HTTP GET error: {e.status} - {e.message}")
                return {"error": e.status}

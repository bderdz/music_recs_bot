from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from music_yoda.api.spotify import Spotify


class SpotifyMiddleware(BaseMiddleware):
    spotify: Spotify

    def __init__(self, token: str) -> None:
        self.spotify = Spotify(token=token)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        data['spotify'] = self.spotify

        return await handler(event, data)

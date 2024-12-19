import asyncio
from aiogram import Bot, Dispatcher

from music_yoda import config
from music_yoda.api.spotify import Spotify

from music_yoda.handlers import start, general, recs, preview
from music_yoda.utils import set_commands
from music_yoda.middlewares import SpotifyMiddleware


async def main() -> None:
    bot: Bot = Bot(token=config.TOKEN, default=config.PROPERTIES)
    dp: Dispatcher = Dispatcher()
    spotify_token: str = await Spotify.get_token()  # Spotify token

    # Applying middleware
    dp.update.middleware(SpotifyMiddleware(token=spotify_token))

    # Handlers
    dp.include_routers(
        general.router,
        start.router,
        recs.router,
        preview.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher

from music_yoda import config
from music_yoda.api.spotify import Spotify
from music_yoda.handlers import start, general
from music_yoda.utils import set_commands


async def main() -> None:
    bot: Bot = Bot(config.TOKEN)
    dp: Dispatcher = Dispatcher()
    spotify_token: str = await Spotify.get_token()  # Spotify token
    spotify: Spotify = Spotify(token=spotify_token)  # Spotify api

    dp.include_routers(
        general.router,
        start.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

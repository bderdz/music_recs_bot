from aiogram import Bot
from aiogram.types import BotCommandScopeDefault
from music_yoda import config


async def set_commands(bot: Bot) -> None:
    await bot.delete_my_commands()
    await bot.set_my_commands(commands=config.commands, scope=BotCommandScopeDefault())

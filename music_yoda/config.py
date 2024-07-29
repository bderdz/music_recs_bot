import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram.types import BotCommand

# .env
load_dotenv()
TOKEN = os.environ.get("TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)

# list of bot commands
commands: list[BotCommand] = [
    BotCommand(command="/start", description="🏁 start")
]

import os
from dotenv import load_dotenv
from aiogram.types import BotCommand

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

commands: list[BotCommand] = [
    BotCommand(command="/start", description="🏁 start")
]

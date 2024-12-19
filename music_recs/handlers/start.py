from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from music_yoda.keyboards.general import main_keyboard

router: Router = Router()

welcome_text: str = """👋 <b>Hello there {name}!</b>

🎧 This bot will help you discover new music on Spotify suited to your preferences quickly and easily.
<b>Choose your inspirations, and we’ll handle the rest!</b>

❔ <i>You can use the menu buttons to navigate or commands like /recs to go to recommendation</i>"""


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.delete()

    first_name: str = message.from_user.first_name

    await message.answer(
        text=welcome_text.format(name=first_name),
        reply_markup=main_keyboard())

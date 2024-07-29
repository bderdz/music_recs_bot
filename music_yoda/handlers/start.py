from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from music_yoda.keyboards import general

router: Router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(text="Hello there", reply_markup=general.main_keyboard())

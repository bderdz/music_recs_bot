from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router: Router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(text="Hi")

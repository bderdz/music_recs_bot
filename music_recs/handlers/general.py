from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

router: Router = Router()


@router.callback_query(F.data == "close")
async def process_close(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await state.clear()

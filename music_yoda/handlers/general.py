from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

router: Router = Router()


def support_button() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    builder.button(
        text="☕️ Buy me a coffee",
        url="https://www.buymeacoffee.com/b.derdz")

    return builder.as_markup()


@router.message(StateFilter(None), Command("support"))
@router.message(StateFilter(None), F.text == "🎁 Support Author")
async def support_handler(message: Message) -> None:
    await message.delete()
    await message.answer(
        text="<b>I would really appreciate your support 🫶</b>",
        reply_markup=support_button())


@router.callback_query(F.data == "close")
async def process_close(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await state.clear()

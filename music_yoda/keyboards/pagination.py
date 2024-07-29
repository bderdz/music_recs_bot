from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def pagination_keyboard(page: int, length: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="◀️" if page > 0 else "✖️",
        callback_data=Pagination(action="prev", page=0 if page == 0 else page - 1))

    builder.button(
        text=f"{page + 1}/{length + 1}",
        callback_data=Pagination(action="idle", page=page))

    builder.button(
        text="️▶️" if page < length else "✖️",
        callback_data=Pagination(action="next", page=length if page == length else page + 1))

    builder.button(text="❌ Close", callback_data=Pagination(action="summary", page=page))

    builder.adjust(3, 1)

    return builder

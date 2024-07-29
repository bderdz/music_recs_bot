from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from music_yoda.keyboards import pagination


def preview_keyboard(url: str, page: int, length: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    builder.button(text="Open in Spotify 🎧", url=url)
    
    if length > 0:
        builder.attach(pagination.pagination_keyboard(page=page, length=length))
        builder.adjust(1, 3)

    return builder.as_markup()

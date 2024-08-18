from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, ReplyKeyboardBuilder


def main_keyboard() -> ReplyKeyboardMarkup:
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: [str] = [
        "🎲 Recommendations",
        "🎁 Support Author"
    ]

    for button in buttons:
        builder.button(text=button)

    builder.adjust(1, 1, 1)

    return builder.as_markup(resize_keyboard=True)


def back_button() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text="◀️ Back", callback_data="back")

    return builder


def close_button() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text="❌ Close", callback_data="close")

    return builder

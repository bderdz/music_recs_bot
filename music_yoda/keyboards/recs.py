from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from music_yoda.keyboards.general import back_button


def recs_keyboard(seed_amount: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    seed_buttons: list[list[str]] = [
        ["Add tracks", "tracks"],
        ["Add artists", "artists"],
        ["Add genres", "genres"],
    ]

    if seed_amount < 5:
        for button in seed_buttons:
            builder.button(text=button[0], callback_data=f"recs_{button[1]}")

    if seed_amount != 0:
        builder.button(text="Submit", callback_data="recs_limit")

    builder.adjust(3, 1)

    return builder.as_markup()


def search_keyboard(n_buttons: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for i in range(n_buttons):
        builder.button(text=f"{i + 1}", callback_data=f"search_{i}")

    builder.attach(back_button())
    builder.adjust(n_buttons, 1)

    return builder.as_markup()


def limit_keyboard() -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[str] = ["1", "5", "10", "20", "50", "100"]

    for button in buttons:
        builder.button(text=button, callback_data=f"limit_{button}")

    builder.attach(back_button())
    builder.adjust(6, 1)

    return builder.as_markup()

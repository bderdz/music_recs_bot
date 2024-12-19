from aiogram.fsm.state import State, StatesGroup


class PreviewState(StatesGroup):
    tracks_preview = State()

from aiogram.fsm.state import StatesGroup, State


class RecsState(StatesGroup):
    idle = State()
    search_genre = State()
    search_artist = State()
    search_track = State()
    limit = State()
    gen_recs = State()

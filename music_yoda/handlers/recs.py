from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from music_yoda.keyboards.recs import recs_keyboard, search_keyboard, back_button, limit_keyboard
from music_yoda.states import PreviewState, RecsState
from music_yoda.api.spotify import Spotify, SearchType
from music_yoda.utils import find_matches, get_seed_info
from music_yoda.handlers.preview import preview_handler

router: Router = Router()


@router.message(StateFilter(None), Command("recs"))
@router.message(StateFilter(None), F.text.lower().contains("recommendations"))
async def recs_handler(message: Message, state: FSMContext, spotify: Spotify) -> None:
    genres_list = await spotify.get_genres()
    text: str = "<b>recs</b>\n"

    await message.delete()
    recs_message = await message.answer(text=text, reply_markup=recs_keyboard(seed_amount=0))

    await state.set_state(RecsState.idle)
    await state.update_data(
        {
            "message_id": recs_message.message_id,
            "seed_amount": 0,
            "seed_tracks": [],
            "seed_artists": [],
            "seed_genres": [],
            "genres_list": genres_list
        }
    )


async def recs_main_menu(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    seed_amount = data["seed_amount"]
    text: str = "<b>recs</b>\n"

    text += get_seed_info(genres=data["seed_genres"], artists=data["seed_artists"], tracks=data["seed_tracks"])

    await state.set_state(RecsState.idle)
    await message.edit_text(text=text, reply_markup=recs_keyboard(seed_amount=seed_amount))


@router.callback_query(StateFilter(RecsState.idle), F.data.in_(["recs_tracks", "recs_artists", "recs_genres"]))
async def search_handler(callback: CallbackQuery, state: FSMContext) -> None:
    search_type: str = callback.data.split("_")[1]

    if search_type == "tracks":
        await state.set_state(RecsState.search_track)
        await callback.message.edit_text("tracks seed", reply_markup=back_button().as_markup())

    elif search_type == "artists":
        await state.set_state(RecsState.search_artist)
        await callback.message.edit_text("artists seed", reply_markup=back_button().as_markup())

    elif search_type == "genres":
        await state.set_state(RecsState.search_genre)
        await callback.message.edit_text("genres seed", reply_markup=back_button().as_markup())


@router.message(StateFilter(RecsState.search_track, RecsState.search_artist))
async def process_search(message: Message, bot: Bot, state: FSMContext, spotify: Spotify) -> None:
    message_id: int = (await state.get_data())["message_id"]
    state_name: str = (await state.get_state()).split(":")[1]
    search_type = SearchType.TRACK if state_name == "search_track" else SearchType.ARTIST
    search_query: str = message.text
    text: str = ""

    # Response data of the search Spotify API request
    response: list[dict[str, str]] = await spotify.search(query=search_query, search_type=search_type)
    await state.update_data({"search_data": response})  # Saving response data to the state

    for i, item in enumerate(response):
        text += f"<b>{i + 1}. {item["name"]}</b>\n\n"

    await message.delete()  # Removing the user query message
    await bot.edit_message_text(
        message_id=message_id, chat_id=message.chat.id, text=text,
        reply_markup=search_keyboard(n_buttons=len(response))
    )


@router.callback_query(StateFilter(RecsState.search_track), F.data.startswith("search_"))
async def search_track_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    result_id: int = int(callback.data.split("_")[1])
    result = (await state.get_data())["search_data"][result_id]

    seed_tracks: list[dict] = data["seed_tracks"]  # The current list of selected tracks
    seed_tracks.append(result)  # Adding the selected tracks to the current list

    await state.update_data({
        "seed_tracks": seed_tracks,
        "seed_amount": data["seed_amount"] + 1
    })

    await recs_main_menu(message=callback.message, state=state)


@router.callback_query(StateFilter(RecsState.search_artist), F.data.startswith("search_"))
async def search_artist_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    data = await state.get_data()
    result_id: int = int(callback.data.split("_")[1])
    result = data["search_data"][result_id]
    seed_artists: list[dict] = data["seed_artists"]  # The current list of selected artists
    seed_artists.append(result)  # Adding the selected artist to the current list

    await state.update_data({
        "seed_artists": seed_artists,
        "seed_amount": data["seed_amount"] + 1
    })

    await recs_main_menu(message=callback.message, state=state)


@router.message(StateFilter(RecsState.search_genre))
async def process_genre_match(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    genres_list = data["genres_list"]
    message_id: int = data["message_id"]
    result = find_matches(pattern=message.text, word_list=genres_list)
    text: str = ""

    for i, genre in enumerate(result):
        text += f"{i + 1}. {genre}\n"

    await state.update_data({"search_data": result})
    await message.delete()
    await bot.edit_message_text(
        message_id=message_id,
        chat_id=message.chat.id,
        text=text,
        reply_markup=search_keyboard(n_buttons=len(result))
    )


@router.callback_query(StateFilter(RecsState.search_genre), F.data.startswith("search_"))
async def search_genre_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    data = await state.get_data()
    result_id: int = int(callback.data.split("_")[1])
    result = data["search_data"][result_id]
    seed_genres: list[dict] = data["seed_genres"]  # The current list of selected genres
    seed_genres.append(result)  # Adding the selected genre to the current list

    # Updating the state
    await state.update_data({
        "seed_genres": seed_genres,
        "seed_amount": data["seed_amount"] + 1
    })

    await recs_main_menu(message=callback.message, state=state)


@router.callback_query(StateFilter(RecsState.idle), F.data == "recs_limit")
async def limit_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(RecsState.limit)
    await callback.message.edit_text("limit", reply_markup=limit_keyboard())


@router.callback_query(StateFilter(RecsState.limit), F.data.startswith("limit_"))
async def process_limit(callback: CallbackQuery, state: FSMContext, spotify: Spotify) -> None:
    limit: int = int(callback.data.split("_")[1])

    await callback.answer()
    await state.update_data({"limit": limit})
    await process_recs_generation(callback=callback, state=state, spotify=spotify)


async def process_recs_generation(callback: CallbackQuery, state: FSMContext, spotify: Spotify) -> None:
    data = await state.get_data()
    limit: int = data["limit"]
    artists_seed = list(map(lambda item: item["id"], data["seed_artists"]))  # mapping to ids list
    tracks_seed = list(map(lambda item: item["id"], data["seed_tracks"]))  # mapping to ids list
    genres_seed = data["seed_genres"]

    # API Recommendations Request
    tracks = await spotify.get_recs(genres=genres_seed, artists=artists_seed, tracks=tracks_seed, limit=limit)

    # Changing state to PreviewState with data from api response
    await state.clear()
    await state.set_state(PreviewState.tracks_preview)
    await state.update_data({"tracks": tracks})

    # Tracks Preview
    await preview_handler(callback=callback, state=state)


# Back button handler
@router.callback_query(StateFilter(RecsState), F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await recs_main_menu(message=callback.message, state=state)

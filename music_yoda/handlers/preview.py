from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, LinkPreviewOptions, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from music_yoda.keyboards.pagination import Pagination
from music_yoda.keyboards.preview import preview_keyboard
from music_yoda.states import PreviewState

router: Router = Router()
router.callback_query.filter(StateFilter(PreviewState.tracks_preview))


async def preview_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()  # Removing recs message

    tracks: list[dict] = (await state.get_data()).get("tracks")
    message = await callback.message.answer_photo(
        photo=tracks[0].get("photo"),
        caption=f"💿 <b>{tracks[0].get("name")}</b>",
        show_caption_above_media=True,
        reply_markup=preview_keyboard(url=tracks[0].get("url"), page=0, length=len(tracks) - 1))

    await state.update_data({"message_id": message.message_id})


@router.callback_query(Pagination.filter(F.action.in_(["next", "prev"])))
async def process_pagination(query: CallbackQuery, state: FSMContext, callback_data: Pagination) -> None:
    await query.answer()

    tracks: list[dict] = (await state.get_data()).get("tracks")
    page: int = callback_data.page
    length: int = len(tracks) - 1

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=tracks[page].get("photo"),
            caption=f"💿 <b>{tracks[page].get("name")}</b>",
            show_caption_above_media=True,
        ),
        reply_markup=preview_keyboard(url=tracks[page].get("url"), page=page, length=length))


@router.callback_query(Pagination.filter(F.action == "idle"))
async def process_idle(query: CallbackQuery) -> None:
    await query.answer()


@router.callback_query(Pagination.filter(F.action == "summary"))
async def process_close_preview(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await query.message.delete()

    tracks: list[dict] = (await state.get_data()).get("tracks")
    summary_text = "<b>💿 Recommended for You:</b>\n\n"

    for track in tracks:
        summary_text += f'🎧 <b><a href="{track["url"]}">{track["name"]}</a></b>\n\n'

    await query.message.answer(text=summary_text, link_preview_options=LinkPreviewOptions(is_disabled=True))
    await state.clear()

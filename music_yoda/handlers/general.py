from aiogram import Router
from aiogram.filters import StateFilter

router: Router = Router()
router.message.filter(StateFilter(None))

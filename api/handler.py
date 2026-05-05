from aiogram import Router, types
from aiogram.filters import Command
from config import Config

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот работает!")

@router.message()
async def debug_handler(message: types.Message):
    print(f"Received message: {message.text}")  # Проверка получения
    await message.answer("Бот активен! Получено: " + message.text)

Config.dp.include_router(router)

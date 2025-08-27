from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import update_quiz_index, get_user_stats, update_user_score
from quiz_utils import get_question_message

async def start_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def quiz_handler(message: types.Message):
    await update_user_score(message.from_user.id, 0)
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)

async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    stats = await get_user_stats(user_id)
    await message.answer(
        f"Ваша статистика:\n"
        f"Последний результат: {stats['last_score']}/10\n"
        f"Всего попыток: {stats['total_attempts']}\n"
        f"Лучший результат: {stats['best_score']}/10"
    )

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question_message(message, user_id)
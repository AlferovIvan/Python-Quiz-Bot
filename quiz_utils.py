from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from quiz_data import quiz_data
from database import get_quiz_index

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    
    for option in answer_options:
        callback_data = "right_answer" if option == right_answer else f"wrong_answer:{option}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data)
        )
    
    builder.adjust(1)
    return builder.as_markup()

async def get_question_message(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]
    
    correct_index = question_data['correct_option']
    opts = question_data['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    
    await message.answer(f"Вопрос {current_question_index + 1}/{len(quiz_data)}:\n{question_data['question']}", reply_markup=kb)
from aiogram import types
from database import get_quiz_index, update_quiz_index, save_quiz_result, get_user_stats, update_user_score, get_user_score
from quiz_utils import get_question_message
from quiz_data import quiz_data

async def right_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    
    current_score = await get_user_score(user_id)
    await update_user_score(user_id, current_score + 1)
    
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    selected_answer = None
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == "right_answer":
                selected_answer = button.text
                break
    
    if selected_answer:
        await callback.message.answer(f"Вы ответили: {selected_answer}")
    await callback.message.answer("✅ Верно!")
    
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)
    
    if current_question_index < len(quiz_data):
        await get_question_message(callback.message, user_id)
    else:
        await finish_quiz(callback.message, user_id)


async def wrong_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    if ":" in callback.data:
        selected_answer = callback.data.split(":", 1)[1]
    else:
        selected_answer = "unknown answer"
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    selected_answer = button.text
                    break
    
    await callback.message.answer(f"Вы ответили: {selected_answer}")

    correct_option = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]
    await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_option}")
    
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)
    
    if current_question_index < len(quiz_data):
        await get_question_message(callback.message, user_id)
    else:
        await finish_quiz(callback.message, user_id)

async def finish_quiz(message, user_id):
    final_score = await get_user_score(user_id)
    username = message.from_user.first_name
    await save_quiz_result(user_id, username, final_score)
    
    stats = await get_user_stats(user_id)
    await message.answer(
        f"Квиз завершен!\n"
        f"Ваш результат: {final_score}/10\n"
        f"Последний результат: {stats['last_score']}/10\n"
        f"Всего попыток: {stats['total_attempts']}"
    )
    
    await update_user_score(user_id, 0)
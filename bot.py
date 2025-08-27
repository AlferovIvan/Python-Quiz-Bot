from aiogram import types, Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F
from handlers import start_handler, quiz_handler, stats_handler
from callbacks import right_answer, wrong_answer
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.message.register(start_handler, Command("start"))
dp.message.register(quiz_handler, Command("quiz"))
dp.message.register(quiz_handler, F.text == "Начать игру")
dp.message.register(stats_handler, F.text == "Статистика")

dp.callback_query.register(right_answer, F.data == "right_answer")
dp.callback_query.register(wrong_answer, F.data.startswith("wrong_answer:"))

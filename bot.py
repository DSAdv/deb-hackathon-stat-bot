from bot_config import *
from aiogram import executor, types


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    username = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    user_id = message.from_user.id
    is_bot = message.from_user.is_bot

    await message.answer(text="Привіт\n"
                        "Я бот статистики по Dota 2\n"
                        "Допоможу тобі бути в курсі всіх останніх подій в чемпіонатах та слідкувати за улюбленними командами\n")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import types
from aiogram.utils import executor
from config import *
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class User_info(StatesGroup):
    i1 = State()
    i2 = State()


@dp.message_handler(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(text="Привіт\n"
                              "Я бот статистики по Dota 2\n"
                              "Допоможу тобі бути в курсі всіх останніх подій в чемпіонатах та слідкувати за улюбленними командам, обери необхідний пунк з меню\n\n"
                              "Якщо ти ще не заповнив інформацію про себе – /info")


@dp.message_handler(Command('info'), state=None)
async def get_info(message: types.Message):
    await message.answer("Введи, будь ласка, steam url")
    await User_info.i1.set()


@dp.message_handler(state=User_info.i1)
async def get_steam_url(message: types.Message, state: FSMContext):
    steam_url = message.text
    await state.update_data(ans1=steam_url)
    await message.answer("В якій країні ти живеш?")
    await User_info.next()


@dp.message_handler(state=User_info.i2)
async def get_region(message: types.Message, state: FSMContext):
    data = await state.get_data()
    steam_url = data.get("ans1")
    region = message.text
    await state.finish()
    print(steam_url, region)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import aiogram

import config
import database
import nscm

bot = aiogram.Bot(token=config.TELEGRAM_API_KEY)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    await message.reply('теперь отправь мне свои данные в формате:\nФамилия Имя Отчество НомерПаспорта')


@dp.message_handler(commands=['check'])
async def check_results(message: aiogram.types.Message):
    if not database.is_user_registered(message):
        response = 'для регистрации напиши мне в лс'
    else:
        user_data = database.get_user_data(message.from_user.id)
        response = nscm.get_results(user_data)
    await message.reply(response)


@dp.message_handler(regexp=database.REGISTER_DATA_REGEXP)
async def register(message: aiogram.types.Message):
    if message.chat.type != 'private':
        return

    if database.is_user_registered(message):
        response = 'ты уже есть в базе данных'
    else:
        response = database.register_user(message)

    await message.reply(response)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)

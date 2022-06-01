import re

import aiogram

import config
import database
import nscm

bot = aiogram.Bot(token=config.TELEGRAM_API_KEY)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    await message.reply('Для регистрации отправь мне свои данные в формате:\nИванов Иван Иванович 012345')


@dp.message_handler(commands=['check'])
async def check_results(message: aiogram.types.Message):
    if not database.is_user_registered(message.chat.id):
        response = 'Для регистрации напиши мне в личку'
    else:
        user_data = database.get_user_data(message.from_user.id)
        response = nscm.get_results(user_data)
    await message.reply(response)


REGISTER_DATA_REGEXP = re.compile(r'^[А-аЯ-я]{2,20}\s[А-аЯ-я]{2,20}\s[А-аЯ-я]{2,20}\s\d{6}$')


@dp.message_handler(chat_type=aiogram.types.ChatType.PRIVATE, regexp=REGISTER_DATA_REGEXP)
async def register(message: aiogram.types.Message):
    if database.is_user_registered(message.chat.id):
        response = 'Ты уже зарегистрирован(а)'
    else:
        database.register_user(message)
        response = config.SUCCESS_RESPONSE
    await message.reply(response)


@dp.message_handler(commands=['unregister'])
async def unregister(message: aiogram.types.Message):
    if database.is_user_registered(message.chat.id):
        database.unregister_user(message.chat.id)
        response = config.SUCCESS_RESPONSE
    else:
        response = 'Ты итак не зарегистрирован(а)'
    await message.reply(response)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)

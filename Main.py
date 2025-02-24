import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from _keys  import API_TOKEN
import DB_conn, Get_data

import unicodedata


# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = API_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("""
Напиши мне число в формате \"+40\"
                         
Затем я тебе верну всю сумму 
    ^ (с 2:00 до 1:59 следующего дня)
                         
Я также посчитаю тебе сумму за всю неделю!
""")

# Обработчик текстовых сообщений
import re
@dp.message()
async def message_handler(message: types.Message):
    user_name = message.from_user.username
    #print(f"User name type: {type(user_name)}")
    #print(f"User name value: {user_name}")

    # Получение текущей даты
    date_today = await Get_data.check_time_and_get_date()

    pattern = r"^\+\d+$"
    if re.search(pattern, message.text):
        try:
            await DB_conn.Save_info(user_name, date_today, int(message.text[1:]))
            is_saved = True
        except:
            is_saved = False

         # Получение данных из БД о tips сегодня и за
        day_tips, week_tips = await DB_conn.Get_info(user_name, date_today)

        await message.answer(f"""
Добавлено +{message.text[1:]}

Всего за: 
    Сегодня: {day_tips}
    Неделю: {week_tips}
""")
    else:
        await message.answer(f"Zrada, неправильно")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
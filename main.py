from extensions import *
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import token

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command('start', 'help'))
async def cmd_start_help(message: types.Message):
    await message.answer('Чтобы начать работу, введите команду боту в следующем формате: '
                                      '\n<Название изначальной валюты> <Название валюты, в которую надо '
                                      'перевести> <Количество изначальной валюты>\nЧтобы увидеть '
                                      'доступные валюты, введите /values')

@dp.message(Command('values'))
async def handle_message(message: types.Message):
    text = ""
    for currency in currencies.keys():
        text += currency + '\n'
    await message.answer(text)

@dp.message(lambda message: message.text and not message.text.startswith('/'))
async def conver(message: types.Message):
    try:
        values = message.text.lower().split()
        # проверка правильности введенных данных
        if len(values) != 3:
            raise APIException('Нужно ввести 3 параметра')
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        await message.reply(f'Ошибка пользователя\n{e}')
    except Exception as e:
        await message.reply(f'Не удалось обработать команду\n{e}')
    else:
        # выводим конвертированную валюту
        await message.reply(f'Цена {amount} {base} в {quote} = {total_base}')

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
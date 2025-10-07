from extensions import *
import telebot
from config import token, currencies

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help']) # подсказка
def say_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Чтобы начать работу, введите команду боту в следующем формате: '
                                      '\n<Название изначальной валюты> <Название валюты, в которую надо '
                                      'перевести> <Количество изначальной валюты>\nЧтобы увидеть '
                                      'доступные валюты, введите /values')

@bot.message_handler(commands=['values'])
def say_values(message: telebot.types.Message): # отображение всех валют
    text = ""
    for currency in currencies.keys():
        text += currency + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message): # конвертация валют
    try:
        values = message.text.lower().split()
        # проверка правильности введенных данных
        if len(values) != 3:
            raise APIException('Нужно ввести 3 параметра')
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # выводим конвертированную валюту
        bot.reply_to(message, f'Цена {amount} {base} в {quote} = {total_base}')

bot.polling(none_stop=True)
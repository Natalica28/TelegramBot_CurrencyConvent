import telebot
from extensions import APIException, CurConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в следующем формате:\n <Название валюты>' \
           '<В какую валюту переводим>' \
           '<Номинал валюты> \n' \
           'Посмотреть список доступных для перевода валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(m: telebot.types.Message):
    message = m.lover
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Параметров должно быть три.')

        quote, base, amount = values
        total_base = CurConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
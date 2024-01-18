# ## Cri_to2Bot
import telebot

from config_bot import keys, TOKEN
from extensions import ConverctionExcention, CryptoConverteer

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты, цену которой он хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))  # добавляет
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(messange: telebot.types.Message):
    try:
        values = messange.text.split(' ')

        if len(values) != 3:
            raise ConverctionExcention('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverteer.get_price(quote, base, amount)  # получаем total_base
    except ConverctionExcention as e:
        bot.reply_to(messange, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(messange, f'Не удалось обработать комманду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount)}'
        bot.send_message(messange.chat.id, text)


bot.polling()


import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Приветствую!\n \
Для начала работы, вводите команды бота в следующем формате:\n \
<имя валюты, из которой хотите перевести>\n \
<имя валюты, в которую хотите перевести>\n \
<количество переводимой валюты>\n \
Список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Не соответствует количество параметров.")
        quote, base, amount = values
        quote, base, amount = quote.lower(), base.lower(), amount.lower()
        price = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Стоимость {amount} {quote} в {base} - {price}."
        bot.send_message(message.chat.id, text)


bot.polling()

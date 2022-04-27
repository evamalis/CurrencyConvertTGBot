import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "For conversion, input command:\n<original currency>\
<target currency>\
<amount>\n Example: JPY USD 1000\n To see the list of available currencies, use command /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Too many parameters')

        quote, base, amount = values
        final_amount = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'User error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Could not process the request\n{e}')
    else:
        text = f'Price of {amount} {quote} in {base} - {final_amount}'
        bot.send_message(message.chat.id, text)


bot.polling()

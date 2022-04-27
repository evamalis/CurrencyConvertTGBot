import json
import requests
import telebot

TOKEN = '5372149287:AAGkFFa6MI4NOiKH0dtCn5FPZLvtlzC76eA'

bot = telebot.TeleBot(TOKEN)

keys = {'euro': 'EUR', 'dollar': 'USD', 'yen': 'JPY', 'bitcoin': 'BTC'}


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException('Cannot convert into the same currency')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('{quote} is not supported')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('{base} is not supported')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Cannot process this amount')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base


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
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Too many parameters')

    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)
    text = f'Price of {amount} {quote} in {base} - {total_base}'
    bot.send_message(message.chat.id, text)





bot.polling()

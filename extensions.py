import requests
import json
from config import keys


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
            raise ConvertionException(f'{quote} is not supported')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'{base} is not supported')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Cannot process this amount')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        final_amount = round(float(amount)*float(total_base), 2)
        return final_amount
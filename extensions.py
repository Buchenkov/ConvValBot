import json

import requests

from config_bot import keys


class ConverctionExcention(Exception):  # ошибки пользователя
    pass


class CryptoConverteer:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConverctionExcention(f'Невозможно перевести одинаковые валюты "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConverctionExcention(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConverctionExcention(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverctionExcention(f'Не удалось обработать количество {amount}')

        # r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

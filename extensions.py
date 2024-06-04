import requests
import json
from config import keys

class APIException (Exception):
    pass

class CurConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/ca29103c7bc9a7b677e6d2aa/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)['conversion_rate'] * amount

        return total_base


import requests # импортируем бибилиотеки для работы с API и json
import json
from configur import keys #импортируем из файла словарь для работы с классами


class CurrencyException(Exception): # добавляем класс искллючений
    pass

class CurrencyConverter: #добавляем класс исключений и прописываем возможные ошибки со стороны сервера и со стороны неверного ввода пользователя, например при вводе одинаковых валют
    @staticmethod
    def get_price(quote: str, base:str, amount:str):
        if quote == base:
            raise CurrencyException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise CurrencyException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise CurrencyException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except KeyError:
            raise CurrencyException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')#ключ API  с сайта, для конвертации по текущему курсу
        total_base = json.loads(r.content)[keys[base]]

        return total_base*amount # возвращаем общее количество валюты
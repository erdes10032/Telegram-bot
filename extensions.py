import requests
import json
from config import currencies

# исключение - введены неверные данные
class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base = str, quote = str, amount = str):
        # проверка правильности введенных данных
        if base == quote:
            raise APIException(f'Нужно ввести разные валюты, а не только {base}')
        if base not in currencies.keys():
            raise APIException(f'Такая валюта отсутствует - {base}')
        elif quote not in currencies.keys():
            raise APIException(f'Такая валюта отсутствует - {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество валюты введено неверно {amount}')
        # обращаемся к api
        response = requests.get('https://api.exchangeratesapi.io/v1/latest?access_key=5ffbc5b3a69fafdb4e838d215263f1d6&format=1)')
        # получаем курсы всех валют по отношению к евро
        data = json.loads(response.content)['rates']
        # находим нужные валюты и считаем их
        total_base = data[currencies[quote]] / data[currencies[base]] * amount
        return total_base

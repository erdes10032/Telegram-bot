import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('token')

currencies = { # все имеющиеся валюты
    'рубль' : 'RUB',
    'доллар' : 'USD',
    'евро' : 'EUR',
    'тенге' : 'KZT',
    'йена' : 'JPY',
    'юань' : 'CNY',
}
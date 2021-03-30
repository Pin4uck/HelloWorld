# Импортируем библиотеки
import re
import requests
import json


URL = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'


# вывод в виде списка словарей
def load_exchange():
    return json.loads(requests.get(URL).text)


def get_exchange(ccy_key):
    for exc in load_exchange():  # проходимся по словарям списка
        if ccy_key == exc['Cur_Abbreviation']:  # Если есть введенная валюта в одном из словарей, выводим этот словарь
            return exc['Cur_Abbreviation'], exc['Cur_OfficialRate'], exc['Cur_ID']
    return False


def get_exchanges(ccy_pattern):  # здесь пока не понимаю
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'
    for exc in load_exchange():
        if re.match(ccy_pattern, exc['Cur_Abbreviation'], re.IGNORECASE) is not None:
            result.append(exc)
    return result  # выводим курс запрошенной валюты

load_exchange()
get_exchange(input())
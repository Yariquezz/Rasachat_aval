import socket
import hashlib
import hmac
import base64
import logging
import googlemaps

logger = logging.getLogger(__name__)

CHECK_PASS = 'qwerty-12345'
GOOGLE_KEY = 'AIzaSyCHsyTDfvYvpASbU0c5Jl_SsHUNtMU57H0'


def localisator(language: str, kind: str):
    switcher = {
        'uk': {
            'atm': ['name_ua', 'address_ua', 'address_notes_ua'],
            'branch': ['name_ua', 'address_ua', 'work_hours'],
            'not found': 'Не знайдено',
            'hello': 'Доброго дня! Вас вітає Райффайзен Банк Аваль',
            'error': 'Щось пішло не так',
            'sender': 'платник',
            'recipient': 'отримувач',
            'amount': 'сума',
            'date': 'дата',
            'description': 'призначення',
            'currencyCode': 'валюта',
            'comissionRate': 'комісія',
            'link_code': 'скачати квитанцію тут',
        },
        'ru': {
            'atm': ['name_ru', 'address_ru', 'address_notes_ru'],
            'branch': ['name_ru', 'address_ru', 'work_hours'],
            'not found': 'Не найдено',
            'hello': 'Добрый день! Вас приветствует Райффайзен Банк Аваль',
            'error': 'Что-то пошло не так',
            'sender': 'плательщик',
            'recipient': 'получатель',
            'amount': 'сумма',
            'date': 'дата',
            'description': 'назначение',
            'currencyCode': 'валюта',
            'comissionRate': 'комисия',
            'link_code': 'скачать квитанцию тут',
        },
        'en': {
            'atm': ['name_en', 'address_en', 'address_notes_en'],
            'branch': ['name_en', 'address_en', 'work_hours'],
            'not found': 'Not found',
            'hello': 'Welcome to Raiffeisen Bank Aval',
            'error': 'Something went wrong',
            'sender': 'sender',
            'recipient': 'recipient',
            'amount': 'amount',
            'date': 'date',
            'description': 'description',
            'currencyCode': 'currency code',
            'comissionRate': 'comission rate',
            'link_code': 'download here',
        },
    }

    logger.info('language is {}'.format(language))

    resp = switcher.get(language)
    if isinstance(resp, dict):
        resp = resp.get(kind)
    else:
        resp = ''  # default response
    return resp


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception as err:
        logger.exception('Exception occurred {}'.format(err))
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def signature(check, time):
    message = bytes("{}{}".format(check, time), 'utf-8')
    secret = bytes(CHECK_PASS, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
    return sign


def distance_matrix(destinations, origins, language):
    gmaps = googlemaps.Client(GOOGLE_KEY)
    try:
        resp = gmaps.distance_matrix(destinations=destinations, origins=origins, language=language, mode='walking')
    except Exception as err:
        logger.info('Can\'t  connect to Google API via %s' % err)
        dist = ''
    else:
        if resp is not None:
            dist = resp['rows'][0]['elements'][0]['distance']['text']
        else:
            dist = ''

    return dist


if __name__ == "__main__":
    print(distance_matrix((50.234, 40.456), (50.234, 41.456), 'uk'))

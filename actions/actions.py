# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
import socket
import hashlib
import hmac
import base64
from datetime import datetime
import googlemaps
import local_settings

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionBracnhLocator(Action):

    def name(self):
        return "action_atm_locator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):


        ## extract the required slots
        location = tracker.get_slot("location")
        lat = tracker.get_slot("latitude")
        lon = tracker.get_slot("longtitude")

        if lat and lon:
            gmaps = googlemaps.Client(key=local_settings.GOOGLE_KEY)
            text = ''
            origins = (lat, lon)
            your_location = gmaps.reverse_geocode(latlng=(lat, lon), language='uk')
            text += 'Найближчі банкомати до вашої адреси \n {} {} {} \n'.format(
                your_location[0]['address_components'][2]['long_name'],
                your_location[0]['address_components'][1]['short_name'],
                your_location[0]['address_components'][0]['long_name'])
            param = {
                'kind': 'atm',
                'contetn-type': 'json'
            }
            url = 'http://api.finlocator.com/api/syndicate/Rny.json'

            r = requests.get(url=url, params=param)

            if r.status_code == 200:
                response = json.loads(r.text)
                # create empty lists
                branches = []
                branches_loc = []
                l = 0
                branches_result = []
                first = 0
                last = 100

                for i in response['features']:
                    branches.append(
                        {
                            "name": i["name_ua"],
                            "address": i["address_ua"],
                            "location": i["loc"],
                            "is_online": i["is_online"]
                        }
                    )
                    branches_loc.append(
                        {
                            'lat': i["loc"]["lat"],
                            'lng': i["loc"]["lon"]
                        }
                    )

                elements = len(branches_loc) // 100
                for j in range(1, elements):
                    distance = gmaps.distance_matrix(destinations=branches_loc[first:last], origins=origins,
                                                     language='uk',
                                                     mode="walking")
                    for k in distance['rows'][0]['elements']:
                        branches_result.append([k['distance']['value'],
                                                '{} {} {}'.format(k['distance']['text'], branches[l]['name'],
                                                                  branches[l]['address'])])
                        l += 1

                    first += 100
                    last += 100

                distance = gmaps.distance_matrix(destinations=branches_loc[last:len(branches_loc)], origins=origins,
                                                 language='uk', mode="walking")
                for k in distance['rows'][0]['elements']:
                    branches_result.append([k['distance']['value'],
                                            '{} {} {}'.format(k['distance']['text'], branches[l]['name'],
                                                              branches[l]['address'])])
                    l += 1

                branches_result.sort()

                for value in branches_result[:3]:
                    text = text + '{} \n'.format(value[1])
            else:
                text += "не знайдено \n Сервер даних не відповідає"
        else:
            text = 'Адресу вказано не вірно'

        dispatcher.utter_message(text=text)

        return []



class ActionAtmLocator(Action):

    def name(self):
        return "action_branch_locator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):


        ## extract the required slots
        location = tracker.get_slot("location")
        lat = tracker.get_slot("latitude")
        lon = tracker.get_slot("longtitude")

        if lat and lon:
            gmaps = googlemaps.Client(key=local_settings.GOOGLE_KEY)
            text = ''
            origins = (lat, lon)
            your_location = gmaps.reverse_geocode(latlng=(lat, lon), language='uk')
            text += 'Найближчі банкомати до вашої адреси \n {} {} {} \n'.format(
                your_location[0]['address_components'][2]['long_name'],
                your_location[0]['address_components'][1]['short_name'],
                your_location[0]['address_components'][0]['long_name'])
            param = {
                'kind': 'branch',
                'contetn-type': 'json'
            }
            url = 'http://api.finlocator.com/api/syndicate/Rny.json'

            r = requests.get(url=url, params=param)

            if r.status_code == 200:
                response = json.loads(r.text)
                # create empty lists
                branches = []
                branches_loc = []
                l = 0
                branches_result = []
                first = 0
                last = 100

                for i in response['features']:
                    branches.append(
                        {
                            "name": i["name_ua"],
                            "address": i["address_ua"],
                            "location": i["loc"],
                            "is_online": i["is_online"]
                        }
                    )
                    branches_loc.append(
                        {
                            'lat': i["loc"]["lat"],
                            'lng': i["loc"]["lon"]
                        }
                    )

                elements = len(branches_loc) // 100
                for j in range(1, elements):
                    distance = gmaps.distance_matrix(destinations=branches_loc[first:last], origins=origins,
                                                     language='uk',
                                                     mode="walking")
                    for k in distance['rows'][0]['elements']:
                        branches_result.append([k['distance']['value'],
                                                '{} {} {}'.format(k['distance']['text'], branches[l]['name'],
                                                                  branches[l]['address'])])
                        l += 1

                    first += 100
                    last += 100

                distance = gmaps.distance_matrix(destinations=branches_loc[last:len(branches_loc)], origins=origins,
                                                 language='uk', mode="walking")
                for k in distance['rows'][0]['elements']:
                    branches_result.append([k['distance']['value'],
                                            '{} {} {}'.format(k['distance']['text'], branches[l]['name'],
                                                              branches[l]['address'])])
                    l += 1

                branches_result.sort()

                for value in branches_result[:3]:
                    text = text + '{} \n'.format(value[1])
            else:
                text += "не знайдено \n Сервер даних не відповідає"
        else:
            text = 'Адресу вказано не вірно'

        dispatcher.utter_message(text=text)

        return []


class SayHello(Action):

    def name(self):
        return "action_say_hello"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        hello_file = '/Users/yarique/Desktop/hello_file.txt'
        try:
            with open(hello_file, 'r', encoding='UTF-8') as hello:
                text = hello.read()
        except Exception as e:
            print(e)
            text = 'Доброго дня! Вас вітає Райффайзен Банк Аваль'
        finally:
            dispatcher.utter_message(text=text)
        return []


class ActionCheckCurrency(Action):

    def name(self):
        return "action_check_currency"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        now = datetime.now().strftime("%Y%m%d")
        dt = datetime.now().strftime("%d.%m.%Y")

        obj = tracker.get_slot("currency")

        if obj in ("долар", "долари", "доляри"):
            currency = 'USD'
        elif obj in ("євро", "єври", "ойро"):
            currency = 'EUR'
        elif obj in ("рублі", "рублів", "рубль"):
            currency = 'RUB'
        else:
            dispatcher.utter_message(text="Даної валюти не знайдено. Уточніть назву валюти")
            return []

        param = {'date': now, 'contetn-type': 'json'}
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'

        try:
            r = requests.get(url=url, params=param)
        except Exception as e:
            print(e)
            text = "Неможливо під'єднатись до сервера НБУ"
        else:
            if r.status_code == 200 and r.text is not None:
                response = json.loads(r.text)

                for i in response:
                    o = dict(i)
                    if o['cc'] in currency:
                        currency_name = str(o['txt'])
                        currency_name_eng = str(o['cc'])
                        rate = str(round(o['rate'], 2))

                text = "Курс {} на {} складає {} грн.".format(currency_name, dt, rate)
            else:
                text = "Сервер не відповідає"

        dispatcher.utter_message(text=text)

        return [SlotSet("currency", obj)]


class ActionGetCheque(Action):
    def name(self):
        return "action_get_cheque"

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        check = tracker.get_slot("check_num")
        ip = self.get_ip()
        time = str(int(datetime.now().timestamp()))
        password = signature(check=check, time=time)
        text = ""
        params = {}
        url = 'http://localhost:8000/api/check'
        try:
            response = requests.get(url=url, json=params,
                                headers=
                                {
                                    'Content-Type': 'application/json',
                                    'x-time': time,
                                    'x-check-id': check,
                                    'x-real-ip': ip,
                                    'x-hmac': password
                                })
        except Exception as e:
            print(e)
            text = 'Щось пішло не так'
        else:
            if response.status_code == 200:
                resp = json.loads(response.text)
                doc = {
                    "sender": "платник",
                    "recipient": "отримувач",
                    "amount": "сумма",
                    "date": "дата",
                    "description": "призначення",
                    "currencyCode": "валюта",
                    "comissionRate": "комісія",
                    "link_code": "скачати квитанцію тут"
                }
                for i in resp['payments'][0]:
                    text += ("{}{} {}\n".format(doc[i], ":", resp['payments'][0][i]))
            else:
                text = "Чек не знайдено"

        dispatcher.utter_message(text=text)

        return []


def signature(check, time):
    pass_word = 'qwerty-12345'

    message = bytes("{}{}".format(check, time), 'utf-8')
    secret = bytes(pass_word, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
    return sign


def localisator(language):
    switcher = {
        'uk': ["Я", "розмовляю", "українською"],
        'ru': ["Я", "говорю", "по-русски"],
        'en': ["I", "speak", "English" ]

    return switcher.get(language, ["Я", "розмовляю", "українською"])
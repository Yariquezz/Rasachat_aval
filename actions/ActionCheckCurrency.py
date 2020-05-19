# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
from datetime import datetime


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



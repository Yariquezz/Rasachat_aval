from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions.Support import localisator
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCATION = os.path.join(BASE_DIR, 'hello_file.txt')


class ActionSayHello(Action):

    def name(self):
        return "action_say_hello"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        try:
            with open(LOCATION, 'r', encoding='UTF-8') as hello:
                hello = hello.read()
        except Exception as err:
            logger.info('Error here: %s' % err)
            dispatcher.utter_message(text=localisator('uk', 'hello'))
        else:
            dispatcher.utter_message(text=hello)

        return []

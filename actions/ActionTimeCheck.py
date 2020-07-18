from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime, timedelta, time

import logging

logger = logging.getLogger(__name__)

SCHEDULE = [[540, 1080], [540, 1080], [540, 1080], [540, 1080], [540, 1020], None, None]


class ActionSayHello(Action):

    def name(self):
        return "action_time_check"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        now = datetime.now()

        if SCHEDULE[now.weekday()]:
            open_time = datetime.combine(datetime.now(), time.min) + timedelta(minutes=schedule[now.weekday()][0])
            close_time = datetime.combine(datetime.now(), time.min) + timedelta(minutes=schedule[now.weekday()][1])
            response = open_time.time() <= now.time() <= close_time.time()
        else:
            response = False

        if response:
            dispatcher.utter_message(text="З'єдную Вас з оператором")
        else:
            dispatcher.utter_message(text="Нажаль зараз неробочий час операторів. Напишиіть нам пізніше")

        return []
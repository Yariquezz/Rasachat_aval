from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions.API import CheckGovUa_API
from actions.Support import localisator
import logging

logger = logging.getLogger(__name__)


class ActionGetCheque(Action):

    def name(self):
        return "action_get_cheque"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        check = tracker.get_slot("check_num")
        slot = []
        try:
            r = CheckGovUa_API.get_check(check)
            slot = [
                SlotSet("check_num", check)
            ]
        except Exception as err:
            logger.info('Error Finlocator API request: %s' % err)
            text = localisator('uk', 'error')
            dispatcher.utter_message(text=text)
        else:
            text = r
            dispatcher.utter_message(text=text)

        return slot

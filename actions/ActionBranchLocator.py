from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.API import Finlocator_API
from actions.Support import localisator
import logging

logger = logging.getLogger(__name__)


class ActionBranchLocator(Action):

    def name(self):
        return "action_branch_locator"

    # noinspection PyUnreachableCode
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        ## extract the required slots
        location = tracker.get_slot("location")
        lat = tracker.get_slot("latitude")
        lon = tracker.get_slot("longitude")
        text = ''

        if location:
            try:
                f = Finlocator_API.search(kind='branch', address=location, language='uk')
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text=localisator('uk', 'not found')
            else:
                for i in f:
                    text += '%s \n' % i
        elif lat and lon:
            try:
                f = Finlocator_API.search(kind='branch', lat=lat, lon=lon, language='uk')
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text=localisator('uk', 'not found')
            else:
                for i in f:
                    text += '%s \n' % i
        else:
            text = localisator('uk', 'not found')

        dispatcher.utter_message(text=text)

        return []
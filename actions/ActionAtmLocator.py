from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.API import Finlocator_API
from actions.Support import localisator
import logging

logger = logging.getLogger(__name__)


class ActionAtmLocator(Action):

    def name(self):
        return "action_atm_locator"

    # noinspection PyUnreachableCode
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        ## extract the required slot
        location = tracker.get_slot("location")
        lat = tracker.get_slot("latitude")
        lon = tracker.get_slot("longitude")
        text = ''

        if location:
            try:
                f = Finlocator_API.search(kind='atm', address=location, language='uk')
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('ua', 'not found')
                logger.info('Response: %s' % text)
            else:
                for i in f:
                    text += '%s \n' % i
        elif lat and lon:
            try:
                f = Finlocator_API.search(kind='atm', lat=lat, lon=lon, language='uk')
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('ua', 'not found')
                logger.info('Response: %s' % text)
            else:
                for i in f:
                    text += '%s \n' % i
        else:
            text = localisator('ua', 'not found')
            logger.info('Response: %s' % text)

        dispatcher.utter_message(text=text)

        return []

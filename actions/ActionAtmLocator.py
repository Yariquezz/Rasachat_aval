from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

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
        slot = []

        if location:
            try:
                finlocator = Finlocator_API.search(kind='atm', address=location, language='uk')
                slot = [
                    SlotSet("location", location)
                ]
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('ua', 'not found')
                logger.info('Response: %s' % text)
            else:
                for i in finlocator:
                    text = i[0]
                    message = dict(
                        custom=dict(
                            location=dict(
                                lat=i[1]['lat'],
                                lon=i[1]['lon']
                            )
                        )
                    )
                    dispatcher.utter_message(text=text)
                    dispatcher.utter_custom_json(json.dumps(message))
        elif lat and lon:
            try:
                finlocator = Finlocator_API.search(kind='atm', lat=lat, lon=lon, language='uk')
                slot = [
                    SlotSet("latitude", lat),
                    SlotSet("longitude", lon)
                ]
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('ua', 'not found')
                logger.info('Response: %s' % text)
            else:
                for i in finlocator:
                    text = i[0]
                    message = dict(
                        custom=dict(
                            location=dict(
                                lat=i[1]['lat'],
                                lon=i[1]['lon']
                            )
                        )
                    )
                    dispatcher.utter_message(text=text)
                    dispatcher.utter_custom_json(json.dumps(message))
        else:
            text = localisator('ua', 'not found')
            logger.info('Response: %s' % text)

        return slot

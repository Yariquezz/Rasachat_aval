from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions.API import Finlocator_API
from actions.Support import localisator
import logging
import json

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
        slot = []

        if location:
            try:
                finlocator = Finlocator_API.search(kind='branch', address=location, language='uk')
                slot = [
                    SlotSet("location", location)
                ]
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('uk', 'not found')
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
                finlocator = Finlocator_API.search(kind='branch', lat=lat, lon=lon, language='uk')
                slot = [
                    SlotSet("latitude", lat),
                    SlotSet("longitude", lon)
                ]
            except Exception as err:
                logger.info('Error Finlocator API request: %s' % err)
                text = localisator('uk', 'not found')
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
            text = localisator('uk', 'not found')
            logger.info('Response: %s' % text)

        return slot

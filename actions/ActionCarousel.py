from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import logging
import json

logger = logging.getLogger(__name__)


class ActionGetCheque(Action):

    def name(self):
        return "action_carousel"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        slot = []

        message = dict(custom=dict(
        carousel = dict(maxWidth=4, maxHeight=4,
        elements = [
            dict(
                title="Tiger",
                imageButton=dict(imageUrl="https://i.imgur.com/nGF1K8f.jpg",actionType="web_url", actionBody="ImageButton",imageHeight=3),
                descriptionButton = dict(text="Little tiger",actionType="web_url",actionBody="descriptionButton",textHeight=2),
                buttons = [
                    dict(title="Go tiger",payload="/affirm",type="postback",buttonHeight=1),
                    dict(title="No",payload="/deny",type="postback",buttonHeight=1),
        ])])))

        dispatcher.utter_custom_json(json.dumps(message))

        return slot

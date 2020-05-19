import requests
import json
import logging
from datetime import datetime

from actions.Support import get_ip, signature, localisator

CHECK_URL = 'http://localhost:8000/api/check'
TIME = str(int(datetime.now().timestamp()))
IP = get_ip()
HEADERS = {
    'Content-Type': 'application/json',
    'x-time': TIME,
    'x-real-ip': IP,
}

logger = logging.getLogger(__name__)


def get_check(check):

    password = signature(check=check, time=TIME)
    text = ""
    params = HEADERS

    params.update({'x-check-id': check, 'x-hmac': password})

    try:
        response = requests.get(
            url=CHECK_URL,
            headers=params,
        )
    except Exception as err:
        logger.info('Can\'t  connect to Check API via %s' % err)
        text = localisator('ua', 'error')
    else:
        if response.status_code == 200:
            resp = json.loads(response.text)
            for i in resp['payments'][0]:
                text += ("{}{} {}\n".format(localisator('uk', i), ":", resp['payments'][0][i]))
        else:
            text = localisator('ua', 'not found')

    return text
import requests
import json
import logging
import socket
from datetime import datetime

from actions.Support import get_ip, signature, localisator

TIME = str(int(datetime.now().timestamp()))
IP = get_ip()
HEADERS = {
    'Content-Type': 'application/json',
    'x-time': TIME,
    'x-real-ip': IP,
}

logger = logging.getLogger(__name__)


def get_host_ip():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except Exception as err:
        logger.info("Unable to get Hostname and IP because of {} return localhost".format(err))
        return 'localhost'
    else:
        return host_ip


CHECK_URL = 'http://{}:8000/api/check'.format(get_host_ip())


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
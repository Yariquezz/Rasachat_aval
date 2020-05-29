import requests
import json
import logging
from datetime import datetime, timedelta, time

from actions.Support import localisator, distance_matrix

FINLOCATOR_URL = 'http://api.finlocator.com/api/syndicate/Rny.json'
HEADER = {
    'contetn-type': 'json',
    'limit': 5,
}

logger = logging.getLogger(__name__)


def branch_schedule(schedule: list, language: str):
    today = datetime.today().weekday()

    if schedule[today]:
        open_time = datetime.combine(datetime.today(), time.min) + timedelta(minutes=schedule[today][0])
        close_time = datetime.combine(datetime.today(), time.min) + timedelta(minutes=schedule[today][1])

        return '{}{} - {}'.format(localisator(language=language, kind='work_hours'), open_time.strftime('%H:%M'), close_time.strftime('%H:%M'))
    else:
        return localisator(language=language, kind='closed')


def search(**kwargs):
    params = HEADER
    resp = []

    for argument in kwargs:
        params.update({argument: kwargs[argument]})

    if 'language' not in params:
        language = 'uk'
        params.pop('language')
    else:
        language = kwargs['language']

    try:
        r = requests.get(url=FINLOCATOR_URL, params=params)
    except Exception as err:
        logger.info('Can\'t  connect to finlocator API via %s' % err)
    else:
        if r.status_code == 200:
            temp_resp = json.loads(r.text)['features']

            if ('lat' and 'lon' in kwargs) and ('address' not in kwargs):
                origins = (kwargs['lat'], kwargs['lon'])
                # if kind == branch return list with branch schedule
                if kwargs['kind'] == 'branch':
                    for i in temp_resp:
                        if i['is_online']:
                            resp.append("{}\n{}\n{}\n{}".format(
                                i[localisator(language=language, kind=kwargs['kind'])[0]],
                                i[localisator(language=language, kind=kwargs['kind'])[1]],
                                branch_schedule(i[localisator(language=language, kind=kwargs['kind'])[2]], language=language),
                                distance_matrix(destinations=(i['loc']['lat'], i['loc']['lon']), origins=origins,
                                                language=language)
                            ))
                # else return location details
                else:
                    for i in temp_resp:
                        if i['is_online']:
                            resp.append("{}\n{}\n{}\n{}".format(
                                i[localisator(language=language, kind=kwargs['kind'])[0]],
                                i[localisator(language=language, kind=kwargs['kind'])[1]],
                                i[localisator(language=language, kind=kwargs['kind'])[2]],
                                distance_matrix(destinations=(i['loc']['lat'], i['loc']['lon']), origins=origins,
                                                language=language)
                            ))
            else:
                if kwargs['kind'] == 'branch':
                    for i in temp_resp:
                        if i['is_online']:
                            resp.append("{}\n{}\n{}\n".format(
                                i[localisator(language=language, kind=kwargs['kind'])[0]],
                                i[localisator(language=language, kind=kwargs['kind'])[1]],
                                branch_schedule(i[localisator(language=language, kind=kwargs['kind'])[2]], language=language),
                            ))
                        else:
                            for i in temp_resp:
                                if i['is_online']:
                                    resp.append("{}\n{}\n{}\n".format(
                                        i[localisator(language=language, kind=kwargs['kind'])[0]],
                                        i[localisator(language=language, kind=kwargs['kind'])[1]],
                                        i[localisator(language=language, kind=kwargs['kind'])[2]]
                                    ))
        else:
            logger.info('Response: %s' % resp)
            return resp

    logger.info('Response: %s' % resp)
    return resp


if __name__ == "__main__":
    loc = search(kind='atm', lat=50.518687, lon=30.20389, language='ru')
    print(len(loc), loc)
    address = search(kind='branch', address='Irpin', language='ru')
    print(len(address), address[0])

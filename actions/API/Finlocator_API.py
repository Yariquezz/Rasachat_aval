import requests
import json
import logging
from actions.Support import localisator, distance_matrix


FINLOCATOR_URL = 'http://api.finlocator.com/api/syndicate/Rny.json'
HEADER = {
    'contetn-type': 'json',
    'limit': 5,
}

logger = logging.getLogger(__name__)


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
                for i in temp_resp:
                    if i['is_online']:
                        resp.append("{} {} {} {}".format(
                            i[localisator(language=language, kind=kwargs['kind'])[0]],
                            i[localisator(language=language, kind=kwargs['kind'])[1]],
                            i[localisator(language=language, kind=kwargs['kind'])[2]],
                            distance_matrix(destinations=(i['loc']['lat'], i['loc']['lon']), origins=origins, language=language)
                        ))
            else:
                for i in temp_resp:
                    if i['is_online']:
                        resp.append("{} {} {}".format(
                            i[localisator(language=language, kind=kwargs['kind'])[0]],
                            i[localisator(language=language, kind=kwargs['kind'])[1]],
                            i[localisator(language=language, kind=kwargs['kind'])[2]]
                        ))
        else:
            return resp

    return resp


if __name__ == "__main__":
    F = Finlocator()
    loc = F.search(kind='atm', lat=50.518687, lon=30.20389, language='ru')
    print(len(loc), loc)
    address = F.search(kind='branch', address='Oslo', language='ru')
    print(len(address), address)
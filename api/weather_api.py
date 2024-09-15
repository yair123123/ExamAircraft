import json
import requests
from toolz import pipe, first
from toolz.curried import get_in, pluck, partial

API_KEY = "07f2b3140861020136800b993d7fef8b"
def get_from_api(url):
    response = requests.get(url)
    return response.json()

def find_city_location(city:str,url_api:str) -> dict:
    data = get_from_api(f"{url_api}/geo/1.0/direct?q={city}&appid={API_KEY}")
    return pipe(
    data[0],
    lambda x:{key: x[key] for key in ('name', 'lat','lon') if key in x}
    )

def find_weather_by_city(city:str,url_api:str) -> str:
    date_filter = "00:00:00"
    data = get_from_api(f"{url_api}/data/2.5/forecast?q={city}&appid={API_KEY}")
    if data is {}:
        return None
    return pipe(
        data,
        partial(get_in, ['list']),
        partial(lambda x: next(filter(lambda y:date_filter in y['dt_txt'] , x))),
        lambda x: {
            'city': city,
            'weather': get_in(['weather', 0, 'main'], x, default='לא נמצא'),
            'clouds': get_in(['clouds', 'all'], x, default=0),
            'wind': get_in(['wind', 'speed'], x, default='לא נמצא')
        }
    )
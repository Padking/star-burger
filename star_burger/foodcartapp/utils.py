import requests

from django.conf import settings


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")

    return lat, lon


if __name__ == '__main__':
    yandex_http_geocoder_api = settings.YANDEX_HTTP_GEOCODER_API
    address = 'Серпуховская'

    coords = fetch_coordinates(yandex_http_geocoder_api, address)
    message_template = 'Долгота: {1}, Широта: {0}'
    msg = message_template.format(*coords)
    print(msg)

import json

import requests


def translate(text, api_key):
    url = 'https://translation.googleapis.com/language/translate/v2'
    ans = json.loads(
        requests.post(url, json={'q': text, 'source': 'en', 'target': 'ru'},
                      params={'key': api_key}).text)
    return ans['data']['translations'][0]['translatedText']

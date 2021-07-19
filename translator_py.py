# coding: utf-8
import json

import requests


class Translator:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:80/api/v1'
        self.access_token = ''
        self.url = ''

    def login(self, email: str, password: str):
        ans = requests.get(self.base_url + '/login',
                           params={'email': email, 'password': password})
        token = json.loads(ans.content)
        if token:
            self.access_token = token
        return True if self.access_token else False

    def tokens(self, url: str):
        self.url = url
        ans = requests.get(
            self.base_url + '/tokens',
            params={'url': url, 'access_token': self.access_token})
        return json.loads(ans.content)

    def translate(self, known: list, unknown: list,
                  transcriptions: bool = True):
        ans = requests.put(self.base_url + '/translate',
                           params={'url': self.url, 'known': json.dumps(known),
                                   'unknown': json.dumps(unknown),
                                   'transcriptions': transcriptions,
                                   'access_token': self.access_token})
        return ans.content.decode('utf-8')

    def anki(self, filepath):
        ans = requests.get(self.base_url + '/anki',
                           params={'access_token': self.access_token})
        with open(filepath, encoding='utf-8', mode='w') as f:
            f.write(ans.content.decode('utf-8'))

# coding: utf-8
import io
import json

import requests


class Translator:
    def __init__(self):
        # self.base_url = 'http://34.70.243.200/api/v1'
        self.base_url = 'http://127.0.0.1/api/v1'
        self.access_token = ''
        self.url = ''

    def login(self, email: str, password: str):
        ans = requests.get(self.base_url + '/login',
                           params={'email': email, 'password': password})
        token = json.loads(ans.content)
        if token:
            self.access_token = token
        return True if self.access_token else False

    def make_article(self, inner_html: str):
        ans = requests.post(self.base_url + '/make_article',
                            files={'inner_html': io.StringIO(inner_html)})
        url = ans.content.decode('utf-8')
        return url

    def tokens(self, url: str):
        self.url = url
        ans = requests.get(
            self.base_url + '/tokens',
            params={'url': url, 'access_token': self.access_token})
        return json.loads(ans.content)

    def append_known(self, tokens: list):
        requests.put(self.base_url + '/append_known',
                     params={
                         'tokens': json.dumps(tokens),
                         'access_token': self.access_token})

    def append_unknown(self, tokens: list):
        requests.put(self.base_url + '/append_unknown',
                     params={'tokens': json.dumps(tokens),
                             'access_token': self.access_token})

    def translate(self, transcriptions: bool = True,
                  translate_unlabeled: bool = True):
        ans = requests.put(self.base_url + '/translate',
                           params={'url': self.url,
                                   'transcriptions': transcriptions,
                                   'translate_unlabeled': translate_unlabeled,
                                   'access_token': self.access_token})
        return ans.content.decode('utf-8')

    def anki(self, filepath):
        ans = requests.get(self.base_url + '/anki',
                           params={'access_token': self.access_token})
        with open(filepath, encoding='utf-8', mode='w') as f:
            f.write(ans.content.decode('utf-8'))

import json

import requests
import webbrowser



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
        ans = requests.get(self.base_url + '/tokens', params={'url': url,
                                                              'access_token': self.access_token})
        return json.loads(ans.content)

    def translate(self, known: list, unknown: list,
                  transcriptions: bool = True):
        ans = requests.put(self.base_url + '/translate',
                           params={'url': self.url, 'known': json.dumps(known),
                                   'unknown': json.dumps(unknown),
                                   'transcriptions': transcriptions,
                                   'access_token': self.access_token})
        return ans.content


url = 'https://en.wikipedia.org/wiki/Blockchain'
translator = Translator()
logged_in = translator.login('lyalinstas@gmail.com', 'andromeda')

if logged_in:
    known, unknown = [], []

    for word in translator.tokens(url):
        ans = input(f"Do you know word '{word}'?: ").lower()

        if ans == 'stop':
            break
        elif ans == 'y':
            known.append(word)
        elif ans == 'n':
            unknown.append(word)

    page = translator.translate(known, unknown, transcriptions=True)

    with open('test.html', encoding='utf-8', mode='w') as f:
        f.write(page)
        webbrowser.open('test.html')



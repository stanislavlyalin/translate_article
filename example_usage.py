# coding: utf-8
import re
import webbrowser

from bs4 import BeautifulSoup

from translator_py import Translator

if __name__ == '__main__':

    email = input('Enter email: ')
    password = input('Enter password: ')

    translator = Translator()
    logged_in = translator.login(email, password)

    if logged_in:
        known, unknown = [], []
        url = 'https://en.wikipedia.org/wiki/Blockchain'

        for word in translator.tokens(url):
            ans = input(f"Do you know word '{word}'?: ").lower()

            if ans == 'stop':
                break
            elif ans == 'y':
                known.append(word)
            elif ans == 'n':
                unknown.append(word)

        page = translator.translate(known, unknown, transcriptions=True)

        bs_doc = BeautifulSoup(page, 'html.parser')
        valid_filepath = re.sub(r'[^\w\-_. ]', '_', bs_doc.title.string)
        translated_filepath = f'{valid_filepath}.html'

        with open(translated_filepath, encoding='utf-8', mode='w') as f:
            f.write(page)
            webbrowser.open(translated_filepath)

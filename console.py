# coding: utf-8
import webbrowser

from translator_py import Translator


def split(command):
    return [item.strip() for item in command.split(' ')]


if __name__ == '__main__':

    translator = Translator()
    known, unknown = [], []

    while True:
        command = input('> ')

        if command.startswith('login'):
            _, email, password = split(command)
            logged_id = translator.login(email, password)
            if not logged_id:
                print('You are not logged in')

        if command.startswith('tokens'):
            _, url = split(command)
            tokens = translator.tokens(url)
            for token in tokens:
                ans = input(f"> do you know word '{token}'? ")
                if ans.lower() == 'y':
                    known.append(token)
                elif ans.lower() == 'n':
                    unknown.append(token)
                elif ans.lower() == 'stop':
                    break
            translator.append_known(known)
            translator.append_unknown(unknown)

        if command.startswith('translate'):
            _, filepath = split(command)
            with open(filepath, encoding='utf-8', mode='w') as f:
                f.write(translator.translate(transcriptions=True,
                                             translate_unlabeled=False))
            webbrowser.open(filepath)

        if command.startswith('known'):
            _, token = split(command)
            translator.append_known([token])

        if command.startswith('unknown'):
            _, token = split(command)
            translator.append_unknown([token])

        if command.startswith('exit'):
            break

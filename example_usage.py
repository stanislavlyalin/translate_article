# coding: utf-8
import webbrowser

from translator_py import Translator

if __name__ == '__main__':

    email = input('Enter email: ')
    password = input('Enter password: ')

    translator = Translator()

    # log in service
    logged_in = translator.login(email, password)

    if logged_in:
        known, unknown = [], []
        url = 'https://en.wikipedia.org/wiki/Blockchain'

        # get article tokens never seen before
        tokens = translator.tokens(url)

        # mark tokens as known/unknown
        for word in tokens:
            ans = input(f"Do you know word '{word}'?: ").lower()

            if ans == 'stop':
                break
            elif ans == 'y':
                known.append(word)
            elif ans == 'n':
                unknown.append(word)

        # update dictionaries
        translator.append_known(known)
        translator.append_unknown(unknown)

        # translate page
        page = translator.translate(transcriptions=True,
                                    translate_unlabeled=False)

        # save page to disk and open in browser
        translated_filepath = 'page.html'
        with open(translated_filepath, encoding='utf-8', mode='w') as f:
            f.write(page)
            webbrowser.open(translated_filepath)

        # mark learned words as known
        print('Type words what you know')
        while True:
            ans = input('I know word: ')
            if ans == 'stop':
                break
            translator.append_known([ans])

        # get anki file
        translator.anki('anki.txt')

# API v1

## Graphical description

```
Client                                              Server
------                                              ------
  |                                                   |
  |      [G] /login, {email: str, password: str}      |
  |-------------------------------------------------->|  # create access_token as a hash of {email, password, salt}  
  |             200, {access_token: str}              |  # dictionaries has access_token in filename
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |                                                   |
  |    [G] /tokens, {url: str, access_token: str}     |
  |-------------------------------------------------->|  # get list of tokens in given article
  |                  200, {[tokens]}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |      [PUT] /prepare,                              |  # prepare article - insert transcriptions/translations
  |        {url, [known], [unknown],                  |
  |         transcriptions: bool [opt, true],         |
  |         access_token: str}                        |
  |-------------------------------------------------->|
  |                 200, {html: str}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |                                                   |
  |             [G] /anki {access_token: str}         |  # prepare data for Anki
  |-------------------------------------------------->|
  |                 200, {anki file}                  |
  |<--------------------------------------------------|
  |                                                   |

```

## Client library interface

Example usage:

```python

from translator_py import Translator

translator = Translator()
logged_in = translator.login(email, password)

if logged_in:
  known, unknown, passed = [], [], []

  for word in translator.tokens(url):
    ans = input(f"Do you know word '{word}'?: ").lower()

    if ans == 'stop':
        break
    elif ans == 'y':
        known.add(word)
    elif ans == 'n':
        unknown.append(word)
    else:
      passed.append(word)

  page = translator.prepare(known, unknown, passed, transcriptions=True)

  # ... save page and open in browser ...

```

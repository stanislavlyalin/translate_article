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

See [example_usage.py](example_usage.py).

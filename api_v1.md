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
  |-------------------------------------------------->|  # get list of tokens in given article never seen before
  |                  200, {[tokens]}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |                                                   |
  |-----+                                             |
  |     |  # tokens markup (known/unknown/pass)       |
  |<----+                                             |
  |                                                   |
  |                                                   |
  |                                                   |
  |          [PUT] /append_known, {[tokens]}          |
  |-------------------------------------------------->|  # update dictionaries after markup tokens from article
  |         [PUT] /append_unknown, {[tokens]}         |
  |-------------------------------------------------->|
  |                                                   |
  |                                                   |
  |                                                   |
  |                                                   |
  |      [PUT] /translate,                            |  # translate article - insert transcriptions/translations
  |        {url,                                      |  # if word from unknown dict has no context, extract context from article text
  |         transcriptions: bool [opt, true],         |
  |         translate_unlabeled: bool [opt, true]     |
  |         access_token: str}                        |
  |-------------------------------------------------->|
  |                 200, {html: str}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |                                                   |
  |          [PUT] /append_known, {[token]}           |  # append dicts word-by-word while reading
  |          [PUT] /append_unknown, {[token]}         |
  |-------------------------------------------------->|
  |                      ...                          |
  |-------------------------------------------------->|
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

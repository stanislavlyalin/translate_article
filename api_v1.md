# API v1

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
  |              [G] /tokens, {url: str}              |
  |-------------------------------------------------->|  # get list of tokens in given article
  |                  200, {[tokens]}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |      [POST] /prepare,                             |  # prepare article - insert transcriptions/translations
  |        {[known], [unknown], [pass],               |
  |         transcriptions: bool [opt, true],         |
  |         api_key: str}                             |
  |-------------------------------------------------->|
  |                 200, {html: str}                  |
  |<--------------------------------------------------|
  |                                                   |
  |                                                   |
  |                                                   |
  |             [G] /anki {api_key: str}              |  # prepare data for Anki
  |-------------------------------------------------->|
  |                 200, {anki file}                  |
  |<--------------------------------------------------|
  |                                                   |


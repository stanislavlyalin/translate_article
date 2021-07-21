# coding: utf-8
import flask

import views

app = flask.Flask(__name__)
api_v1 = flask.Blueprint('api-v1', __name__)

api_v1.add_url_rule('/login', methods=['GET'],
                    view_func=views.Login.as_view('login'))
api_v1.add_url_rule('/tokens', methods=['GET'],
                    view_func=views.Tokens.as_view('tokens'))
api_v1.add_url_rule('/append_known', methods=['PUT'],
                    view_func=views.AppendKnown.as_view('append_known'))
api_v1.add_url_rule('/append_unknown', methods=['PUT'],
                    view_func=views.AppendUnknown.as_view('append_unknown'))
api_v1.add_url_rule('/translate', methods=['PUT'],
                    view_func=views.Translate.as_view('translate'))
api_v1.add_url_rule('/anki', methods=['GET'],
                    view_func=views.Anki.as_view('anki'))

app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(port=80)

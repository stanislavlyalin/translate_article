# coding: utf-8
import flask

import views

app = flask.Flask(__name__)
api_v1 = flask.Blueprint('api-v1', __name__)

api_v1.add_url_rule('/login', methods=['GET'],
                    view_func=views.Login.as_view('login'))
api_v1.add_url_rule('/tokens', methods=['GET'],
                    view_func=views.Tokens.as_view('tokens'))
api_v1.add_url_rule('/prepare', methods=['PUT'],
                    view_func=views.Prepare.as_view('prepare'))
api_v1.add_url_rule('/anki', methods=['GET'],
                    view_func=views.Anki.as_view('anki'))

app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(port=80)

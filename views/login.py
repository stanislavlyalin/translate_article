import flask.views

from .utils import hash, is_user_registered


class Login(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)
        token = hash(args['email'], args['password'])
        if is_user_registered(token):
            return flask.jsonify(token), 200
        return flask.jsonify(''), 200

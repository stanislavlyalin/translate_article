# coding: utf-8
import flask.views


class Anki(flask.views.MethodView):
    def get(self):
        return flask.jsonify('Not yet implemented', 200)

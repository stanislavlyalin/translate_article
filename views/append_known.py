# coding: utf-8

import json

import flask.views

from utils.dict import known_filepath, unknown_filepath, load_dict, save_dict


class AppendKnown(flask.views.MethodView):
    @staticmethod
    def put():
        args = dict(flask.request.args)
        known = set(json.loads(args['tokens']))
        access_token = args['access_token']

        known_from_file = load_dict(known_filepath(access_token))
        unknown_from_file = load_dict(unknown_filepath(access_token))

        known = known.union(known_from_file)
        unknown_from_file -= known

        save_dict(known, known_filepath(access_token))
        save_dict(unknown_from_file, unknown_filepath(access_token))

        return flask.jsonify({}), 204

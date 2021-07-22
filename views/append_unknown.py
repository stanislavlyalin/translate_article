# coding: utf-8

import json

import flask.views

from utils.dict import load_global, save_global, known_filepath, \
    unknown_filepath, load_dict, save_dict
from utils.translate import process_tokens


class AppendUnknown(flask.views.MethodView):
    @staticmethod
    def put():
        args = dict(flask.request.args)
        unknown = set(json.loads(args['tokens']))
        access_token = args['access_token']

        global_dict = load_global()
        tokens_to_process = set(
            [token for token in unknown if token not in global_dict.keys()])
        save_global({**global_dict, **process_tokens(tokens_to_process)})

        known_from_file = load_dict(known_filepath(access_token))
        unknown_from_file = load_dict(unknown_filepath(access_token))

        unknown = unknown.union(unknown_from_file)
        known_from_file -= unknown

        save_dict(known_from_file, known_filepath(access_token))
        save_dict(unknown, unknown_filepath(access_token))

        return flask.jsonify({}), 204

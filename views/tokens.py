# coding: utf-8
import flask.views

from utils.dict import known_filepath, unknown_filepath, load_dict
from utils.readable_article import ReadableArticle


class Tokens(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)
        url = args['url']
        access_token = args['access_token']

        article = ReadableArticle(url)

        known = load_dict(known_filepath(access_token))
        unknown = load_dict(unknown_filepath(access_token))

        def has_numbers(s: str) -> bool:
            return any(char.isdigit() for char in s)

        unseen_tokens = [token for token in article.tokens() if
                         token not in known and
                         token not in unknown and
                         not token.isdigit() and
                         not has_numbers(token) and
                         not token.endswith("'s") and
                         len(token) > 1]

        return flask.jsonify(unseen_tokens), 200

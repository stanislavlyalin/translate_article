# coding: utf-8
import flask.views

from utils.dict import load_known_dict, load_unknown_dict
from utils.readable_article import ReadableArticle


class Tokens(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)
        url = args['url']
        access_token = args['access_token']

        article = ReadableArticle(url)
        tokens = article.tokens()

        known = load_known_dict(f'{access_token}_known.txt')
        unknown = load_unknown_dict(f'{access_token}_unknown.txt')

        unseen_tokens = []

        for word in tokens:
            # known words, digits and one-letter words are passed
            if word in known or word.isdigit() or len(word) == 1:
                continue

            # unknown words from dict are passed to increase processing speed
            if word in unknown.keys():
                continue

            unseen_tokens.append(word)

        return flask.jsonify(unseen_tokens), 200

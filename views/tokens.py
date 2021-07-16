import flask.views
import nltk

from .readable_article import ReadableArticle
from .utils import load_known_dict, load_unknown_dict


class Tokens(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)

        # TODO: полей url и access_token может не быть

        url = args['url']
        access_token = args['access_token']

        # TODO: может не быть подключения к интернету или URL неправильный.
        #  В этом случае вовзращать пустой список
        article = ReadableArticle(url)

        # select unique tokens by regex only in text nodes
        tokens = []
        for text in article.text_nodes():
            for token in nltk.regexp_tokenize(text.lower(), r"[-\w']+"):
                if token not in tokens:
                    tokens.append(token)

        known_filepath = f'{access_token}_known.txt'
        unknown_filepath = f'{access_token}_unknown.txt'
        known = load_known_dict(known_filepath)
        unknown = load_unknown_dict(unknown_filepath)

        unseen_tokens = []

        for i, word in enumerate(tokens):
            # known words, digits and one-letter words are passed
            if word in known or word.isdigit() or len(word) == 1:
                continue

            # unknown words from dict are passed to increase processing speed
            if word in unknown:
                continue

            unseen_tokens.append(word)

        return flask.jsonify(unseen_tokens), 200

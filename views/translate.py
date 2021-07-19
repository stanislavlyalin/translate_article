import json
import re

import eng_to_ipa as ipa
import flask.views

from .readable_article import ReadableArticle
from .utils import translate, save_known_dict, save_unknown_dict, get_context, \
    load_known_dict, load_unknown_dict


class Translate(flask.views.MethodView):
    @staticmethod
    def put():
        args = dict(flask.request.args)
        url = args['url']
        known = json.loads(args['known'])
        to_translate = json.loads(args['unknown'])
        access_token = args['access_token']

        article = ReadableArticle(url)
        article_text = article.text()
        tokens = article.tokens()

        api_key = 'AIzaSyAyqWeQA9dkBZ39JWaXSGIpBrea7f_9WIY'

        context = {}
        # translation = [translate(word, api_key) for word in to_translate]
        translation = []
        for word in to_translate:
            translation.append(translate(word, api_key))
            context[word] = get_context(word, article_text)

        translation_pairs = []
        for en, ru in zip(to_translate, translation):
            translation_pairs.append((en, ru))

        known_filepath = f'{access_token}_known.txt'
        unknown_filepath = f'{access_token}_unknown.txt'

        known_from_file = load_known_dict(known_filepath)
        unknown_from_file = load_unknown_dict(unknown_filepath)

        known = set(known).union(known_from_file)

        save_known_dict(known, known_filepath)
        unknown = {word: (translation, context[word] if word in context else '')
                   for word, translation in translation_pairs}

        unknown = {**unknown, **unknown_from_file}
        save_unknown_dict(unknown, unknown_filepath)

        # translation_pairs = list(filter(lambda word, translation_context: word in tokens, unknown.items()))

        translation_pairs = [(word, translation_context[0]) for
                             word, translation_context in unknown.items()]
        translation_pairs = list(
            filter(lambda item: item[0] in tokens, translation_pairs))

        # replace unknown words to words + translations
        span_begin, span_end = 'SPAN_BEGIN', 'SPAN_END'
        for en, ru in translation_pairs:
            # negative lookup for replace whole words only
            r = re.compile(rf'(?<!\w)({en})(?!\w)', re.IGNORECASE)
            # \1 to keep original case
            for text in article.text_nodes():
                if en in text.lower():
                    text_to_replace = r.sub(
                        rf'\1 {span_begin}/{ipa.convert(en)}, {ru}/{span_end}',
                        text)
                    text.replace_with(text_to_replace)

        common_style = '''<style type="text/css">
                    img {
                      max-width: 100%;
                      height: auto;
                    }
                    span.translation {
                      color: #eee;
                    }
                </style>
                '''
        style_attr = 'style="font-family: verdana; font-size: 10pt; ' \
                     'line-height: 150%; text-align: justify; padding: 30px;"'
        link_to_original = f'<a href="{url}">' \
                           f'Link to original page</a><br><br>'
        node_content = article.body_html(). \
            replace(span_begin, '<span class="translation">'). \
            replace(span_end, '</span>')

        content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                <title>{article.title()}</title>
                <meta charset="utf-8"/>
                {common_style}
                </head>
                <body {style_attr}>
                {link_to_original}
                {node_content}
                </body>
                </html>
                '''

        return content, 200

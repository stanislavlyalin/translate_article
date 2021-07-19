# coding: utf-8
import json
import re

import eng_to_ipa as ipa
import flask.views

from utils.dict import load_known_dict, load_unknown_dict, save_known_dict, \
    save_unknown_dict
from utils.readable_article import ReadableArticle
from utils.translate import load_api_key, translate, get_context

span_begin, span_end = 'SPAN_BEGIN', 'SPAN_END'


class Translate(flask.views.MethodView):
    @staticmethod
    def put():
        # parse params
        args = dict(flask.request.args)
        url = args['url']
        known = json.loads(args['known'])
        unknown = json.loads(args['unknown'])
        transcriptions = args['transcriptions']
        access_token = args['access_token']

        # update known dict
        Translate.__update_known_dict(known, access_token)

        article = ReadableArticle(url)
        article_text = article.text()
        tokens = article.tokens()

        # make translation
        api_key = load_api_key('api.key')
        unknown_translated = {}
        for word in unknown:
            translated = translate(word, api_key)
            transcription = ipa.convert(word)
            context = get_context(word, article_text)
            unknown_translated[word] = (translated, transcription, context)

        # update unknown dict
        unknown = Translate.__update_unknown_dict(unknown_translated,
                                                  access_token)

        # replace unknown words to words + translations
        Translate.__apply_translation(unknown, tokens, article, transcriptions)

        return Translate.__make_html(article, url), 200

    @staticmethod
    def __update_known_dict(known, access_token):
        known_filepath = f'{access_token}_known.txt'
        known_from_file = load_known_dict(known_filepath)
        known = set(known).union(known_from_file)
        save_known_dict(known, known_filepath)
        return known

    @staticmethod
    def __update_unknown_dict(unknown_translated, access_token):
        unknown_filepath = f'{access_token}_unknown.txt'
        unknown_from_file = load_unknown_dict(unknown_filepath)
        unknown = {**unknown_translated, **unknown_from_file}
        save_unknown_dict(unknown, unknown_filepath)
        return unknown

    @staticmethod
    def __apply_translation(unknown, tokens, article, transcriptions):
        for word, value in unknown.items():
            if word in tokens:
                en = word
                ru, transcription, context = value

                # negative lookup for replace whole words only
                r = re.compile(rf'(?<!\w)({en})(?!\w)', re.IGNORECASE)
                # \1 to keep original case
                for text in article.text_nodes():
                    if en in text.lower():
                        with_transcription = \
                            rf'\1 {span_begin}/{transcription}, {ru}/{span_end}'
                        only_translation = rf'\1 {span_begin}/{ru}/{span_end}'

                        replace_pattern = with_transcription if transcriptions \
                            else only_translation

                        text_to_replace = r.sub(replace_pattern, text)
                        text.replace_with(text_to_replace)

    @staticmethod
    def __make_html(article, url):
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
        return content

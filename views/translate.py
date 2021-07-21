# coding: utf-8
import re

import flask.views

from utils.dict import load_dict, known_filepath, unknown_filepath, load_global
from utils.readable_article import ReadableArticle
from utils.translate import process_tokens

span_begin, span_end = 'SPAN_BEGIN', 'SPAN_END'


class Translate(flask.views.MethodView):
    @staticmethod
    def put():
        args = dict(flask.request.args)
        url = args['url']
        transcriptions = args['transcriptions'] == 'True'
        translate_unlabeled = args['translate_unlabeled'] == 'True'
        access_token = args['access_token']

        article = ReadableArticle(url)
        tokens = set(article.tokens())

        known_from_file = load_dict(known_filepath(access_token))
        unknown_from_file = load_dict(unknown_filepath(access_token))
        global_dict = load_global()

        # make translation
        if translate_unlabeled:
            unknown = tokens - known_from_file
            unknown_from_global = {token: global_dict[token] for token in
                                   unknown if token in global_dict.keys()}
            unknown_from_process = process_tokens(
                unknown - set(unknown_from_global.keys()))
            to_translate = {**unknown_from_global, **unknown_from_process}
        else:
            to_translate = {token: global_dict[token] for token in
                            unknown_from_file if
                            token in global_dict.keys() and token in tokens}

        # replace unknown words to words + translations
        Translate.__apply_translation(to_translate, article, transcriptions)

        return Translate.__make_html(article, url), 200

    @staticmethod
    def __apply_translation(to_translate, article, transcriptions):
        for en, value in to_translate.items():
            ru, transcription = value['translation'], value['transcription']

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
        link_to_original = f'<a href="{url}">' \
                           f'Link to original page</a><br><br>'
        node_content = article.body_html(). \
            replace(span_begin, '<span class="translation">'). \
            replace(span_end, '</span>')

        article.head().append(common_style)
        article.body().clear()
        article.body().append(link_to_original)
        article.body().append(node_content)

        return article.whole_html()

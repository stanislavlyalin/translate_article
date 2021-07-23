# coding: utf-8
import hashlib
from pathlib import Path

import flask.views

from utils.readable_article import custom_style


class MakeArticle(flask.views.MethodView):
    @staticmethod
    def post():
        args = dict(flask.request.args)
        inner_html_file = flask.request.files['inner_html']
        inner_html = inner_html_file.read().decode('utf-8')
        inner_html = inner_html.replace('\n', '<br/>')

        static_dir = 'static'
        Path(static_dir).mkdir(parents=True, exist_ok=True)

        filename = f'{static_dir}/{hashlib.md5(inner_html.encode("utf-8")).hexdigest()}.html'

        with open(filename, encoding='utf-8', mode='w') as page:
            page.write(f'''
            <!doctype html>
            <html>
                <head>
                    {custom_style()}
                </head>
                <body>
                    {inner_html}
                </body>
            </html>
            ''')

        url = f'{flask.request.url_root}{filename}'

        return url, 200

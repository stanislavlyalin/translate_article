# coding: utf-8
import flask.views

import hashlib
from pathlib import Path


class MakeArticle(flask.views.MethodView):
    @staticmethod
    def post():
        args = dict(flask.request.args)
        inner_html = args['inner_html']

        static_dir = 'static'
        Path(static_dir).mkdir(parents=True, exist_ok=True)

        filename = f'{static_dir}/{hashlib.md5(inner_html.encode("utf-8")).hexdigest()}.html'

        with open(filename, encoding='utf-8', mode='w') as page:
            style = '''
            <style type="text/css">
                body {
                    font-family: verdana;
                    font-size: 10pt;
                    line-height: 150%;
                    text-align: justify;
                    padding: 30px;
                }   
                img {
                    max-width: 100%;
                    height: auto;
                }
            </style>
            '''

            page.write(f'''
            <!doctype html>
            <html>
                <head>
                    {style}
                </head>
                <body>
                    {inner_html}
                </body>
            </html>
            ''')

        url = f'{flask.request.url_root}{filename}'

        return url, 200

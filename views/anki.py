# coding: utf-8
import io
import re

import flask.views


class Anki(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)
        access_token = args['access_token']

        unknown_filepath = f'{access_token}_unknown.txt'
        with open(unknown_filepath, encoding='utf-8') as f:
            content = f.readlines()

        proxy = io.StringIO()

        for line in content:
            word, translation, transcription, context = line.split(';')

            r = re.compile(rf'(?<!\w)({word})(?!\w)', re.IGNORECASE)
            context = r.sub(rf'<b>\1</b>', context.strip())

            proxy.write(
                f'<b>{word}</b><br>({transcription})<br><br>{context};{translation}\n')

        mem = io.BytesIO()
        mem.write(proxy.getvalue().encode())
        mem.seek(0)
        proxy.close()

        return flask.send_file(mem, as_attachment=True,
                               attachment_filename='anki.txt',
                               mimetype='text/csv')

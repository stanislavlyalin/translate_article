# coding: utf-8
import io
import re

import flask.views

from utils.dict import unknown_filepath, load_dict, load_global


class Anki(flask.views.MethodView):
    @staticmethod
    def get():
        args = dict(flask.request.args)
        access_token = args['access_token']

        unknown_from_file = load_dict(unknown_filepath(access_token))
        global_dict = load_global()
        to_anki = {token: global_dict[token] for token in unknown_from_file if
                   token in global_dict.keys()}

        proxy = io.StringIO()

        for word, value in to_anki.items():
            translation, transcription, context = value['translation'], value[
                'transcription'], 'empty context'

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

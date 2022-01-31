# coding: utf-8

import pyperclip
import spacy
from utils.tense import tense, tense_schema
from utils.translate import load_api_key, translate

if __name__ == '__main__':

    # tenses cheatsheet
    # https://online-teacher.ru/image/english/zoom/vremena-angliyskogo-yazika-tablitsah.jpg

    input('Press any key to get text from clipboard')
    text = pyperclip.paste()

    mode = int(input('Mode (1: en-ru, 2: ru-en): '))

    tenses_to_train = input('What tenses you want to train? (lower case separated by commas or all): ').split(',')

    nlp = spacy.load('en_core_web_sm')
    api_key = load_api_key()

    sentences = [str(sent).strip() for sent in list(nlp(text).sents)]
    tense_sents = list(filter(lambda sent: tense(sent) != 'not defined', sentences))

    if 'all' not in tenses_to_train:
        tense_sents = list(filter(lambda sent: tense(sent) in tenses_to_train, tense_sents))

    sents_count = len(tense_sents)

    for i, sent in enumerate(tense_sents):
        sent_tense = tense(sent)
        schema = tense_schema(sent_tense)
        translation = translate(sent, api_key)

        if mode == 1:
            input('%d of %d. %s' % (i + 1, sents_count, sent))
            print('  %s %s\n  %s\n' % (schema, sent_tense, translation))
        elif mode == 2:
            input('%d of %d. %s' % (i + 1, sents_count, translation))
            print('  %s %s\n  %s\n' % (schema, sent_tense, sent))

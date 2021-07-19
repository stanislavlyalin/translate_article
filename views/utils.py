import hashlib
import json
import re
from pathlib import Path

import eng_to_ipa as ipa
import requests

hashes_filepath = 'user_hashes.txt'


def hash(email, password):
    salt = 'my_awesome_service'
    return hashlib.md5(f'{email}{password}{salt}'.encode('utf-8')).hexdigest()


def is_user_registered(token):
    if Path(hashes_filepath).is_file():
        with open(hashes_filepath, encoding='utf-8') as f:
            hashes = [line.strip() for line in f.readlines()]
            return token in hashes
    return False


def load_known_dict(file_path: str):
    """
    :param file_path: path to the dict file
    :return: set of words from dict
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.readlines()
            return set([x.strip() for x in content])
    except:
        return set()


def load_unknown_dict(file_path: str):
    """
    :param file_path: path to the dict file
    :return: dict of words-translations
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.readlines()

        unknown = {}
        for x in content:
            word, translation, transcription, context = x.strip().split(';')
            unknown[word] = (translation, context)
        return unknown
    except:
        return {}


def save_known_dict(known: set, file_path: str):
    """
    :param known: set of words to save
    :param file_path: path to the dict file
    """
    try:
        with open(file_path, encoding='utf-8', mode='w') as f:
            for word in sorted(known):
                f.write(f'{word}\n')
    except:
        pass


def save_unknown_dict(unknown: dict, file_path: str):
    """
    :param unknown: dict of unknown words (key) with translations (value)
    :param file_path: path to the dict file
    """
    try:
        with open(file_path, encoding='utf-8', mode='w') as f:
            for word in sorted(unknown):
                translation, context = unknown[word]
                f.write(f'{word};{translation};{ipa.convert(word)};{context}\n')
    except:
        pass


def translate(text, api_key):
    url = 'https://translation.googleapis.com/language/translate/v2'
    ans = json.loads(
        requests.post(url, json={'q': text, 'source': 'en', 'target': 'ru'},
                      params={'key': api_key}).text)
    return ans['data']['translations'][0]['translatedText']


def get_context(word: str, text: str):
    """
    Get word context (sentence) in the given text
    :param word: word
    :param text: text from which context will be extracted
    :return: context (sentence) or empty string
    """
    # [?!\.]? - punctuation or none if begin of sentence
    # [A-Za-z,:\- ]* - letter any case, comma, colons, dashes, spaces 0 or more
    # {word} - desired word for context extraction
    # [A-Za-z,:\- ]* - letter any case, comma, colons, dashes, spaces 0 or more
    # [?!\.]? - punctuation or none if end of sentence
    r = re.compile(rf'[?!.]?([A-Za-z,:\- ]*{word}[A-Za-z,:\- ]*[?!.]?)',
                   re.IGNORECASE)
    m = re.search(r, text)
    return m[1].strip() if m else ''

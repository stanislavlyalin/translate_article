# coding: utf-8
import json
import re

import requests


def load_api_key(filepath):
    """
    Loads Google Translate API key from given filepath
    :param filepath: path to file with API key
    :return: API key as str
    """
    with open(filepath, encoding='utf-8') as f:
        return f.readline().strip()


def translate(text, api_key):
    """
    Performs text translation from en to ru with given API key
    :param text: text to translate
    :param api_key: Google Translate API key
    :return: translated text
    """
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

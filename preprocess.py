import re
import webbrowser

import eng_to_ipa as ipa
import nltk
from bs4 import BeautifulSoup
from newspaper import Article
from readability import Document
from tqdm import tqdm

from translate import translate


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
            unknown[word] = translation
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


def text_nodes(root_node):
    """
    Recursive iterate over text nodes
    """
    for node in root_node.findChildren(text=True, recursive=True):
        yield node


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


if __name__ == '__main__':

    url = input('Enter page URL: ').strip()
    article = Article(url)
    article.download()
    doc = Document(article.html)
    article_text = article.text
    title = doc.title()

    node = BeautifulSoup(doc.get_clean_html(), 'html.parser').find('body')

    # select unique tokens by regex only in text nodes
    tokens = []
    for text in text_nodes(node):
        for token in nltk.regexp_tokenize(text.lower(), r"[-\w']+"):
            if token not in tokens:
                tokens.append(token)

    token_len = len(tokens)

    known_filepath = 'known.txt'
    unknown_filepath = 'unknown.txt'
    known = load_known_dict(known_filepath)
    unknown = load_unknown_dict(unknown_filepath)

    to_translate = []  # list of words to translate
    translation_pairs = [(word, translation) for word, translation in
                         unknown.items()]
    context = {}

    for i, word in enumerate(tokens):
        # known words, digits and one-letter words are passed
        if word in known or word.isdigit() or len(word) == 1:
            continue

        # unknown words from dict are passed to increase processing speed
        if word in unknown:
            continue

        percent = '%2d' % (100 * (i + 1) // token_len)
        ans = input(f"({percent}%) Do you know word '{word}'?: ").lower()

        if ans == 'stop':
            break
        elif ans == 'y':
            known.add(word)
        elif ans == 'n':
            to_translate.append(word)
            context[word] = get_context(word, article_text)

    # print list of words to translate
    print('Words to translate:')
    print(';'.join(to_translate))

    api_key = input('Enter API key: ')
    translation = [translate(word, api_key) for word in to_translate]

    for en, ru in zip(to_translate, translation):
        translation_pairs.append((en, ru))

    save_known_dict(known, known_filepath)
    unknown = {word: (translation, context[word]) for word, translation in
               translation_pairs}
    save_unknown_dict(unknown, unknown_filepath)

    # keep only words presented in current document
    translation_pairs = list(
        filter(lambda item: item[0] in tokens, translation_pairs))

    # replace unknown words to words + translations
    span_begin, span_end = 'SPAN_BEGIN', 'SPAN_END'
    for en, ru in tqdm(translation_pairs):
        # negative lookup for replace whole words only
        r = re.compile(rf'(?<!\w)({en})(?!\w)', re.IGNORECASE)
        # \1 to keep original case
        for text in text_nodes(node):
            if en in text.lower():
                text_to_replace = r.sub(
                    rf'\1 {span_begin}/{ipa.convert(en)}, {ru}/{span_end}',
                    text)
                text.replace_with(text_to_replace)

    # save prepared page near the original
    translated_file_path = f'{title}.html'
    with open(translated_file_path, encoding='utf-8', mode='w') as f:
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
        node_content = node.decode_contents(). \
            replace(span_begin, '<span class="translation">'). \
            replace(span_end, '</span>')

        content = f'''
            <!DOCTYPE html>
            <html>
            <head>
            <title>{title}</title>
            <meta charset="utf-8"/>
            {common_style}
            </head>
            <body {style_attr}>
            {link_to_original}
            {node_content}
            </body>
            </html>
            '''
        f.write(content)
    print(f'Processed page successfully save on {translated_file_path}')
    webbrowser.open(translated_file_path)

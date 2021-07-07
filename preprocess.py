import nltk
import os
import re
import webbrowser
from bs4 import BeautifulSoup


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


def save_known_dict(known: set, file_path: str):
    """
    :param known: set of words to save
    :param file_path: path to the dict file
    """
    try:
        with open(file_path, encoding='utf-8', mode='w') as f:
            for word in known:
                f.write(f'{word}\n')
    except:
        pass


if __name__ == '__main__':

    file_path = input('Enter file path: ')
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    doc = BeautifulSoup(content, 'html.parser')

    selector = input('Enter CSS selector for page main content: ')

    nodes = doc.select(selector)
    if not nodes:
        print('Node not found in document. Exit')

    node = nodes[0]
    node_text = str(node.text.lower())
    node_inner_html = node.decode_contents()

    # select unique tokens by regex
    tokens = []
    for token in nltk.regexp_tokenize(node_text, r'[\w-]+'):
        if token not in tokens:
            tokens.append(token)
    token_len = len(tokens)

    known_filepath = 'known.txt'
    known = load_known_dict(known_filepath)
    to_translate = []  # list of words to translate

    for i, word in enumerate(tokens):
        # known words, digits and one-letter words are passed
        if word in known or word.isdigit() or len(word) == 1:
            continue

        percent = '%2d' % (100 * (i+1) // token_len)
        ans = input(f"({percent}%) Do you know word '{word}'?: ").lower()

        if ans == 'stop':
            break
        elif ans == 'y':
            known.add(word)
        else:
            to_translate.append(word)

    save_known_dict(known, known_filepath)

    # print list of words to translate
    print('Words to translate:')
    print(';'.join(to_translate))

    # launch web-browser with Google Translate page
    url = 'https://translate.google.com/'
    params = f'?hl=ru&sl=en&tl=ru&text={"%3B".join(to_translate)}&op=translate'
    webbrowser.open(url + params)

    translation = [token.strip() for token in
                   input('Enter translated words: ').split(';')]
    translation_pairs = [(en, ru) for en, ru in zip(to_translate, translation)]

    # replace unknown words to words + translations
    for en, ru in translation_pairs:
        # negative lookup for replace whole words only
        r = re.compile(rf'(?<!\w)({en})(?!\w)', re.IGNORECASE)
        # \1 to keep original case
        node_inner_html = r.sub(rf'\1 /{ru}/', node_inner_html)

    # save prepared page near the original
    translated_file_path = f'{os.path.splitext(file_path)[0]}_translated.html'
    with open(translated_file_path, encoding='utf-8', mode='w') as f:
        style_attr = 'style="font-family: verdana; font-size: 10pt"'
        content = f'''
            <!DOCTYPE html>
            <html>
            <head>
            <title>{doc.title}</title>
            </head>
            <body {style_attr}>{node_inner_html}</body>
            </html>
            '''
        f.write(content)

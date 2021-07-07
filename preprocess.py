from collections import defaultdict

import nltk
import os
import re
import webbrowser
from bs4 import BeautifulSoup

if __name__ == '__main__':
    file_path = input('Enter file path: ')

    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    doc = BeautifulSoup(content, 'html.parser')

    selector = input('Enter CSS selector for page main content: ')
    node = doc.select(selector)[0]
    node_text = str(node.text.lower())
    node_inner_html = node.decode_contents()

    # выбор токенов по регулярному выражению
    all_tokens = nltk.regexp_tokenize(node_text, r'[\w-]+')
    tokens = []

    # такое решение гарантирует, что порядок токенов будет сохранён
    for token in all_tokens:
        if token not in tokens:
            tokens.append(token)
    token_len = len(tokens)

    # загрузка словаря извесных слов
    known = set()
    known_filepath = 'known.dict'
    try:
        with open(known_filepath, encoding='utf-8') as f:
            content = f.readlines()
            known = set([x.strip() for x in content])
    except:
        pass

    to_translate = []

    for i, token in enumerate(tokens):
        word = token

        # известные слова пропускаем
        if word in known or word.isdigit() or len(word) == 1:
            continue

        ans = input(f"({'%2d' % (100 * (i+1) // token_len)}%) Do you know word '{word}'?: ").lower()

        if ans == 'stop':
            break
        elif ans == 'y':
            known.add(word)
        else:
            to_translate.append(word)

    # сохранение словаря известных слов
    try:
        with open(known_filepath, encoding='utf-8', mode='w') as f:
            for word in known:
                f.write(f'{word}\n')
    except:
        pass

    # вывод списка слов для перевода
    print('Words to translate:')
    print(';'.join(to_translate))

    # запуск браузера со словами для перевода
    url = f'https://translate.google.com/?hl=ru&sl=en&tl=ru&text={"%3B".join(to_translate)}&op=translate'
    webbrowser.open(url)

    translation = input('Enter translated words: ')

    translation_pairs = []

    for en, ru in zip(to_translate, [token.strip() for token in translation.split(';')]):
        translation_pairs.append((en, ru))

    # для всех пар выполнить замену текста html-кода
    for en, ru in translation_pairs:
        r = re.compile(rf'(?<!\w)({en})(?!\w)', re.IGNORECASE)
        node_inner_html = r.sub(rf'\1 /{ru}/', node_inner_html)

    translated_file_path = f'{os.path.splitext(file_path)[0]}_translated.html'
    with open(translated_file_path, encoding='utf-8', mode='w') as f:
        f.write(f'<!DOCTYPE html><html><head></head><body style="font-family: verdana; font-size: 10pt">{node_inner_html}</body></html>')

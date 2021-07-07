from collections import defaultdict

import json
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
    tokens = nltk.regexp_tokenize(node_text, r'[\w-]+')
    total_tokens = len(tokens)

    # упорядочивание токенов по убыванию частоты встречаемости
    token_count = defaultdict(lambda: 0)
    for token in tokens:
        token_count[token] += 1
    token_count = sorted(
        [(token, count) for token, count in token_count.items()],
        key=lambda x: x[1])[::-1]
    token_len = len(token_count)

    # загрузка словаря извесных слов
    known = []
    known_filepath = 'known.dict'
    try:
        with open(known_filepath, encoding='utf-8') as f:
            known = json.load(f)
    except:
        pass

    current_tokens = 0
    to_translate = []

    for i, token in enumerate(token_count):
        word = token[0]
        count = token[1]
        current_tokens += count

        # известные слова пропускаем
        if word in known or word.isdigit() or len(word) == 1:
            continue

        ans = input(
            f"({i + 1} of {token_len}, {current_tokens * 100 // total_tokens}%) Do you know word '{word}' [{count} times]?: ").lower()

        if ans == 'stop':
            break
        elif ans == 'y':
            known.append(word)
        elif ans == 'n':
            to_translate.append(word)

    # сохранение словаря известных слов
    try:
        with open(known_filepath, encoding='utf-8', mode='w') as f:
            json.dump(known, f)
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
        r = re.compile(rf'({en})', re.IGNORECASE)
        node_inner_html = r.sub(rf'\1 /{ru}/', node_inner_html)

    translated_file_path = f'{os.path.splitext(file_path)[0]}_translated.html'
    with open(translated_file_path, encoding='utf-8', mode='w') as f:
        f.write(f'<!DOCTYPE html><html><head></head><body>{node_inner_html}</body></html>')

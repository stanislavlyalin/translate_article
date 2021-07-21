# coding: utf-8
import re

import nltk
from bs4 import BeautifulSoup
from newspaper import Article
from readability import Document


class ReadableArticle:
    def __init__(self, url: str):
        self.url = url
        self.article = Article(url)
        self.article.download()
        self.article.parse()
        self.doc = Document(self.article.html)
        title = self.doc.title()
        self.bs_doc = BeautifulSoup(self.doc.get_clean_html(), 'html.parser')
        self.__replace_resource_url()

    def text(self):
        return self.article.text

    def head(self):
        return self.bs_doc.find('head')

    def body(self):
        return self.bs_doc.find('body')

    def title(self):
        return self.doc.title()

    def text_nodes(self):
        for node in self.body().findChildren(text=True, recursive=True):
            yield node

    def tokens(self):
        tokens = []
        for text in self.text_nodes():
            for token in nltk.regexp_tokenize(text.lower(), r"[-\w']+"):
                if token not in tokens:
                    tokens.append(token)
        return tokens

    def body_html(self):
        return self.body().decode_contents()

    def whole_html(self):
        return self.bs_doc.prettify(encoding='utf-8', formatter=None)

    def __replace_resource_url(self):
        # replace all image tags
        domain = ''
        m = re.search('(https?://.*?)/', self.url)
        if m:
            domain = m[1]
        for img in self.bs_doc.find_all('img', {'src': True}):
            if 'http' not in img['src']:
                img['src'] = 'https:' + img['src']
        for a in self.bs_doc.find_all('a', {'href': True}):
            if 'http' not in a['href']:
                a['href'] = domain + a['href']

# coding: utf-8

import spacy

nlp = spacy.load('en_core_web_sm')

rules = {
    'present continues': {'root': 'VBG', 'children': [{'dep': 'aux', 'tag': 'VBP'}]},
    'present simple': {'root': 'VBP', 'children': []},
    'present perfect': {'root': 'VBN', 'children': [{'dep': 'aux', 'tag': 'VBP'}]},
    'present perfect continues': {'root': 'VBG',
                                  'children': [{'dep': 'aux', 'tag': 'VBP'}, {'dep': 'aux', 'tag': 'VBN'}]},

    'past continues': {'root': 'VBG', 'children': [{'dep': 'aux', 'tag': 'VBD'}]},
    'past simple': {'root': 'VBD', 'children': []},
    'past perfect': {'root': 'VBN', 'children': [{'dep': 'aux', 'tag': 'VBD'}]},
    'past perfect continues': {'root': 'VBG', 'children': [{'dep': 'aux', 'tag': 'VBD'}, {'dep': 'aux', 'tag': 'VBN'}]},

    'future continues': {'root': 'VBG', 'children': [{'dep': 'aux', 'tag': 'MD'}, {'dep': 'aux', 'tag': 'VB'}]},
    'future simple': {'root': 'VB', 'children': [{'dep': 'aux', 'tag': 'MD'}]},
    'future perfect': {'root': 'VBN', 'children': [{'dep': 'aux', 'tag': 'MD'}, {'dep': 'aux', 'tag': 'VB'}]},
    'future perfect continues': {'root': 'VBG', 'children': [{'dep': 'aux', 'tag': 'MD'}, {'dep': 'aux', 'tag': 'VB'},
                                                             {'dep': 'aux', 'tag': 'VBN'}]},
}


def tense(sentence: str) -> str:
    sent = list(nlp(sentence).sents)[0]
    for name, rule in rules.items():
        root_equals = rule['root'] == sent.root.tag_

        rule_children = set(['%s-%s' % (child['dep'], child['tag']) for child in rule['children']])
        sent_children = set(['%s-%s' % (child.dep_, child.tag_) for child in sent.root.children])

        children_equals = rule_children.intersection(sent_children) == rule_children

        if root_equals and children_equals:
            return name
    return 'not defined'


def tense_schema(tense: str) -> str:
    tense_to_schema = {
        'present continues':         '|     | --> |     |',
        'present simple':            '|     |  O  |     |',
        'present perfect':           '|     | ->x |     |',
        'present perfect continues': '|     |a-->b|     |',
        'past continues':            '| --> |     |     |',
        'past simple':               '|  O  |     |     |',
        'past perfect':              '| ->x |     |     |',
        'past perfect continues':    '|a-->b|     |     |',
        'future continues':          '|     |     | --> |',
        'future simple':             '|     |     |  O  |',
        'future perfect':            '|     |     | ->x |',
        'future perfect continues':  '|     |     |a-->b|'
    }
    return tense_to_schema[tense]

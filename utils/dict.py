# coding: utf-8

import json


def known_filepath(token: str):
    """
    Returns filepath of known words dict
    :param token: users access token
    :return: filepath of known words dict
    """
    return f'{token}_known.json'


def unknown_filepath(token: str):
    """
    Returns filepath of unknown words dict
    :param token: users access token
    :return: filepath of unknown words dict
    """
    return f'{token}_unknown.json'


def load_dict(file_path: str):
    """
    Loads dict with words
    :param file_path: path to the dict file
    :return: set of words from dict
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            return set(json.load(f))
    except:
        return set()


def save_dict(tokens: set, file_path: str):
    """
    Saves dictionary to the given file
    :param tokens: dictionary tokens to save
    :param file_path: path to the dict file
    """
    try:
        with open(file_path, encoding='utf-8', mode='w') as f:
            json.dump(list(tokens), f, indent=2)
    except Exception as e:
        print(e)


def load_global():
    try:
        with open(__global_filepath(), encoding='utf-8') as f:
            return dict(json.load(f))
    except:
        return dict()


def save_global(dictionary: dict):
    try:
        with open(__global_filepath(), encoding='utf-8', mode='w') as f:
            json.dump(dictionary, f, indent=2)
    except Exception as e:
        print(e)


def __global_filepath():
    """
    Returns filepath of global dictionary
    includes translations and transcriptions
    :return: filepath of global dictionary
    """
    return 'global_dictionary.json'

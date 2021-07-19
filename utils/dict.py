# coding: utf-8
def load_known_dict(file_path: str):
    """
    Loads dict with known words
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
    Loads dict with unknown words and additional information
    :param file_path: path to the dict file
    :return: dict of {words: additional information}
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.readlines()

        unknown = {}
        for x in content:
            word, translation, transcription, context = x.strip().split(';')
            unknown[word] = (translation, transcription, context)
        return unknown
    except:
        return {}


def save_known_dict(known: set, file_path: str):
    """
    Saves known words to the given file
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
    Saves unknown words with additional information to the given file
    :param unknown: dict of unknown words (key) with addit. information (value)
    :param file_path: path to the dict file
    """
    try:
        with open(file_path, encoding='utf-8', mode='w') as f:
            for word in sorted(unknown):
                translation, transcription, context = unknown[word]
                f.write(f'{word};{translation};{transcription};{context}\n')
    except:
        pass

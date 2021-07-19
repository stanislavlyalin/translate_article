# coding: utf-8
import hashlib
from pathlib import Path

hashes_filepath = 'user_hashes.txt'


def hash(email, password):
    """
    Calculates MD5-hash for given email-password pair with salt
    :param email: email
    :param password: password
    :return: MD5-hash
    """
    salt = 'my_awesome_service'
    return hashlib.md5(f'{email}{password}{salt}'.encode('utf-8')).hexdigest()


def is_user_registered(token):
    """
    Checks is user registered in system or not
    :param token: users token (email-password hash)
    :return: True if user registered. Otherwise False
    """
    if Path(hashes_filepath).is_file():
        with open(hashes_filepath, encoding='utf-8') as f:
            hashes = [line.strip() for line in f.readlines()]
            return token in hashes
    return False

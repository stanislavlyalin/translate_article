# coding: utf-8

import argparse
from pathlib import Path

from utils.auth import hashes_filepath, hash

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', help='User email', required=True, type=str)
    parser.add_argument('--password', help='User password', required=True,
                        type=str)
    args = parser.parse_args()

    hashes = set()
    if Path(hashes_filepath).is_file():
        with open(hashes_filepath, encoding='utf-8') as f:
            lines = f.readlines()
        hashes = set([line.strip() for line in lines])

    new_user_hash = hash(args.email, args.password)
    hashes.add(new_user_hash)

    with open(hashes_filepath, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(hashes))

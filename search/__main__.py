# __main__.py

from __future__ import print_function

from argparse import ArgumentParser
from datetime import date
import logging
import sys
import re

from . import (
    InvalidQueryError,
    Query,
    search,
)
from .unittests.testobject import TestObject


if sys.version_info[0] >= 3:
    raw_input = input  # use input() on Python 3


def execute_query(search_str, dry_run):
    # if the query string starts with exit or quit -> stop.
    if any(search_str.lower().strip().startswith(k) for k in ['quit', 'exit']):
        return False

    values = [
        {'x': 2, 'y': 2, 'foo': 3},
        {'x': 2, 'yy': 20, 'foo': 3},

        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        {'name': 'Mike', 'fo0d': 'bar', 'date': date.today()},
        {'name': 'mike', 'food': 'bar'},

        TestObject(x=3, y=2, foo='travis'),
        TestObject(name='Travis', age='None'),
        TestObject(name='Tim', age='*'),
        TestObject(name='.', age='192')
    ]

    try:
        results = search(search_str, values, dry_run)

        if dry_run:
            print(results)
        else:
            print('\nResults:')
            for r in results:
                print(' '*4, r)
            print('{} results found - out of {} records'.format(len(results), len(values)))
    except InvalidQueryError as e:
        print(f'Invalid Query: {e}')
    return True


def main():
    parser = ArgumentParser()
    parser.add_argument('cmds', nargs='*')
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-l', '--logging-level', default='info')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.logging_level.upper()))


    if args.cmds:
        for cmd in re.split(',|;', ' '.join(args.cmds)):
            print(f'{cmd.strip()}')
            if not execute_query(cmd, args.dryrun):
                return 0
        else:
            print()

    while True:
        if not execute_query(raw_input('search > '), args.dryrun):
            break
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
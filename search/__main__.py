# __main__.py

from __future__ import print_function

from argparse import ArgumentParser
from datetime import datetime
import logging
import sys
import re


from . import search
from .query import Query, InvalidQueryError
from .unittests.testobject import TestObject


if sys.version_info[0] >= 3:
    raw_input = input  # use input() on Python 3

def execute_query(search_str):
    values = [
        {'x': 2, 'y': 2, 'foo': 3},
        {'x': 2, 'yy': 20, 'foo': 3},

        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        {'name': 'Mike', 'fo0d': 'bar', 'date': datetime.today()},
        {'name': 'mike', 'food': 'bar'},

        TestObject(x=3, y=2, foo='travis'),
        TestObject(name='Travis', age='None'),
        TestObject(name='Tim', age='*'),
        TestObject(name='.', age='192')
    ]

    try:
        results = search(search_str, values)

        print('\nResults:')

        for r in results:
            print(' '*4, r)

        print('{} results found - out of {} records'.format(len(results), len(values)))

    except InvalidQueryError as e:
        print('Invalid Query: {}'.format(e))


def run_query(query_str, dryrun):
    if query_str.lower().strip() in ['quit', 'exit']:
        return True

    if dryrun:
        print(str(Query(query_str)))
    else:
        execute_query(query_str)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('cmds', nargs='*')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-dr', '--dryrun', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    cmds = ' '.join(args.cmds)

    if cmds:
        for cmd in re.split(',|;', cmds):
            if run_query(cmd, dryrun=args.dryrun):
                exit(0)
        else:
            print()

    while True:
        if run_query(raw_input('search > '), dryrun=args.dryrun):
            break
        print()
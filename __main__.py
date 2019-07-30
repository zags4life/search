# __main__.py

from argparse import ArgumentParser
from datetime import datetime
import logging
import sys
import re


from .query import Query
from .unittests.testobject import TestObject


if sys.version_info[0] >= 3:
    raw_input = input  # use input() on Python 3

def execute_query(search_str, dry_run=False, debug=False):
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
        q = Query(search_str)

        if not dry_run:
            print('{}'.format(q))

        results = q(values)

        if not dry_run:
            print('\nResults:')

            for v in results:
                print(' '*4, v)

            print('{} results found - out of {} records'.format(len(results), len(values)))

    except InvalidQueryError as e:
        print('Invalid Query: {}'.format(e))


def run_query(query_str, dryrun=False, debug=False):
    if query_str.lower().strip() in ['quit', 'exit']:
        return True

    if dryrun:
        print(str(Query(query_str)))
    else:
        execute_query(query_str, debug=debug)

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
            if cmd and run_query(cmd):
                exit(0)
        else:
            print()

    while True:
        search_str = raw_input('search > ')

        if not search_str:
            continue

        if run_query(search_str, dryrun=args.dryrun, ):
            break
        print()
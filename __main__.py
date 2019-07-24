# __main__.py

from .unittests import execute_query
from .query import Query

from argparse import ArgumentParser
import logging
import sys
import re

if sys.version_info[0] >= 3:
    raw_input = input  # use input() on Python 3


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
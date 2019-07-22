# __main__.py

from .unittests import run
from .unittests import execute_query
from .query import Query

from argparse import ArgumentParser
import logging
import sys

def is_quit(s):
    return s.lower().strip() == 'quit' or s.lower().strip() == 'exit'

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('cmd', nargs='*')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)# if args.debug else logging.INFO)

    cmd = ' '.join(args.cmd)

    if sys.version_info[0] >= 3:
        raw_input = input  # use input() on Python 3

    while True:
        search_str = raw_input('search > ') if not cmd else cmd

        if not search_str:
            continue

        # if search_str.lower().strip() == 'quit' \
                # or search_str.lower().strip() == 'exit':
        if is_quit(search_str):
            break

        if args.debug:
            print(str(Query(search_str)))
        else:
            execute_query(search_str, debug=args.debug)
        print()
        cmd = None
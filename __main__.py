# __main__.py

from .unittests import run
from .unittests import execute_query
from .query import Query

from argparse import ArgumentParser
import logging
import sys

if __name__ == '__main__':
    if sys.version_info[0] >= 3:
        raw_input = input  # use input() on Python 3
            
    logging.basicConfig(level=logging.DEBUG)
    
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    
    while True:
        search_str = input('search > ')
        if search_str.lower().strip() == 'quit' \
                or search_str.lower().strip() == 'exit':
            break
        if args.debug:
            print(str(Query(search_str)))
        else:
            execute_query(search_str.lower().strip(), debug=args.debug)
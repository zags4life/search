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
from .decorators import show_stack_values


if sys.version_info[0] >= 3:
    raw_input = input  # use input() on Python 3


VALUES = [
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


class TestExecutor:
    def __init__(self, initial_cmds, log_level, dry_run):
        self.log_level = log_level
        self.dry_run = dry_run

        self.initial_cmds = f'@log {log_level};' + initial_cmds

    def run(self):
        if self.initial_cmds:
            for cmd in re.split(',|;', self.initial_cmds):
                if cmd and not self.execute(cmd):
                    return 0

        while True:
            user_input = raw_input('search > ')
            if not self.execute(user_input):
                break
        return 0

    def execute(self, search_str):
        return self.execute_cmd(search_str) if self.is_cmd(search_str) \
            else self.execute_search(search_str)

    def execute_cmd(self, cmd):
        cmd = cmd.strip().lower()
        if any(cmd.startswith(k) for k in ['quit', 'exit']):
            logging.info(f'Exit - thanks for coming')
            return False

        if cmd.startswith('@log'):
            cmds = cmd.split(' ')
            if len(cmds) < 2:
                logging.error('Invalid cmd - @log requires additional parameter.'
                    'E.g. "@log debug"')
            else:
                level_str = cmds[1].upper()
                level = getattr(logging, level_str)

                logger = logging.getLogger()
                logger.setLevel(level)

                logger.info(f'Set {logger.name} logger to {level_str}')
        
        if cmd.startswith('@dryrun'):
            self.dry_run = not self.dry_run
            logging.info(f'Set dry_run to {self.dry_run}')
        return True

    def execute_search(self, search_str):
        '''Execute search and display results'''
        try:
            results = search(search_str, VALUES, self.dry_run)

            if self.dry_run:
                logging.info(results)
            else:
                logging.info('\nResults:')
                for r in results:
                    logging.info(f"{' '*4} {r}")
                logging.info(f'{len(results)} results found - out of {len(VALUES)} records')
        except InvalidQueryError as e:
            logging.info(f'Invalid Query: {e}')
        return True

    @staticmethod
    def is_cmd(search_str):
        return re.search(r'(?i)^(@|quit|exit)', search_str.strip()) is not None


def main():
    parser = ArgumentParser()
    parser.add_argument('cmds', nargs='*')
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-l', '--logging-level', default='info')
    parser.add_argument('--print-values', action='store_true', 
        help="Print stack values.  This only works when --logging-level debug")
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s')

    show_stack_values(args.print_values)

    executor = TestExecutor(
        initial_cmds=' '.join(args.cmds),
        log_level=args.logging_level,
        dry_run=args.dryrun
    )
    return executor.run()


if __name__ == '__main__':
    sys.exit(main())
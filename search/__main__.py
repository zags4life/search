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
from .unittests.testobject import TestObject, NestedTestObject
from .decorators import show_stack_values


if sys.version_info[0] < 3:
    input = raw_input  # use raw_input() for Python 2


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
    TestObject(name='.', age='192'),
    NestedTestObject(**{'foo.bar.gurp': 10}),
    NestedTestObject(**{'person.age': 10}),
]


class TestExecutor:
    '''Test executor object is used when search is run directly from the
    command line and is intended for debuggging purposes only.  This object
    will allow the used to test different search queries using the test values
    defined in `VALUES`.

    This object will first run the initial commands then will create a CLI.

    Parameters:
        initial_cmds - a list of strings representing the initial cmds to run
        log_level - the python logging level to set.  This can be modified
            later from the TestExecutor CLI using the command
            `@log error|warn|warning|info|debug`.
        dry_run - a boolean indicating whether to execute the search in dry run
            mode.  This can be modified later from the TestExecutor CLI using
            the command `@dry_run true|false`.
    '''
    def __init__(self, initial_cmds, log_level, dry_run):
        self.log_level = log_level
        self.dry_run = dry_run

        self.initial_cmds = f'@log {log_level};' + initial_cmds

    def run(self):
        '''Runs the CLI, entering the message loop'''

        # Run the initial commands first.
        if self.initial_cmds:
            for cmd in re.split(',|;', self.initial_cmds):
                if cmd:
                    if not self.execute(cmd):
                        return 0
                    logging.info('')

        # Execute the user input
        while self.execute(input('search > ')):
            logging.info('')
        return 0

    def execute(self, user_input_str):
        '''Executes user input.  If the users input is a cmd (see `is_cmd` for
        what defines a cmd) the command will be executed, otherwise the user
        input will be used to search the test values.

        Parameters:
            user_input_str - the cmd specified by the user from the CLI

        Returns - False if the caller should exit the CLI message loop;
            otherwise True.
        '''
        return self.execute_cmd(user_input_str) if self.is_cmd(user_input_str) \
            else self.execute_search(user_input_str)

    def execute_cmd(self, cmd):
        cmd = cmd.strip().lower()
        if any(cmd.startswith(k) for k in ['quit', 'exit']):
            logging.info(f'Exit - thanks for coming')
            return False

        if cmd.startswith('@log'):
            return self.__update_logging_level(cmd)

        if cmd.startswith('@dryrun'):
            self.dry_run = not self.dry_run
            logging.info(f'Set dry_run to {self.dry_run}')
            return True
        
        # If we get here, the command is unknown / not supported
        logging.error(f"Unsupported command '{cmd}'")
        return True

    def execute_search(self, search_str):
        '''Execute search and display results'''
        try:
            results = search(search_str, VALUES, self.dry_run)

            if self.dry_run:
                logging.info(results)
            else:
                logging.info('')
                logging.info('Results:')
                for r in results:
                    logging.info(f"{' '*4} {r}")
                logging.info(
                    f'{len(results)} results found - out of '
                    f'{len(VALUES)} records')
                
        except InvalidQueryError as e:
            logging.info(f'Invalid Query: {e}')
        return True

    @staticmethod
    def is_cmd(user_input_str):
        '''Static method that determines if the cli string, entered by the
        user, is a command.  If it is a command, this method will return True;
        otherwise False.

        A user input string is determined to be a command if the string is
        `quit`, `exit`, or starts with `@`.

        Parameters:
            user_input_str - the user input, as a string

        Returns - True if user_input_str is a command; otherwise False.
        '''
        return re.search(r'(?i)^(@|quit|exit)', user_input_str.strip()) is not None

    @staticmethod
    def __update_logging_level(cmd):
        assert cmd.startswith('@log')

        cmds = cmd.split(' ')
        if len(cmds) < 2:
            logging.error('Invalid cmd - @log requires additional parameter.'
                'E.g. "@log debug"')

        else:
            level_str = cmds[1].lower()

            if level_str == 'all':
                # enable printing values for each stacktrace
                show_stack_values(enable=True)

                # reset logging_level to debug
                level_str = 'debug'
            else:
                show_stack_values(enable=False)
            level = getattr(logging, level_str.upper())

            logger = logging.getLogger()
            logger.setLevel(level)

            logger.info(f'Set {logger.name} logger to {level_str}')
        return True


def main():
    parser = ArgumentParser()
    parser.add_argument('cmds', nargs='*')
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-l', '--logging-level', default='info',
        choices=['error', 'warn', 'warning', 'info', 'debug', 'all'])
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s')

    # Create a test executor and run it.
    executor = TestExecutor(
        initial_cmds=' '.join(args.cmds),
        log_level=args.logging_level,
        dry_run=args.dryrun
    )
    return executor.run()


if __name__ == '__main__':
    sys.exit(main())
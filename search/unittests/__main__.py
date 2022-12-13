# __main__.py

import argparse
import importlib
import logging
import os
import re

log = logging.getLogger(__name__)

from . import run

def main(tests_to_run):
    curdir = os.path.abspath(os.path.curdir)
    package_path = os.path.split(__file__.replace(curdir, ''))[0]
    package = '.'.join(t for t in re.split(r'[\\/]', package_path) if t)

    # import all python files in this module
    for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
        path = root.replace(curdir, '').replace(package_path, '')

        for file in [f for f in files if f.endswith(".py") and not f.startswith('__')]:
            file = '{}.{}'.format(path.replace('\\', '.'), file.replace('.py', ''))
            log.debug('importing module {} from package {}'.format(file, package))

            # import module
            importlib.import_module(file, package)

    # run all tests
    run(tests_to_run)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', choices=['error', 'warning', 'info', 'debug'], default='warning')
    parser.add_argument('-t', '--tests', default='.*')
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
    )

    exit(main(args.tests))
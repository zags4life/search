# __main__.py
import argparse
import importlib
import logging
import os
import re

logger = logging.getLogger(__name__)

from . import run


def main(args):
    tests_to_run = args.tests

    curdir = os.path.abspath(os.path.curdir)
    package_path = os.path.dirname(os.path.abspath(__file__))

    # Determine the package name
    package = '.'.join(
        p.replace('\\', '')
        for p in os.path.split(package_path.replace(curdir, '')) if p
    )
    if package.startswith('.'):
        package = package[1:]

    # import all python files in this module
    for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
        # if the current directory is pycache, ignore it and continue
        if '__pycache__' in root:
            continue

        path = root.replace(package_path, '')

        for file in [f for f in files if f.endswith(".py") and not f.startswith('__')]:
            filepath = path.replace('\\', '.')
            module = f"{filepath}.{file.replace('.py', '')}"

            logger.debug(f'importing module {package}{module}')

            # import module
            importlib.import_module(module, package)

    # run all tests
    run(tests_to_run, args.list_tests)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level',
        choices=['error', 'warning', 'info', 'debug'], default='info')
    parser.add_argument('--log-file')
    parser.add_argument('-t', '--tests', default='.*')
    parser.add_argument('-l', '--list', dest='list_tests', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        #format='%(name)-15s %(message)s' if not args.log_file \
        format='%(message)s' if not args.log_file \
            else '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
        filename=args.log_file,
        filemode='w'
    )

    exit(main(args))
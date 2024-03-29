# unittests/__init__.py
from datetime import datetime
import logging
import re
import time

from search import Query, InvalidQueryError

from .testobject import (
    TestObject,
    PropertyTestObject,
    NestedTestObject
)


logger = logging.getLogger(__name__)

REGISTERED_UNITTESTS = []


#NB: This should all be converted to pytest
def unittest(func):
    '''Decorator to register a test'''
    REGISTERED_UNITTESTS.append(func)
    return func
test = unittest


def run(test_filter, list_tests=False):
    '''Run tests based on the test filter, as a string, provided by the caller.

    Parameters:
        test_filter - a regular expression used to filter tests

    Returns - an int representing the number of failing test cases.
    '''
    start_time = time.time()


    filtered_tests = [t for t in REGISTERED_UNITTESTS
        if re.search(test_filter, t.__name__)]
    total_count = len(filtered_tests)
    failed_tests = []

    if filtered_tests:
        padding = max(len(t.__name__) for t in filtered_tests)

    for test in filtered_tests:
        name = ' '.join(
            [p.title() for p in test.__name__.replace('_', ' ').split()])
        name = name.replace('testobject', 'TestObject')

        try:
            if not list_tests:
                test()
            logger.info(f'{name:<{padding}}  '
                f'{"SKIP" if list_tests else "PASS"}')
        except AssertionError as e:
            logger.info(f'    {e}')
            logger.info(f'{name:<{padding}}  FAIL')
            failed_tests.append(name)

    _print_results(total_count, failed_tests, start_time)

    return len(failed_tests)


def _print_results(total_count, failed_tests, start_time):
    # Print failing test cases, if any
    for idx, failed_test in enumerate(failed_tests):
        if idx == 0:
            logger.info('')
            logger.info(f'Failed Tests:')
        logger.info(f'    {idx+1}) {failed_test}')

    padding = len(str(total_count))
    logger.info('')
    logger.info(f'Pass   {total_count - len(failed_tests):>{padding}}')
    logger.info(f'Fail   {len(failed_tests):>{padding}}')
    logger.info(f"-------{'-' * padding}")
    logger.info(f'Total  {total_count:>{padding}}')
    logger.info('')
    logger.info(f'Total time: {time.time() - start_time:,.2f} secs')

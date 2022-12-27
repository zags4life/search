# unittest/__init__.py

from datetime import datetime
import logging
import re

from .testobject import (
    TestObject,
    PropertyTestObject,
    NestedTestObject
)
from ..query import Query, InvalidQueryError


logger = logging.getLogger(__name__)

REGISTERED_UNITTESTS = []


def unittest(log=logger):
    '''Decorator to register a test'''
    def decorator(func):
        REGISTERED_UNITTESTS.append((func, log))
        return func
    return decorator
test = unittest


def run(test_case_filter):
    '''Run tests based on the test filter, as a string, provided by the caller.
    
    Parameters:
        test_case_filter - a regular expression used to filter tests
        
    Returns - an int representing the number of failing test cases.
    '''
    filtered_tests = [t for t in REGISTERED_UNITTESTS 
        if re.search(test_case_filter, t[0].__name__)]
    total_count = len(filtered_tests)
    failed_tests = []

    for test, log in filtered_tests:
        try:
            test()
            log.info(f'{test.__name__} - pass')
        except AssertionError as e:
            log.info(f'{test.__name__} - FAIL\n    {e}')
            failed_tests.append(test.__name__)

    _print_results(total_count, failed_tests)
    return len(failed_tests)
    
def _print_results(total_count, failed_tests):
    # Print failing test cases, if any
    for idx, failed_test in enumerate(failed_tests):
        if idx == 0:
            logger.info('')
            logger.info(f'Failed Tests:')
        logger.info(f'    {idx+1}) {failed_test}')

    padding = len(str(total_count))
    logger.info('')
    logger.info(f' Pass   {total_count - len(failed_tests):>{padding}}')
    logger.info(f' Fail   {len(failed_tests):>{padding}}')
    logger.info(f" -------{'-' * padding}")
    logger.info(f' Total  {total_count:>{padding}}')

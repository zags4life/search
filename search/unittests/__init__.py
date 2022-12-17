# unittest/__init__.py

from datetime import datetime
import logging
import re

from .testobject import TestObject, TestFieldObject
from ..query import Query, InvalidQueryError

logger = logging.getLogger(__name__)
REGISTERED_UNITTESTS = []


def unittest(log):
    '''Decorator to register a test'''
    def decorator(func):
        REGISTERED_UNITTESTS.append((func, log))
        return func
    return decorator
test = unittest


def run(tests_to_run):
    pass_count = 0
    fail_count = 0
    total_count = 0

    filtered_tests = [test for test in REGISTERED_UNITTESTS
        if re.search(tests_to_run, test[0].__name__)]
    total_count = len(filtered_tests)

    for test, log in filtered_tests:
        try:
            log.info(f'{test.__name__}')
            test()
            log.info(f'{test.__name__} - PASS\n')
            pass_count += 1
        except AssertionError as e:
            log.error(e)
            fail_count += 1

    padding = len(str(total_count))

    logger.info(f' pass   {pass_count:>{padding}}')
    logger.info(f' fail   {fail_count:>{padding}}')
    logger.info(f" -------{'-' * padding}")
    logger.info(f' total  {total_count:>{padding}}')

    return fail_count
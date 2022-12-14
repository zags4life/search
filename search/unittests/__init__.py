# unittest/__init__.py

from datetime import datetime
import logging
import re

from .testobject import TestObject, TestFieldObject
from ..query import Query, InvalidQueryError

logger = logging.getLogger(__name__)

REGISTERED_UNITTESTS = []

def unittest(func):
    '''Decorator to register tests
    '''
    REGISTERED_UNITTESTS.append(func)
test = unittest


def run(tests_to_run):
    result = 0
    fail_count = 0
    total_count = 0

    for test in REGISTERED_UNITTESTS:
        if not re.search(tests_to_run, test.__name__):
            continue

        total_count += 1
        try:
            logger.info(f'{test.__name__}')
            test()
            logger.info(f'{test.__name__} - PASS\n')
        except AssertionError as e:
            logger.error(e)
            result = 1
            fail_count += 1

    pass_count = total_count - fail_count
    padding = len(str(total_count))

    logger.info(f' pass   {pass_count:>{padding}}')
    logger.info(f' fail   {fail_count:>{padding}}')
    logger.info(f" -------{'-' * padding}")
    logger.info(f' total  {total_count:>{padding}}')

    return result
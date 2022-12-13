# unittest/__init__.py

from datetime import datetime
import logging
import re

from .testobject import TestObject
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
    for test in REGISTERED_UNITTESTS:
        if not re.search(tests_to_run, test.__name__):
            continue

        try:
            logger.info(f'{test.__name__}')
            test()
            logger.info(f'{test.__name__} - PASS\n')
        except AssertionError as e:
            logger.error(e)
    return result
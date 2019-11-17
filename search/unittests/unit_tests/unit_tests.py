# unit_tests/unit_tests.py

import logging

from .. import test

logger = logging.getLogger(__name__)

@test
def unittest():
    query = 'name like (?i)mike and ^fo{2}'
    print(query)
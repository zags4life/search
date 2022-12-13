# unit_tests/unit_tests.py

import logging

from .. import test, TestObject
from ... import query

logger = logging.getLogger(__name__)

def log_results(expected, actual):
    logger.debug('Found results:')
    for result in actual:
        logger.debug(f'    {result}')

    logger.debug('Expected results:')
    for result in expected:
        logger.debug(f'    {result}')
        

def validate_results(expected, actual):
    log_results(expected, actual)

    assert len(actual) == len(expected), \
        f'Incorrect number of results.  ' \
        f'Expected: {len(expected)}  Actual: {len(actual)}'

    matches = []

    for expected_result in expected:
        match = True
        for result in actual:
            if expected_result == result:
                break
        else:
            match &= False

        matches.append((expected_result, match))

    # Assert all expected results were found in results
    assert all(m[1] for m in matches), \
        f'Unexpected search results:' \
        f"{' '.join([f'{er} - found {found}' for er, found in matches if not found])}"


@test
def unittest_test_objects():
    query_str = 'name like (?i)mike and ^fo{2}'

    expected_results = [
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=3, y=2, foo='gurp', name='Mike'),
    ]

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=3, y=2, foo='gurp', name='Mike'),
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
    ]

    results = query(query_str, values)
    validate_results(expected_results, results)
    

@test
def unittest_mix_objects():
    query_str = 'x = 3 and (name like (?i)mike and ^fo{2})'

    expected_results = [
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        dict(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=3, y=2, foo='gurp', name='Mike'),
    ]

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        dict(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=3, y=2, foo='gurp', name='Mike'),
        dict(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
    ]

    results = query(query_str, values)    
    validate_results(expected_results, results)
    
    
@test
def unittest_mix_objects_no_results():
    query_str = 'x = 1 and (name like (?i)mike and ^fo{2})'

    expected_results = []

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        dict(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=3, y=2, foo='gurp', name='Mike'),
        dict(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp'),
    ]

    results = query(query_str, values)    
    validate_results(expected_results, results)
# unit_tests/unit_tests.py
import logging

from .. import test, TestObject, TestFieldObject
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


@test
def unittest_strings():
    query_str = 'name like (?i)mike and ^fo{1}'
    expected_results = [
        {'name': 'Mike', 'fo0d': 'bar'},
    ]

    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        TestFieldObject(x=1, y=2, foo='bar')
    ]

    results = query(query_str, values)
    validate_results(expected_results, results)


@test
def unittest_empty_query():
    '''Verify that empty query string returns the complete set of values'''
    query_str = ''

    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
    ]
    expected_results = values

    results = query(query_str, values)
    validate_results(expected_results, results)


@test
def unittest_int_and_query():
    ''''''
    query_str = 'x = 1 and y <= 5'
    expected_results = [
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar')
    ]

    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar'),
        dict(x='3', y=5, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
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
    
    
@test
def unittest_lists_and_dicts_case_insensitive_regex():
    query_str = 'x = 3 or (name like (?i)mike and ^fo{2})'

    expected_results = [
        dict(x=3, y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x=3, y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    results = query(query_str, values)    
    validate_results(expected_results, results)
    
    
@test
def unittest_lists_and_dicts_case_sensitive_regex():
    query_str = 'x = 3 or (name like mike and ^fo{2})'

    expected_results = [
        dict(x=3, y=2, foo='gurp'),
        dict(x=5, y=2, foo='gurp', name='mike'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x=3, y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    results = query(query_str, values)
    validate_results(expected_results, results)
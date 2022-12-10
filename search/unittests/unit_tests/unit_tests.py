# unit_tests/unit_tests.py

import logging

from .. import test, TestObject
from ... import query

logger = logging.getLogger(__name__)

class TestPropertyObject(TestObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def name(self):
        return 'Mike'

@test
def unittest_strings():
    query_str = 'name like (?i)mike and ^fo{1}'
    expected_results = [
        {'name': 'Mike', 'fo0d': 'bar'},
        TestPropertyObject(x=1, y=2, foo='bar')
    ]
    
    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        TestPropertyObject(x=1, y=2, foo='bar')
    ]
    print(f'QUERY: {query_str}')
    results = query(query_str, values)
    print(f'RESULTS: {results}')

    assert len(results) == len(expected_results), \
        f'Expected: {len(expected_results)}  Actual: {len(results)}'
    # assert results == expected_results, \
        # f'Expected: {expected_results}  Actual: {results}'


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
    print(f'QUERY: {query_str}')
    results = query(query_str, values)
    print(f'RESULTS: {results}')
    
    assert results == values


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
    print(f'QUERY: {query_str}')
    results = query(query_str, values)
    print(f'RESULTS: {results}')
    
    assert len(results) == len(expected_results), \
        f'Expected: {len(expected_results)}  Actual: {len(results)}'
    # assert results == expected_results, \
        # f'Expected: {expected_results}  Actual: {results}'


@test
def unittest_int_or_query():
    ''''''
    query_str = 'x = 1 or y <= 5'
    expected_results = [
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar'),
        dict(x='3', y=5, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
    ]
    
    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar'),
        dict(x='3', y=5, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
    ]
    print(f'QUERY: {query_str}')
    results = query(query_str, values)
    print(f'RESULTS: {results}')
    
    assert len(results) == len(expected_results), \
        f'Expected: {len(expected_results)}  Actual: {len(results)}'
    # assert results == expected_results, \
        # f'Expected: {expected_results}  Actual: {results}'


@test
def unittest_int_or_parans_query():
    ''''''
    query_str = 'x = 1 or (y <= 5 and y > 2)'
    expected_results = [
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar'),
        dict(x='3', y=5, foo='gurp'),
    ]
    
    values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=4, foo='bar'),
        dict(x='3', y=5, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
    ]
    print(f'QUERY: {query_str}')
    results = query(query_str, values)
    print(f'RESULTS: {results}')
    
    assert len(results) == len(expected_results), \
        f'Expected: {len(expected_results)}  Actual: {len(results)}'
    # assert results == expected_results, \
        # f'Expected: {expected_results}  Actual: {results}'
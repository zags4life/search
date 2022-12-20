# unit_tests/unit_tests.py
import logging

from .. import (
    unittest, 
    TestObject, 
    TestFieldObject
)
from .utils import run_unittest_and_verify_results

logger = logging.getLogger(__name__)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_strings():
    query_str = 'name like (?i)mike'
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
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

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_None_value():
    query_str = 'x = None'

    expected_results = [
        dict(x=None, y=2, foo='gurp'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x=None, y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_empty_string_single_quotes():
    query_str = "x = ''"

    expected_results = [
        dict(x='', y=2, foo='gurp'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x='', y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_empty_string_double_quotes():
    query_str = 'x = ""'

    expected_results = [
        dict(x='', y=2, foo='gurp'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x='', y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_quoted_string_single_quotes():
    query_str = "name = 'mIke'"

    expected_results = [
        dict(x=4, y=2, foo='gurp', name='mIke'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x='', y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_quoted_string_double_quotes():
    query_str = 'name = "mIke"'

    expected_results = [
        dict(x=4, y=2, foo='gurp', name='mIke'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x='', y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
    
    
@unittest(logger)
def unittest_quoted_string_mixed_quotes():
    query_str = 'name = \'mIke"'

    expected_results = [
        dict(x=4, y=2, foo='gurp', name='mIke'),
    ]

    values = [
        ['x', 1, 2, 3],
        dict(x='', y=2, foo='gurp'),
        dict(x=4, y=2, foo='gurp', name='mIke'),
        dict(x=5, y=2, foo='gurp', name='mike'),
        dict(x=6, y=2, foo='gurp', name='Mike'),
        dict(x=7, y=2, foo='gurp'),
        dict(x=8, y=2, foo='gurp'),
        dict(x=9, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)
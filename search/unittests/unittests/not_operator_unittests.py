# not_operator_unittests.py

from search import search

from . import (
    logger, 
    run_unittest_and_verify_results, 
    validate_results
)
from .. import unittest
from ..testobject import (
    TestObject,
    PropertyTestObject
)

VALUES = [
    TestObject(x=3, y=2, foo='gurp'),
    TestObject(x=3, y=2, foo='gurp', name='mIke'),
    TestObject(x=3, y=2, foo='gurp', name='mike'),
    TestObject(x=1, y=2, foo='gurp', name='Mike'),
    TestObject(x=2, y=2, foo='gurp'),
    TestObject(x=4, y=2, foo='gurp'),
]


@unittest(logger)
def unittest_not():
    '''Validate simple not operator'''
    for query_str in ['!name like (?i)mike', '!(name like (?i)mike)']:
        run_unittest_and_verify_results(
            query_str=query_str, 
            values=VALUES, 
            expected_values=VALUES[:1] + VALUES[-2:]
        )


@unittest(logger)
def unittest_not_not():
    '''Validate that two not operators are equivalent to no not operator.
    E.g. NOT NOT condition == condition
    '''
    expected_values = VALUES[-2:-1]

    query_str1 = '!!x=2'
    query_str2 = 'x=2'
    
    results1 = search(query_str1, VALUES)
    results2 = search(query_str2, VALUES)
    
    # Validate that each query returned the expected set
    validate_results(expected_values, results1)
    validate_results(expected_values, results2)
    
    # Validate that both resulting set are identical
    validate_results(results1, results2)
    
    assert results1 == results2

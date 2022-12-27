# operator_unittests.py
from . import logger
from .. import unittest
from ..testobject import (
    TestObject,
    PropertyTestObject
)
from .utils import run_unittest_and_verify_results


@unittest(logger)
def unittest_equals():
    query_str = 'x=3'

    expected_results = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
    ]

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=1, y=2, foo='gurp'),
    ]
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_not_equals():
    query_str = 'x != 3'

    expected_results = [
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=1, y=2, foo='gurp'),
    ]

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=1, y=2, foo='gurp'),
    ]

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_less_than():
    query_str = 'x < 3'

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=1, y=2, foo='gurp'),
    ]
    expected_results = values[3:]

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_less_than_or_equal():
    query_str = 'x <= 3'

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[:-1]

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_greater_than():
    query_str = 'x > 3'

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[-1:]

    run_unittest_and_verify_results(query_str, values, expected_results)
    

@unittest(logger)
def unittest_greater_than_or_equal():
    query_str = 'x >= 3'

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[:3] + values[-1:]
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_like():
    query_str = 'name like Mike'

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[3:4]

    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest(logger)
def unittest_not():
    for query_str in ['!name like (?i)mike', '!(name like (?i)mike)']:
        values = [
            TestObject(x=3, y=2, foo='gurp'),
            TestObject(x=3, y=2, foo='gurp', name='mIke'),
            TestObject(x=3, y=2, foo='gurp', name='mike'),
            TestObject(x=1, y=2, foo='gurp', name='Mike'),
            TestObject(x=2, y=2, foo='gurp'),
            TestObject(x=4, y=2, foo='gurp'),
        ]
        expected_results = values[:1] + values[-2:]

        run_unittest_and_verify_results(query_str, values, expected_results)
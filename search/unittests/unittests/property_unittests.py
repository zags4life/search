# property_unittests.py
from . import run_unittest_and_verify_results
from .. import unittest
from ..testobject import PropertyTestObject

def update_property_values(values):
    for v in values:
        v.update()

@unittest
def unittest_properties_equals():
    query_str = 'x=3'

    expected_results = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
    ]
    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=1, y=2, foo='gurp'),
    ]
    
    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_not_equals():
    query_str = 'x != 3'

    expected_results = [
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=1, y=2, foo='gurp'),
    ]

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=1, y=2, foo='gurp'),
    ]

    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_less_than():
    query_str = 'x < 3'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=1, y=2, foo='gurp'),
    ]
    expected_results = values[3:]

    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_less_than_or_equal():
    query_str = 'x <= 3'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[:-1]

    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_greater_than():
    query_str = 'x > 3'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[-1:]

    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)
    

@unittest
def unittest_properties_greater_than_or_equal():
    query_str = 'x >= 3'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[:3] + values[-1:]
    
    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_like():
    query_str = 'name like Mike'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=4, y=2, foo='gurp'),
    ]
    expected_results = values[3:4]

    update_property_values(expected_results)
    update_property_values(values)
    
    run_unittest_and_verify_results(query_str, values, expected_results)


@unittest
def unittest_properties_any():
    query_str = 'name'

    values = [
        PropertyTestObject(x=3, y=2, foo='gurp'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mIke'),
        PropertyTestObject(x=3, y=2, foo='gurp', name='mike'),
        PropertyTestObject(x=1, y=2, foo='gurp', name='Mike'),
        PropertyTestObject(x=2, y=2, foo='gurp'),
        PropertyTestObject(x=4, y=2, foo='gurp'),
    ]

    update_property_values(values)
    expected_results = values
    
    run_unittest_and_verify_results(query_str, values, expected_results)
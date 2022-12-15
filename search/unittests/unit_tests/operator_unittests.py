# operator_unittests.py

from .. import test, TestObject, TestFieldObject
from ... import query


from .utils import validate_results

@test
def unittest_equals():
    query_str = 'x=3'

    expected_results = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
    ]

    values = [
        TestObject(x=3, y=2, foo='gurp'),
        TestObject(x=3, y=2, foo='gurp', name='mIke'),
        TestObject(x=3, y=2, foo='gurp', name='mike'),
        TestObject(x=1, y=2, foo='gurp', name='Mike'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=2, y=2, foo='gurp'),
        TestObject(x=1, y=2, foo='gurp'),
    ]
    
    results = query(query_str, values)
    validate_results(expected_results, results)
    

@test
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
    
    results = query(query_str, values)
    validate_results(values[3:], results)


@test
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
    
    results = query(query_str, values)
    validate_results(values[3:], results)
    


@test
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
    
    results = query(query_str, values)
    validate_results(values[:-1], results)
    


@test
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
    
    results = query(query_str, values)
    validate_results(values[-1:], results)
    

@test
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
    
    results = query(query_str, values)
    validate_results(values[:3] + values[-1:], results)


@test
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
    
    results = query(query_str, values)
    validate_results(values[3:4], results)
# nest_objects.py

from . import logger
from .. import (
    unittest, 
    TestObject, 
    NestedTestObject
)
from .utils import run_unittest_and_verify_results


@unittest(logger)
def nested_object_unittest():
    query_str = 'foo.bar.gurp=10'
    values = [
        NestedTestObject.create_instance({'foo.bar.gurp': 10}),
        TestObject(foo=10),
        {'foo.bar': 10},
        {'foo.bar.gurp': 10},
    ]
    
    expected_values = values[:1] + values[3:]
    
    run_unittest_and_verify_results(query_str, values, expected_values)


@unittest(logger)
def nested_object_wildcard_name_unittest():
    query_str = 'foo.[a-zA-Z]+.gurp=10'
    values = [
        NestedTestObject.create_instance({'foo.bar.gurp': 10}),
        NestedTestObject.create_instance({'foo.bar.gurp.gurp': 10}),
        TestObject(foo=10),
        {'foo.bar': 10},
        {'foo.foo.gurp': 10},
    ]
    
    expected_values = values[:1] + values[-1:]
    
    run_unittest_and_verify_results(query_str, values, expected_values)
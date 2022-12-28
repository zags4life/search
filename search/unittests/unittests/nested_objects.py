# nest_objects.py

from . import logger, run_unittest_and_verify_results
from .. import (
    unittest,
    TestObject,
    NestedTestObject
)


@unittest(logger)
def unittest_nested_object():
    for query_str in ['foo.bar.gurp=10', 'foo\.bar\.gurp=10']:

        values = [
            NestedTestObject.create_instance({'foo.bar.gurp': 10}), # match
            TestObject(foo=10),
            {'foo.bar': 10},
            {'foo.bar.gurp': 10}, # match
        ]

        expected_values = values[:1] + values[-1:]

        run_unittest_and_verify_results(query_str, values, expected_values)


@unittest(logger)
def unittest_nested_object_wildcard_name():
    query_str = 'fo.*\.[a-z]+\.gurp=10'
    values = [
        NestedTestObject.create_instance({'fo0.bar.gurp': 10}), # match
        NestedTestObject.create_instance({'foo.bar.gurp.gurp': 10}),
        TestObject(foo=10),
        {'foo.bar': 10},
        {'foo.foo.gurp': 10}, # match
    ]

    expected_values = values[:1] + values[-1:]

    run_unittest_and_verify_results(query_str, values, expected_values)
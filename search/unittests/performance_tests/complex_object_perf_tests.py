# property_execution_perf_tests.py
from . import logger
from .utils import run_perf_test
from .. import test


LARGE_TEST_COUNT = 100000
LARGE_TEST_ITERATION = 10


@test(logger)
def execution_performance_large_PropertyTestObject_test():
    iterations = LARGE_TEST_ITERATION
    count = LARGE_TEST_COUNT 

    setup_str = """
from search import search
from search.unittests.testobject import PropertyTestObject

values = []

for _ in range({0}):
    values.extend([
        PropertyTestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
        PropertyTestObject(**dict(x=1, y=2, foo='bar')),
        PropertyTestObject(**dict(x='3', y=2, foo='gurp')),
        PropertyTestObject(**dict(x=3, y=2, foo='gurp')),
        PropertyTestObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
        PropertyTestObject(**{{'name': 'Mike', 'foo': 'bar'}}),
    ])
    
for v in values:
    v.update()
""".format(count) # There are already 6 items

    statement = """
results = search('name = Mike', values)
expected_count = {0}

assert len(results) == expected_count, \
    f'Unexpected numbers of results.  ' \
    f'Expected: {{expected_count}}.  ' \
    f'Actual: {{len(results)}}'
""".format(int(count * 2))

    run_perf_test(iterations, count * 6, setup_str, statement)


@test(logger)
def execution_performance_large_NestedTestObject_test():
    iterations = LARGE_TEST_ITERATION
    count = LARGE_TEST_COUNT

    setup_str = """
from search import search
from search.unittests.testobject import NestedTestObject

values = []

for _ in range({0}):
    values.extend([
        NestedTestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
        NestedTestObject(**dict(x=1, y=2, foo='bar')),
        NestedTestObject(**dict(x='3', y=2, foo='gurp')),
        NestedTestObject(**dict(x=3, y=2, foo='gurp')),
        NestedTestObject(**{{'person.name': 'Mike', 'fo0d': 'bar'}}),
        NestedTestObject(**{{'person.name': 'Mike', 'foo': 'bar'}}),
    ])
""".format(count) # There are already 6 items

    statement = """
results = search('person.name = Mike', values)
assert len(results) == {0}
""".format(int(count * 2))

    run_perf_test(iterations, count * 6, setup_str, statement)
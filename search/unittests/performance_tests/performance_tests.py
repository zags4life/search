# performance_tests.py

import timeit

from . import logger
from .utils import run_perf_test
from .. import test


TEST_QUERY = 'fo=bar and !(x=2 and y = 3)'

BUILTIN_OBJECT_SETUP = """
from search import search
values=[
    {{'x': 1, 'y': 2, 'foo': 3}},
    dict(x=1, y=2, foo='bar'),
    dict(x='3', y=2, foo='gurp'),
    dict(x=3, y=2, foo='gurp'),
    [1,2,3,4],
    {{'name': 'Mike', 'fo0d': 'bar'}},
]*{0}
"""

BUILTIN_STATEMENT = f"""
results = search('{TEST_QUERY}', values)
expected_count = {{0}} * 2

assert len(results) == expected_count, \
    f'Invalid number of results: Expected: {{{{expected_count}}}}, ' \
    f'Actual: {{{{len(results)}}}}'
"""


@test(logger)
def end_to_end_query_performance_test():
    iterations = 20000

    total_time = timeit.timeit(
        """Query('foo=bar and x = 1')(values)""",
        setup="""from search.query import Query; values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        ]""",
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,}".format('Total items', 6))
    logger.info("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test(logger)
def compile_performance_test():
    iterations = 20000

    total_time = timeit.timeit(
        "Query('foo=bar')",
        setup="from search.query import Query",
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test(logger)
def execution_performance_test():
    iterations = 10000
    count = 6

    run_perf_test(
        iterations,
        count,
        setup=BUILTIN_OBJECT_SETUP.format(int(count/6)),
        statement=BUILTIN_STATEMENT.format(int(count/6))
    )

@test(logger)
def execution_performance_medium_test():
    iterations = 100
    count = 6000

    run_perf_test(
        iterations,
        count,
        setup=BUILTIN_OBJECT_SETUP.format(int(count/6)),
        statement=BUILTIN_STATEMENT.format(int(count/6))
    )


LARGE_TEST_COUNT = 600000
LARGE_TEST_ITERATION = 10


@test(logger)
def execution_performance_large_test():
    iterations = LARGE_TEST_ITERATION
    count = LARGE_TEST_COUNT

    run_perf_test(
        iterations,
        count,
        setup=BUILTIN_OBJECT_SETUP.format(int(count/6)),
        statement=BUILTIN_STATEMENT.format(int(count/6))
    )


@test(logger)
def execution_performance_large_TestObject_test():
    iterations = LARGE_TEST_ITERATION
    count = LARGE_TEST_COUNT

    setup_str = """
from search import search
from search.unittests.testobject import TestObject

values = []

for _ in range({0}):
    values.extend([
        TestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
        TestObject(**dict(x=1, y=2, foo='bar')),
        TestObject(**dict(x='3', y=2, foo='gurp')),
        TestObject(**dict(x=3, y=2, foo='gurp')),
        TestObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
        TestObject(**{{'name': 'Mike', 'foo': 'bar'}}),
    ])
""".format(int(count/6)) # There are already 6 items

    statement = """
results = search('fo=bar', values)
expected_count = {0}

assert len(results) == expected_count, \
    f'Unexpected numbers of results.  ' \
    f'Expected: {{expected_count}}.  ' \
    f'Actual: {{len(results)}}'
""".format(int(count/6*3))

    run_perf_test(iterations, count, setup_str, statement=statement)


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
""".format(int(count/6)) # There are already 6 items

    statement = """
results = search('name = Mike', values)
expected_count = {0}

assert len(results) == expected_count, \
    f'Unexpected numbers of results.  ' \
    f'Expected: {{expected_count}}.  ' \
    f'Actual: {{len(results)}}'
""".format(int(count/6*2))

    run_perf_test(iterations, count, setup_str, statement)


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
""".format(int(count/6)) # There are already 6 items

    statement = """
results = search('person.name = Mike', values)
assert len(results) == {0}
""".format(int(count/6*2))

    run_perf_test(iterations, count, setup_str, statement)
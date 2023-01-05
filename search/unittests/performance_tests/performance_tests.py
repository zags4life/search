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

EXCEPTION_HANDLING_STMT = f"search('{TEST_QUERY}', values)"


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
        statement=EXCEPTION_HANDLING_STMT
    )

@test(logger)
def execution_performance_medium_test():
    iterations = 100
    count = 6000

    run_perf_test(
        iterations,
        count,
        setup=BUILTIN_OBJECT_SETUP.format(int(count/6)),
        statement=EXCEPTION_HANDLING_STMT
    )

@test(logger)
def execution_performance_large_test():
    iterations = 10
    count = 600000

    run_perf_test(
        iterations,
        count,
        setup=BUILTIN_OBJECT_SETUP.format(int(count/6)),
        statement=EXCEPTION_HANDLING_STMT
    )


@test(logger)
def execution_performance_large_TestObject_test():
    iterations = 10
    count = 600000

    setup_str = """
from search import Query
from search.unittests.testobject import TestObject
q = Query('fo=bar')
values=[
    TestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
    TestObject(**dict(x=1, y=2, foo='bar')),
    TestObject(**dict(x='3', y=2, foo='gurp')),
    TestObject(**dict(x=3, y=2, foo='gurp')),
    TestObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
    TestObject(**{{'name': 'Mike', 'foo': 'bar'}}),
]*{0}
""".format(int(count/6)) # There are already 6 items

    run_perf_test(iterations, count, setup_str, statement="q(values)")


@test(logger)
def execution_performance_large_PropertyTestObject_test():
    iterations = 10
    count = 600000

    setup_str = """
from search import Query
from search.unittests.testobject import PropertyTestObject
q = Query('fo=bar')
values=[
    PropertyTestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
    PropertyTestObject(**dict(x=1, y=2, foo='bar')),
    PropertyTestObject(**dict(x='3', y=2, foo='gurp')),
    PropertyTestObject(**dict(x=3, y=2, foo='gurp')),
    PropertyTestObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
    PropertyTestObject(**{{'name': 'Mike', 'foo': 'bar'}}),
]*{0}
""".format(int(count/6)) # There are already 6 items

    statement = 'q(values)'

    run_perf_test(iterations, count, setup_str, statement)


@test(logger)
def execution_performance_large_NestedTestObject_test():
    iterations = 10
    count = 600000

    setup_str = """
from search import search
from search.unittests.testobject import NestedTestObject

values=[
    NestedTestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
    NestedTestObject(**dict(x=1, y=2, foo='bar')),
    NestedTestObject(**dict(x='3', y=2, foo='gurp')),
    NestedTestObject(**dict(x=3, y=2, foo='gurp')),
    NestedTestObject(**{{'person.name': 'Mike', 'fo0d': 'bar'}}),
    NestedTestObject(**{{'person.name': 'Mike', 'foo': 'bar'}}),
]*{0}
""".format(int(count/6)) # There are already 6 items

    statement = "search('person.name = Mike', values)"

    run_perf_test(iterations, count, setup_str, statement)
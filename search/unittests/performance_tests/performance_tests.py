# unittests/performance_tests/performance_tests.py

from __future__ import print_function

import logging
import timeit

logger = logging.getLogger(__name__)

from .. import test
from ...query import Query

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
    logger.info("{0: >25}: {1:,.2f} ms".format('total time', total_time))
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
    iterations = 100000

    total_time = timeit.timeit(
        """q(values)""",
        setup="""from search.query import Query; q = Query('foo=bar'); values=[
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {'name': 'Mike', 'fo0d': 'bar'},
        ]""",
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test(logger)
def execution_performance_medium_test():
    iterations = 1000
    count = 200

    total_time = timeit.timeit(
        """q(values)""",
        setup="""from search.query import Query; q = Query('foo=bar');  values=[
        {{'x': 1, 'y': 2, 'foo': 3}},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {{'name': 'Mike', 'fo0d': 'bar'}},
        ]*{0}""".format(count),
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,}".format('Total items', count*6))
    logger.info("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test(logger)
def execution_performance_large_test():
    iterations = 10
    count = 600000/6

    total_time = timeit.timeit(
        """try:
    q(values)
except Exception as e:
    print(e)""",
        setup="""from search.query import Query; q = Query('foo=bar');  values=[
        {{'x': 1, 'y': 2, 'foo': 3}},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        {{'name': 'Mike', 'fo0d': 'bar'}},
        ]*{0}""".format(int(count)),
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,}".format('Total items', count))
    logger.info("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test(logger)
def execution_performance_large_TestObject_test():
    iterations = 10
    count = 600000/6

    setup_str = """from search.query import Query; from search.unittests.testobject import TestObject; q = Query('foo=bar'); values=[
            TestObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
            TestObject(**dict(x=1, y=2, foo='bar')),
            TestObject(**dict(x='3', y=2, foo='gurp')),
            TestObject(**dict(x=3, y=2, foo='gurp')),
            TestObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
        ]*{0}""".format(int(count))

    total_time = timeit.timeit(
        stmt="q(values)",
        setup=setup_str,
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,}".format('Total items', count))
    logger.info("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))
    

@test(logger)
def execution_performance_large_TestFieldObject_test():
    iterations = 10
    count = 600000/6

    setup_str = """from search.query import Query; from search.unittests.testobject import TestFieldObject; q = Query('foo=bar'); values=[
            TestFieldObject(**{{'x': 1, 'y': 2, 'foo': 3}}),
            TestFieldObject(**dict(x=1, y=2, foo='bar')),
            TestFieldObject(**dict(x='3', y=2, foo='gurp')),
            TestFieldObject(**dict(x=3, y=2, foo='gurp')),
            TestFieldObject(**{{'name': 'Mike', 'fo0d': 'bar'}}),
        ]*{0}""".format(int(count))

    total_time = timeit.timeit(
        stmt="q(values)",
        setup=setup_str,
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,}".format('Total items', count))
    logger.info("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))
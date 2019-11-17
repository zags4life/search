# unittests/performance_tests/performance_tests.py

from __future__ import print_function

import logging
import timeit

logger = logging.getLogger(__name__)

from .. import test
from ...query import Query

@test
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

    print("{0: >25}: {1:,}".format('Total iterations', iterations))
    print("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    print("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test
def compile_performance_test():
    iterations = 20000

    total_time = timeit.timeit(
        "Query('foo=bar')",
        setup="from search.query import Query",
        number=iterations) * 1000

    print("{0: >25}: {1:,}".format('Total iterations', iterations))
    print("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    print("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test
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

    print("{0: >25}: {1:,}".format('Total iterations', iterations))
    print("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    print("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test
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

    print("{0: >25}: {1:,}".format('Total iterations', iterations))
    print("{0: >25}: {1:,}".format('Total items', count*6))
    print("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    print("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))

@test
def execution_performance_large_test():
    iterations = 10
    count = 600000

    total_time = timeit.timeit(
        """q(values)""",
        setup="""from search.query import Query; q = Query('foo=bar');  values=[
        {{'x': 1, 'y': 2, 'foo': 3}},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        {{'name': 'Mike', 'fo0d': 'bar'}},
        ]*{0}""".format(int(count/6)),
        number=iterations) * 1000

    print("{0: >25}: {1:,}".format('Total iterations', iterations))
    print("{0: >25}: {1:,}".format('Total items', count))
    print("{0: >25}: {1:,.2f} secs".format('total time', total_time/1000))
    print("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))
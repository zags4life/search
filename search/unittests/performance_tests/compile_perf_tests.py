# compile_perf_tests.py

import timeit

from . import logger
from .. import test


@test(logger)
def basic_compile_perf_test():
    iterations = 20000

    total_time = timeit.timeit(
        "Query('foo=bar')",
        setup="from search.query import Query",
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))
    

@test(logger)
def basic_compile_perf_test():
    iterations = 20000

    total_time = timeit.timeit(
        "Query('foo=bar and (!(foo like bar or x) or name ='Tom')",
        setup="from search.query import Query",
        number=iterations) * 1000

    logger.info("{0: >25}: {1:,}".format('Total iterations', iterations))
    logger.info("{0: >25}: {1:,.2f} ms".format('total time', total_time))
    logger.info("{0: >25}: {1:,.4f} ms".format('time per iteration', total_time/iterations))
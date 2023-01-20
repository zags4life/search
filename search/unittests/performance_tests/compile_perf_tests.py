# compile_perf_tests.py
import timeit

from .. import test

ITERATIONS = 10000
PADDING = len('time per iteration')

@test
def perf_basic_compile_test():
    total_time = timeit.timeit(
        "Query('foo=bar')",
        setup="from search.query import Query",
        number=ITERATIONS) * 1000

    _log_results(total_time)


@test
def perf_complex_compile_test():
    total_time = timeit.timeit(
        "Query(\"foo=bar and (!(foo like bar or x) or name ='Tom')\")",
        setup="from search.query import Query",
        number=ITERATIONS) * 1000
    _log_results(total_time)


def _log_results(total_time):
    suffix = 'ms'
    iter_suffix = 'ms'
    total_time_per_iter = total_time / ITERATIONS
    
    if total_time_per_iter > 1000:
        total_time_per_iter /= 1000
        total_time_per_iter_str_suffix = 'secs'
    
    if total_time > 1000:
        total_time /= 1000
        suffix = 'secs'
    total_time_str = f'{total_time:,.2f} {suffix}'
    total_time_per_iter_str = f'{total_time_per_iter:,.4f} {iter_suffix}'
    
    logger.info(f"{'Total Iterations':>{PADDING}}: {ITERATIONS:>15,}")
    logger.info(f"{'total time':>{PADDING}}: {total_time_str:>15}")
    logger.info(f"{'time per iteration':>{PADDING}}: {total_time_per_iter_str:>15}")
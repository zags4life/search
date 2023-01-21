# execution_perf_tests.py
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


@test
def perf_execution_equality_and_equality_test():
    iterations = 10000
    count = 1

    run_perf_test(
        iterations,
        count * 6,
        setup=BUILTIN_OBJECT_SETUP.format(count),
        statement=BUILTIN_STATEMENT.format(count)
    )

@test
def perf_execution_equality_and_equality_medium_test():
    iterations = 100
    count = 1000

    run_perf_test(
        iterations,
        count * 6,
        setup=BUILTIN_OBJECT_SETUP.format(count),
        statement=BUILTIN_STATEMENT.format(count)
    )

@test
def perf_execution_equality_and_equality_large_test():
    iterations = 100
    count = 100000

    run_perf_test(
        iterations,
        count * 6,
        setup=BUILTIN_OBJECT_SETUP.format(count),
        statement=BUILTIN_STATEMENT.format(count)
    )
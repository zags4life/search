# utils.py
import logging

from search import search

from .. import TestObject


logger = logging.getLogger(__name__)


def log_results(expected, actual):
    logger.debug('Found results:')
    for result in actual:
        logger.debug(f'    {result}')

    logger.debug('Expected results:')
    for result in expected:
        logger.debug(f'    {result}')


def results_are_equal(lhs, rhs):
    if type(lhs) != type(rhs):
        return False

    if isinstance(lhs, TestObject):
        return TestObject.is_equal(lhs, rhs)
    return lhs == rhs


def validate_results(expected, actual):
    log_results(expected, actual)

    assert len(actual) == len(expected), \
        f'Incorrect number of results.  ' \
        f'Expected: {len(expected)}  Actual: {len(actual)}'

    matches = []

    for expected_result in expected:
        match = True
        for result in actual:
            # if expected_result == result:
            if results_are_equal(expected_result, result):
                break
        else:
            match &= False

        matches.append((expected_result, match))

    # Assert all expected results were found in results
    assert all(m[1] for m in matches), \
        f'Unexpected search results:' \
        f"{' '.join([f'{er} - found {found}' for er, found in matches if not found])}"


def run_unittest_and_verify_results(query_str, values, expected_results):
    '''Runs a query using the provided query string and value collection, then
    validates the results against the expected results collection.  An 
    AssertionError is raised if the test fails
    
    Parameters:
    query_str - a string representing the query
    values - a collection of values to search
    expected_results - a collection of expected values to validate against the
        results returned by *query*
    '''
    results = search(query_str, values)
    validate_results(expected_results, results)
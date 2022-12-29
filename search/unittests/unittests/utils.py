# utils.py
import logging

from search import search

from .. import TestObject


logger = logging.getLogger(__name__)


def log_results(expected, actual):
    '''Log results, at debug log level.  This method will first log the 
    'actual' set, then the 'expected' set.
    
    Parameters:
        expected - the expected set of values
        actual - the actual set of values
        
    Returns - None
    '''
    logger.debug('Found results:')
    for result in actual:
        logger.debug(f'    {result}')

    logger.debug('Expected results:')
    for result in expected:
        logger.debug(f'    {result}')


def results_are_equal(object1, object2):
    '''Validates that two objects are equal.  If the two objects are equal, 
    return True; otherwise False.
    '''
    # Validate the two objects are the same type
    if type(object1) != type(object2):
        return False

    # if object1 is a TestObject, use TestObject's is_equal method to validate
    # that object1 == object2. If object1 is _not_ a TestObject, default to the
    # built-in equality operator.
    if isinstance(object1, TestObject):
        return TestObject.is_equal(object1, object2)
    return object1 == object2


def validate_results(expected, actual):
    '''Validate two sets are the same.  If they are not, an AssertionError is
    raised.
    
    Parameters:
        expected - the expected set of values
        actual - the actual set of values
    '''
    
    # Log the results
    log_results(expected, actual)

    # Validate the two sets are the same length
    assert len(actual) == len(expected), \
        f'Incorrect number of results.  ' \
        f'Expected: {len(expected)}  Actual: {len(actual)}'

    # Iterate through the collection of expected values.  For each expected 
    # value, iterate through the collection of actual values, comparing each
    # actual value to the expected value.  Then store the expected value
    # and a boolean indicating whether is it a match.
    matches = []
    for expected_result in expected:
        is_match = True
        for result in actual:
            if results_are_equal(expected_result, result):
                break
        else:
            # If we get through the list without breaking, no match was found
            is_match = False
        
        # Store the expected result and a bool indicating whether a match in 
        # the `actual` collection was found.
        matches.append((expected_result, is_match))

    # Assert all expected results were found in the `actual` collection.
    assert all(is_match for _, is_match in matches), \
        f'Missing expected search result: ' \
        f"{' '.join([f'{v}' for v, m in matches if not m])}"


def run_unittest_and_verify_results(query_str, values, expected_values):
    '''Runs a query using the provided query string and value collection, then
    validates the results against the expected results collection.  An 
    AssertionError is raised if the test fails
    
    Parameters:
    query_str - a string representing the query
    values - a collection of values to search
    expected_values - a collection of expected values to validate against the
        results returned by *query*
    '''
    results = search(query_str, values)
    validate_results(expected_values, results)
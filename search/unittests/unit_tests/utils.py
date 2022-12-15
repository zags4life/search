# utils.py

import logging

logger = logging.getLogger(__name__)

def log_results(expected, actual):
    logger.debug('Found results:')
    for result in actual:
        logger.debug(f'    {result}')

    logger.debug('Expected results:')
    for result in expected:
        logger.debug(f'    {result}')


def validate_results(expected, actual):
    log_results(expected, actual)

    assert len(actual) == len(expected), \
        f'Incorrect number of results.  ' \
        f'Expected: {len(expected)}  Actual: {len(actual)}'

    matches = []

    for expected_result in expected:
        match = True
        for result in actual:
            if expected_result == result:
                break
        else:
            match &= False

        matches.append((expected_result, match))

    # Assert all expected results were found in results
    assert all(m[1] for m in matches), \
        f'Unexpected search results:' \
        f"{' '.join([f'{er} - found {found}' for er, found in matches if not found])}"
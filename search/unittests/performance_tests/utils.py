# utils.py

import timeit

from . import logger

def run_perf_test(iterations, count, setup, statement) -> None:
    '''Run a performance test

    Parameters:
    iterations - an int representing the number of iterations to run
    count - The number of items in the list
    setup - The setup statement, used to setup to test
    statement - The statement to execute the test
    '''
    logger.info(f"{'Total iterations':>25}: {iterations:>10,}")
    logger.info(f"{'Total items':>25}: {count:>10,}")

    statement = _wrap_cmd(statement)
    setup = _wrap_cmd(setup)

    total_time = timeit.timeit(
        stmt=statement,
        setup=setup,
        number=iterations)

    avg_time = (total_time * 1000) / iterations
    suffix = 'ms'

    if avg_time > 1000:
        avg_time /= 1000
        suffix = 'secs'

    logger.info(f"{'Avg time': >25}: {avg_time:>10,.4f} {suffix}")

def _wrap_cmd(cmd):
    '''Helper method that wraps any command in a try/catch block'''
    lines = cmd.strip().split('\n')
    lines = [' ' * 4 + line for line in lines]
    lines.insert(0, 'try:')
    lines.append('except Exception as e:')
    lines.append('    raise')
    return '\n'.join(lines)
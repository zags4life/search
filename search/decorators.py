# decorators.py
from datetime import datetime
from functools import wraps


STACKDEPTH = 0

PRINT_STACK_VALUES = False

def show_stack_values(enable):
    global PRINT_STACK_VALUES
    PRINT_STACK_VALUES = enable


def stacktrace(logger):
    '''Decorator that will log when the method is first called and when it
    exits.  The output will be indented based on the depth of the stack.
    '''
    def decorator(func):
        def print_stack(self, values, *args, **kwargs):
            global STACKDEPTH
            global PRINT_STACK_VALUES
            
            results = None
            try:
                start_time = datetime.now()
                logger.debug(f"{' ' * (4 * STACKDEPTH)}>>> {self}")

                if PRINT_STACK_VALUES:
                    for result in values:
                        logger.debug(f"{' ' * (4 * (STACKDEPTH+1))}- {result}")

                STACKDEPTH += 1
                results = func(self, values, *args, **kwargs)
                return results
            finally:
                STACKDEPTH -= 1
                logger.debug(
                    f"{' ' * (4 * STACKDEPTH)}<<< {self} "
                    f"({datetime.now() - start_time})"
                )

                if PRINT_STACK_VALUES:
                    if not results:
                        logger.debug(f"{' ' * (4 * (STACKDEPTH+1))}* No Results *")
                    else:
                        for result in results:
                            logger.debug(f"{' ' * (4 * (STACKDEPTH+1))}+ {result}")
            return results

        @wraps(func)
        def wrapper(*args, **kwargs):
            return print_stack(*args, **kwargs)
        return wrapper if __debug__ else func
    return decorator


def validate_query(func):
    def _validate(query_str):
        stack = []
        try:
            for c in query_str:
                if c == '(':
                    stack.append(c)
                elif c == ')':
                    stack.pop(-1)
        except IndexError:
            raise InvalidQueryError('Unbalanced parenthesis')

        if len(stack) != 0:
            raise InvalidQueryError('Unbalanced parenthesis')

    def wrapper(query_str, *args, **kwargs):
        _validate(query_str)
        return func(query_str, *args, **kwargs)
    return wrapper
# decorators.py
from datetime import datetime
from functools import wraps
import time


STACKDEPTH = 0

PRINT_STACK_VALUES = False

def show_stack_values(enable):
    '''Enables / disables the ability to view values being passed into, results
    from, condition objects.  This augments the `stacktrace` decorator, used to
    trace how conditions are called.  Note:  this feature is only supported 
    when debug logging is enabled AND python is not optimized (`-O`).
    
    Parameters:
        enable - a boolean indicating whether to enable or disable this feature
    '''
    global PRINT_STACK_VALUES
    PRINT_STACK_VALUES = enable


def stacktrace(logger):
    '''Decorator that will log when the method is first called and when it
    exits.  The output will be indented based on the depth of the stack.
    '''
    def decorator(func):
        def print_stack(self, values, *args, **kwargs):
            global STACKDEPTH, PRINT_STACK_VALUES
            
            results = None
            try:
                start_time = time.time()
                padding = ' ' * (4 * STACKDEPTH)
                logger.debug(f"{padding}>>> {self}")


                STACKDEPTH += 1
                
                if PRINT_STACK_VALUES:
                    padding = ' ' * (4 * STACKDEPTH)
                    logger.debug(f'{padding}Input set:')
                    for result in values:
                        logger.debug(f"{padding}- {result}")

                results = func(self, values, *args, **kwargs)
                return results
            finally:
                padding = f"{' ' * (4 * STACKDEPTH)}"
                if PRINT_STACK_VALUES:
                    logger.debug(f'{padding}Resultant set:')
                    if not results:
                        logger.debug(f"{padding}* No Results *")
                    else:
                        for result in results:
                            logger.debug(f"{padding}+ {result}")
                    logger.debug(f"{padding}Elapse time: {time.time() - start_time:,.4f}")

                STACKDEPTH -= 1
                padding = ' ' * (4 * STACKDEPTH)
                logger.debug(f"{padding}<<< {self} ")
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
# decorators.py
from datetime import datetime
from functools import wraps


STACKDEPTH = 0


def stacktrace(logger):
    '''Decorator that will log when the method is first called and when it
    exits.  The output will be indented based on the depth of the stack.
    '''
    def decorator(func):
        def print_stack(self, values, *args, **kwargs):
            global STACKDEPTH
            results = None
            try:
                if STACKDEPTH == 0:
                    for result in values:
                        logger.debug(f"  {result}")
            
                start_time = datetime.now()
                logger.debug(f"{' ' * (4 * STACKDEPTH)}>>> {self}")

                STACKDEPTH += 1
                results = func(self, values, *args, **kwargs)
                
                return results
            finally:
                STACKDEPTH -= 1

                logger.debug(
                    f"{' ' * (4 * STACKDEPTH)}<<< {self} "
                    f"({datetime.now() - start_time})"
                )
                
                for result in results:
                    logger.debug(f"{' ' * (4 * (STACKDEPTH))}  {result}")
            return results

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) if not __debug__ \
                else print_stack(*args, **kwargs)
        return wrapper
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
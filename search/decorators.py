# decorators.py
from datetime import datetime
from functools import wraps


STACKDEPTH = 0


def stacktrace(logger):
    def decorator(func):
        def print_stack(self, *args, **kwargs):
            global STACKDEPTH

            try:
                start_time = datetime.now()
                logger.debug(f"{' ' * (4 * STACKDEPTH)}>>> {self}")

                STACKDEPTH += 1
                return func(self, *args, **kwargs)
            finally:
                STACKDEPTH -= 1
                
                logger.debug(
                    f"{' ' * (4 * STACKDEPTH)}<<< {self} "
                    f"({datetime.now() - start_time})"
                )

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return print_stack(self, *args, **kwargs)
        return wrapper
    return decorator
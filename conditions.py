# condition.py

from abc import ABC, abstractmethod
import logging

from .fields import QueryField

stackdepth = 0

logger = logging.getLogger(__name__)

def stacktrace(func):
    def print_stack(self, *args, **kwargs):
        global stackdepth

        try:
            logger.debug('{0}{1} {2}'.format('    ' * stackdepth, '>>>', str(self)))

            stackdepth += 1
            return func(self, *args, **kwargs)
        finally:
            stackdepth -= 1
            logger.debug('{0}{1} {2}'.format('    ' * stackdepth, '<<<', str(self)))

    def wrapper(self, *args, **kwargs):
        if __debug__:
            return print_stack(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

class Condition(ABC):
    '''An ABC for all search conditions'''

    @abstractmethod
    def __call__(self, values):
        pass

#################################################
# Logic Statements
#################################################

class NotStatement(Condition):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    @stacktrace
    def __call__(self, values):
        return values - (values & self.condition(values))

    def __str__(self):
        return '[NOT {0.condition}]'.format(self)

class AndStatement(Condition):
    def __init__(self, c1, c2):
        super().__init__()
        self.condition1 = c1
        self.condition2 = c2

    @stacktrace
    def __call__(self, values):
        return self.condition1(values) & self.condition2(values)

    def __str__(self):
        return "[{0.condition1} AND {0.condition2}]".format(self)

class OrStatement(Condition):
    def __init__(self, c1, c2):
        super().__init__()
        self.condition1 = c1
        self.condition2 = c2

    @stacktrace
    def __call__(self, values):
        return self.condition1(values) | self.condition2(values)

    def __str__(self):
        return "[{0.condition1} OR {0.condition2}]".format(self)


#################################################
# Arithmetic Expressions
#################################################

class Expression(Condition):
    OPERATOR = None

    def __init__(self, lhs, rhs):
        super().__init__()

        self.field = QueryField(lhs, rhs)

    def __str__(self):
        assert self.__class__.OPERATOR
        return '({} {} {})'.format(
            self.field.name,
            self.__class__.OPERATOR,
            self.field.value)

    def __repr__(self):
        return '{}: "{}"'.format(self.__class__.__name__, str(self))

    @classmethod
    def _get_values(cls, values, search_func):
        '''Returns a set of values which match search_func

        parameters:
            values - values to search_func
            search_func - a function used for comparision of the values
        '''
        results = set()
        for value in values:
            if search_func(value):
                results.add(value)
        return results

class EqualExpression(Expression):
    OPERATOR = '='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f == self.field for f in v.fields))

class NotEqualExpression(Expression):
    OPERATOR = '!='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f != self.field for f in v.fields))

class LikeExpression(Expression):
    OPERATOR = 'LIKE'

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f.match(self.field) for f in v.fields))

class LessThanExpression(Expression):
    OPERATOR = '<'

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f < self.field for f in v.fields))

class LessThanOrEqualExpression(Expression):
    OPERATOR = '<='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f <= self.field for f in v.fields))

class GreaterThanExpression(Expression):
    OPERATOR = '>'

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f > self.field for f in v.fields))

class GreaterThanOrEqualExpression(Expression):
    OPERATOR = '>='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            search_func=lambda v: any(f >= self.field for f in v.fields))


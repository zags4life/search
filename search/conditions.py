# condition.py

from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging
import operator
from six import with_metaclass

from .fields import QueryField

stackdepth = 0

logger = logging.getLogger(__name__)

def stacktrace(func):
    def print_stack(self, *args, **kwargs):
        global stackdepth

        try:
            start_time = datetime.now()
            logger.debug('{0}{1} {2}'.format('    ' * stackdepth, '>>>', str(self)))

            stackdepth += 1
            return func(self, *args, **kwargs)
        finally:
            stackdepth -= 1
            logger.debug('{0}{1} {2} ({3})'.format(
                    '    ' * stackdepth,
                    '<<<',
                    str(self),
                    (datetime.now() - start_time)
                )
            )

    def wrapper(self, *args, **kwargs):
        if __debug__:
            return print_stack(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

class Condition(with_metaclass(ABCMeta, object)):
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
        super(AndStatement, self).__init__()
        self.condition1 = c1
        self.condition2 = c2

    @stacktrace
    def __call__(self, values):
        return self.condition1(values) & self.condition2(values)

    def __str__(self):
        return "[{0.condition1} AND {0.condition2}]".format(self)

class OrStatement(Condition):
    def __init__(self, c1, c2):
        super(OrStatement, self).__init__()
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
        super(Expression, self).__init__()
        self.field = QueryField(lhs, rhs)

    def __str__(self):
        assert self.__class__.OPERATOR
        return '({} {} {})'.format(
            self.field.name,
            self.__class__.OPERATOR,
            self.field.value)

    def __repr__(self):
        return '{}: "{}"'.format(self.__class__.__name__, str(self))

    def _get_values(self, values, op):
        '''Returns a set of values which match search_func

        parameters:
            values - values to search_func
            op - the operator function used to compare each field
        '''

        def check(v):
            for field in v.fields:
                if op(field, self.field):
                    return True
            return False

        results = set()
        for value in values:
            if check(value):
                results.add(value)
        return results

class EqualExpression(Expression):
    OPERATOR = '='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.eq
        )

class NotEqualExpression(Expression):
    OPERATOR = '!='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.ne
        )

class LikeExpression(Expression):
    OPERATOR = 'LIKE'

    @stacktrace
    def __call__(self, values):
        def like(lhs, rhs):
            return lhs.match(rhs)

        return self._get_values(
            values=values,
            op=like
        )

class LessThanExpression(Expression):
    OPERATOR = '<'

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.lt
        )

class LessThanOrEqualExpression(Expression):
    OPERATOR = '<='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.le
         )

class GreaterThanExpression(Expression):
    OPERATOR = '>'

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.gt
        )

class GreaterThanOrEqualExpression(Expression):
    OPERATOR = '>='

    @stacktrace
    def __call__(self, values):
        return self._get_values(
            values=values,
            op=operator.ge
        )
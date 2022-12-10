# condition.py

from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging
import operator
from six import with_metaclass

from .fields import QueryField

STACKDEPTH = 0

logger = logging.getLogger(__name__)

def stacktrace(func):
    def print_stack(self, *args, **kwargs):
        global STACKDEPTH

        try:
            start_time = datetime.now()
            logger.debug('{0}{1} {2}'.format('    ' * STACKDEPTH, '>>>', str(self)))

            STACKDEPTH += 1
            return func(self, *args, **kwargs)
        finally:
            STACKDEPTH -= 1
            logger.debug('{0}{1} {2} ({3})'.format(
                    '    ' * STACKDEPTH,
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
    '''Logical NOT statement.  This class will NOT a condition, returning a
    set of items that do not match the condition
    '''
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    @stacktrace
    def __call__(self, values):
        return values - (values & self.condition(values))

    def __str__(self):
        return '[NOT {0.condition}]'.format(self)


class AndStatement(Condition):
    '''Logical AND statement.  This class will AND two sets (conditions) together'''
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
    '''Logical OR statement.  This class will OR two sets (conditions) together'''
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
    EXPRESSION_NAME = None

    def __init__(self, lhs, rhs):
        super(Expression, self).__init__()
        self.field = QueryField(lhs, rhs)

    def __call__(self, values):
        '''Returns a set of values which match search_func

        parameters:
            values - values to search_func
        '''

        def check(v):
            for field in v.fields:
                if self.OPERATOR(field, self.field):
                    return True
            return False

        results = set()
        for value in values:
            if check(value):
                results.add(value)
        return results

    def __str__(self):
        assert self.__class__.EXPRESSION_NAME
        return '({} {} {})'.format(
            self.field.name,
            self.__class__.EXPRESSION_NAME,
            self.field.value)

    def __repr__(self):
        return '{}: "{}"'.format(self.__class__.__name__, str(self))


class EqualExpression(Expression):
    EXPRESSION_NAME = '='
    OPERATOR = operator.eq


class NotEqualExpression(Expression):
    EXPRESSION_NAME = '!='
    OPERATOR = operator.ne


class LikeExpression(Expression):
    EXPRESSION_NAME = 'LIKE'

    @staticmethod
    def like(lhs, rhs):
        return lhs.match(rhs)
    OPERATOR = like


class LessThanExpression(Expression):
    EXPRESSION_NAME = '<'
    OPERATOR = operator.lt

class LessThanOrEqualExpression(Expression):
    EXPRESSION_NAME = '<='
    OPERATOR = operator.le


class GreaterThanExpression(Expression):
    EXPRESSION_NAME = '>'
    OPERATOR = operator.gt


class GreaterThanOrEqualExpression(Expression):
    EXPRESSION_NAME = '>='
    OPERATOR = operator.gt
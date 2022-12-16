# condition.py

from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging
import operator
from six import with_metaclass
import re

from .decorators import stacktrace
from .field import Field

logger = logging.getLogger(__name__)

#################################################
# Base class
#################################################

class Condition(with_metaclass(ABCMeta, object)):
    '''An ABC for all search conditions'''

    @abstractmethod
    def __call__(self, values):
        pass


#################################################
# Logical Conditions
#################################################

class NotStatement(Condition):
    '''Logical NOT statement.  This class will NOT a condition, returning a
    set of items that do not match the condition
    '''
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    @stacktrace(logger)
    def __call__(self, values):
        return values - (values & self.condition(values))

    def __str__(self):
        return f'[NOT {self.condition}]'


class AndStatement(Condition):
    '''Logical AND statement.  This class will AND two sets (conditions) together'''
    def __init__(self, c1, c2):
        super(AndStatement, self).__init__()
        self.condition1 = c1
        self.condition2 = c2

    @stacktrace(logger)
    def __call__(self, values):
        return self.condition1(values) & self.condition2(values)

    def __str__(self):
        return f"[{self.condition1} AND {self.condition2}]"


class OrStatement(Condition):
    '''Logical OR statement.  This class will OR two sets (conditions) together'''
    def __init__(self, c1, c2):
        super(OrStatement, self).__init__()
        self.condition1 = c1
        self.condition2 = c2

    @stacktrace(logger)
    def __call__(self, values):
        return self.condition1(values) | self.condition2(values)

    def __str__(self):
        return f"[{self.condition1} OR {self.condition2}]"


#################################################
# Arithmetic Operators
#################################################

class Operator(Condition):
    '''Operator base class that will perform an arithmetic comparision 
    like '=', '!=', '<', etc
    '''
    OPERATOR_NAME = None # Used by __str__
    OPERATOR = None      # a function defined by child classes

    def __init__(self, lhs, rhs):
        super(Operator, self).__init__()
        self.field = Field(lhs, rhs)

    @stacktrace(logger)
    def __call__(self, values):
        return self._get_values(values)

    def _get_values(self, values):
        '''Returns a set of values which match search_func

        parameters:
            values - a list of values to evaluate
        '''
        def _check(val):
            '''Check the value'''
            instance_fields = val.__dict__ if not isinstance(val, dict) else val
            property_fields = {}

            # If val is not a dict, update property_fields
            if not isinstance(val, dict):
                property_fields = {
                    k: getattr(val, k)
                    for k, v in val.__class__.__dict__.items()
                    if type(v) is property
                }

            # Iterate through all instance and property fields
            for fields in [instance_fields, property_fields]:
                assert isinstance(fields, dict), \
                    f'Unexpected field type: Expected: {type(dict)}, Actual: {type(fields)}'

                for k, v in fields.items():
                    # Is the field name match the key.  If True,
                    # Convert the search field to the same type as value,
                    # then apply the operator
                    if re.search(self.field.name, k):
                        with self.field.convert_type(v) as field_value:
                            if self.OPERATOR(v, field_value):
                                return True
            return False

        results = set()
        for value in values:
            if _check(value):
                results.add(value)
        return results

    def __str__(self):
        assert self.__class__.OPERATOR_NAME, \
            f'{self.__class__.__name__} does not implement OPERATOR_NAME'
        return f'({self.field.name} {self.__class__.OPERATOR_NAME} ' \
            f'{self.field.value})'

    def __repr__(self):
        return f'{self.__class__.__name__}: "{self}"'


class EqualOperator(Operator):
    OPERATOR_NAME = '='
    OPERATOR = operator.eq


class NotEqualOperator(Operator):
    OPERATOR_NAME = '!='
    OPERATOR = operator.ne


class LikeOperator(Operator):
    OPERATOR_NAME = 'LIKE'

    @staticmethod
    def like(lhs, rhs):
        return rhs and re.search(rhs, str(lhs))
    OPERATOR = like


class LessThanOperator(Operator):
    OPERATOR_NAME = '<'
    OPERATOR = operator.lt

class LessThanOrEqualOperator(Operator):
    OPERATOR_NAME = '<='
    OPERATOR = operator.le


class GreaterThanOperator(Operator):
    OPERATOR_NAME = '>'
    OPERATOR = operator.gt


class GreaterThanOrEqualOperator(Operator):
    OPERATOR_NAME = '>='
    OPERATOR = operator.ge

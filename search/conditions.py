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
# Logical Statements
#
# Logical statements compare two Expressions
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
# Arithmetic Expressions
#################################################

class Expression(Condition):
    '''Expression base class that will perform an arithmetic comparision 
    like '=', '!=', '<', etc
    '''
    EXPRESSION_NAME = None # Used by __str__
    EXPRESSION = None      # a function defined by child classes

    def __init__(self, name, value):
        '''Base class for all expressions.  It is expected that this class is
        subclassed.
        
        Parameters:
        name - the name of the field to find
        value - the value of the field to find
        '''
        super(Expression, self).__init__()
        self.field = Field(name, value)
        
        assert self.__class__.EXPRESSION, \
            f'{self.__class__.__name__} does not implement EXPRESSION'
        assert self.__class__.EXPRESSION_NAME, \
            f'{self.__class__.__name__} does not implement EXPRESSION_NAME'

    @stacktrace(logger)
    def __call__(self, values):
        '''Returns a set of values which match search criteria

        parameters:
            values - a list of values to evaluate
        returns - results subset of values
        '''
        results = set()
        for value in values:
            if self._convert_type_and_compare_value(value):
                results.add(value)
        return results

    def _convert_type_and_compare_value(self, value):
        '''Check the value'''
        instance_fields = value.__dict__ if not isinstance(value, dict) else value
        property_fields = {}

        # If value is not a dict, update property_fields
        if not isinstance(value, dict):
            property_fields = {
                k: getattr(value, k)
                for k, v in value.__class__.__dict__.items()
                if type(v) is property
            }

        # Iterate through all instance and property fields
        for fields in [instance_fields, property_fields]:
            assert isinstance(fields, dict), \
                f'Unexpected field type: Expected: {type(dict)}, Actual: {type(fields)}'

            for field_name, v in fields.items():
                # Is the field name match the key.  If True,
                # Convert the search field to the same type as value,
                # then apply the operator
                if re.search(self.field.name, field_name) is not None:
                    with self.field.convert_type(v) as field_value:
                        if self.EXPRESSION(v, field_value):
                            return True
        return False

    def __str__(self):
        return f'({self.field.name} {self.__class__.EXPRESSION_NAME} ' \
            f'{self.field.value})'

    def __repr__(self):
        return f'{self.__class__.__name__}: "{self}"'


class AnyExpression(Expression):
    '''Any expression allows for finding objects whose fields are a name 
    match only.
    '''
    EXPRESSION_NAME = 'ANY'

    def __init__(self, name):
        # Ensure name is in the format '^name$'
        name = name if name.startswith('^') else '^' + name
        name = name if name.endswith('$') else name + '$'
        super(AnyExpression, self).__init__(name, '.*')

    def operator_any(*args):
        return True
    EXPRESSION = operator_any


class EqualExpression(Expression):
    '''Equality expression that validates any element whose name is a 
    match (regular expression), the elements value equals the field's value, as
    the same type as the element value (which will require type conversion).
    '''
    EXPRESSION_NAME = '='
    EXPRESSION = operator.eq


class GreaterThanExpression(Expression):
    '''Greater than expression that validates any element whose name is a 
    match (regular expression), the elements value is greater than the field's 
    value, as the same type as the element value (which will require automatic
    type conversion).
    '''
    EXPRESSION_NAME = '>'
    EXPRESSION = operator.gt


class GreaterThanOrEqualExpression(Expression):
    '''Greater than or equal to expression that validates any element whose name
    is a match (regular expression), the elements value is greater than or 
    equal to the field's value, as the same type as the element value (which will 
    require automatic type).
    '''
    EXPRESSION_NAME = '>='
    EXPRESSION = operator.ge


class LessThanExpression(Expression):
    '''Greater than expression that validates any element whose name is a 
    match (regular expression), the elements value is less than the 
    the field's value, as the same type as the element value (which will 
    require automatic type).
    '''
    EXPRESSION_NAME = '<'
    EXPRESSION = operator.lt
    

class LessThanOrEqualExpression(Expression):
    '''Less than or equal to expression that validates any element whose name
    is a match (regular expression), the elements value is less than or 
    equal to the field's value, as the same type as the element value (which will 
    require automatic type).
    '''
    EXPRESSION_NAME = '<='
    EXPRESSION = operator.le


class LikeExpression(Expression):
    '''String comparison expression, where the field value is treated a 
    regular expression.  Note: Expression will always treat the field name as a
    regular expression.
    '''
    EXPRESSION_NAME = 'LIKE'

    @staticmethod
    def operator_like(name, value):
        return value is not None and re.search(value, str(name)) is not None
    EXPRESSION = operator_like


class NotEqualExpression(Expression):
    '''Inequality expression that validates any element whose name is a 
    match (regular expression), the elements value does not equal the field's
    value, as the same type as the element value (which will require type 
    conversion).
    '''
    EXPRESSION_NAME = '!='
    EXPRESSION = operator.ne
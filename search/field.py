# fields.py
from datetime import date, datetime
import logging
import re

from .exceptions import InvalidQueryError
from .parsers import register_parser, PARSERS

logger = logging.getLogger(__name__)


class Field(object):
    '''Represents a field, containing a name and a value, to be used for
    comparisons.  This class provides helper equality / inequality operator
    to provide a common, unified, interface for comparing unlike objects
    '''
    def __init__(self, name, value):
        assert isinstance(value, str), 'value must be of type str'
        self.name = name
        self.value = self.__cleanup_value(value)

        self.original_name = name
        self.original_value = self.value
        
        if '\.' in self.name or ('\.' not in self.name and '.' in self.name):
            wildcard = r'\.' if '\.' in self.name else '.'
            parts = self.name.split(wildcard)
            self.name = parts[0]
            self.value = type(self)('\.'.join(parts[1:]), self.value)

        self.__name_attr_regex = self.compile_regex(self.name)
        self.__org_name_attr_regex = self.compile_regex(self.original_name)

    @staticmethod
    def compile_regex(regex_str):
        try:
            # Precompile the regular expression for performance improvement.
            return re.compile(regex_str)
        except re.error as e:
            raise InvalidQueryError(f"Invalid regular expression: '{regex_str}'")

    @property
    def is_nested_type(self):
        '''Getter that returns True if the Field represents a nested field,
        otherwise False.
        '''
        return self.name != self.original_name

    def compare_value(self, obj, op_func):
        '''Compares an object against the Field's name and value, using
        the provided op_func.  If the object contains a matching attribute
        name and op_func returns True when comparing Field's value to
        the matching attributes value, this method will return True;
        otherwise False.

        the matching attribute's value

        Parameters:
            obj - The object to compare_value
            op_func - the operator function to use for comparisons, which
                returns True or False. E.g. operator.eq

        Returns - True if the object has an attribute whose name is a match
            and op_func returns True when comparing the matching attribute
            value to this Field object's value attribute.  Otherwise False.
        '''

        # Create a dict of params to pass to __compare_value_helper.
        # This is to allow us to call __compare_value_helper only once
        # but change the parameters if the object is nested or not.
        params = dict(
            obj=obj,
            op_func=op_func,
            regex=self.__name_attr_regex,
            value=self.value
        )

        if self.is_nested_type:
            # There are two paths for nested type:
            # 1) look for child objects matching the child attrs - recursively
            # 2) look for attributes whose names are in the format foo.bar

            _, matching_value = self.__is_matching_attr_name(
                obj,
                self.__name_attr_regex
            )

            # If a matching value is found, recursively test the matching
            # value against the sub-field (as self.value).
            if matching_value and \
                    self.value.compare_value(matching_value, op_func):
                return True

            # If no match was found, compare obj against the original name
            params['regex'] = self.__org_name_attr_regex
            params['value'] = self.original_value

        return self.__compare_value_helper(**params)

    def __str__(self):
        '''Returns a string representation of the object'''
        return f'Field[name={self.name}, value={self.value}]'

    ###########################################################################
    # Class Methods
    ###########################################################################

    @classmethod
    def __compare_value_helper(cls, obj, regex, value, op_func):
        '''Helper class method used for comparing a value

        Parameters:
            obj - the object to compare
            regex - the regular expression to use when comparing attr names
            value - the value to compare, as a string
            op_func - the operator function to use for comparisons, which
                returns True or False. E.g. operator.eq

        Returns - True if the object has an attribute whose name is a match
            and op_func returns True when comparing the matching attribute
            value to this Field object's value attribute.  Otherwise False.
        '''
        _, matching_value = cls.__is_matching_attr_name(obj, regex)

        # If the obj has a matching name or the value is a special case
        #
        # Special cases:
        # 1) the value we are looking for is None
        # 2) the value we are looking for is empty string
        #
        if (matching_value
                or matching_value is None and value in ('None', '.*')
                or matching_value == '' and value in ('', '.*')):

            return op_func(
                matching_value, 
                cls.__convert_type(type(matching_value), value)
            )
        return False

    ###########################################################################
    # Static Methods
    ###########################################################################

    @staticmethod
    def __cleanup_value(value:str):
        '''Strip out unwanted characters'''
        value = value.replace('"', '')
        value = value.replace("'", '')
        value = value.strip()
        return value

    @staticmethod
    def __convert_type(_type:type, value:str):
        '''Converts str_value (which is always a string) to the same type as
        value.  If self.value is successfully converted, the converted value is
        return; otherwise None.

        Parameters:
            _type - the type to convert 'value' to
            value - the value, as a string, to convert

        Returns - the converted value is successful; otherwise None
        '''
        try:
            if _type in PARSERS:
                return PARSERS[_type](value)
            else:
                return _type(value)
        except Exception:
            pass
        return None

    @staticmethod
    def __is_matching_attr_name(other, regex):
        '''This method determines if 'other' contains an attribute that matches
        regex. This method will first extract all public attributes and 
        properties from the 'other' object, then compares the attributes names
        to regex using a precompiled regular expression.  If an attribute
        is a match the attributes value is returned to the caller.

        Parameters
            other - the object to compare_value
            regex - the regular expression to use when comparing attr names

        Returns - the matching attributes value if other contains a matching
            attribute, otherwise False.
        '''
        # Get all the attributes.
        # Note: We are _not_ using `inspect` for better performance.
        try:
            attributes = {
                k:v for k, v in other.__dict__.items() if not k.startswith('_')
            } if not isinstance(other, dict) else other

            # If value is not a dict, update property_attributes
            if not isinstance(other, dict):
                attributes.update({
                    k: getattr(other, k)
                    for k, v in other.__class__.__dict__.items()
                    if type(v) is property
                })

            # Iterate through all attributes from obj and verify if an
            # attribute matches the fields name or fully qualified name (in
            # the case were the two are different).
            for attr_name, attr_value in attributes.items():
                if regex.search(attr_name):
                    return attr_name, attr_value
        except AttributeError:
            pass
        return False, False
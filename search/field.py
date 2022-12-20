# fields.py
from datetime import date, datetime
import logging
import re

import inspect


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

        # Precompile the regular expression for performance improvement.
        self.__regex = re.compile(self.name)

    def compare_value(self, field, op_func):
        '''Compares an object against the Field's name and value, using
        the provided op_func.  If the object contains a matching attribute
        name and op_func returns True when comparing Field's value to 
        the matching attributes value, this method will return True;  
        otherwise False.
        
        the matching attribute's value 
 
        Parameters:
            field - The object to compare_value
            op_func - the operator function to use for comparisons, which
                returns True or False. E.g. operator.eq
        
        Returns - True if the object has an attribute whose name is a match
            and op_func returns True when comparing the matching attribute 
            value to this Field object's value attribute.  Otherwise False.
        '''
        matching_value = self.__is_matching_attr_name(field)
        
        # If the field has a matching name or the value is a special case
        #
        # Special cases:
        # 1) the value we are looking for is None
        # 2) the value we are looking for is empty string
        #
        if (matching_value
            or matching_value is None and self.value == 'None'
            or matching_value == '' and self.value == ''):

            if op_func(matching_value, self.__convert_type(matching_value)):
                return True
        return False
        
    def __is_special_case(self, value):
        '''Determines if the value is a special case;
        Special cases:
          1) the value we are looking for is None
          2) the value we are looking for is empty string
        '''
        return ((value is None and self.value == 'None')
            or (value == '' and self.value == ''))

    def __is_matching_attr_name(self, other):
        '''Determines if 'other' contains an attribute that matches self.name.
        This method will first extract all public attributes and properties
        from the 'other' object, then compares the attributes names to 
        self.name using a precompiled regular expression.  If an attribute
        is a match the attributes value is returned to the caller.
        
        Parameters
            other - the object to compare_value
            
        Returns - the matching attributes value if other contains a matching
            attribute, otherwise False.
        '''
        
        # Get all the attributes.
        # Note: We are _not_ using `inspect` for better performance.
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
        
        # Iterate through all instance and property attributes
        for attr_name, attr_value in attributes.items():
            if self.__regex.search(attr_name):
                return attr_value
        return False

    def __convert_type(self, value):
        '''Converts self.value (which is always a string) to the same type as 
        value.  If self.value is successfully converted, the converted value is
        return; otherwise None.

        Parameters:
            value - the value we need to convert to
            
        Returns - the converted value is successful; otherwise None
        '''

        try:
            # If the value is a date, convert the string value to a date object.
            # Else, convert the string value to the same type as the value
            return (Date(self.value)
                if isinstance(value, (date, datetime))
                else type(value)(str(self.value)))
        except Exception:
            return None

    def __str__(self):
        return f'Field[name={self.name}, value={self.value}]'

    @staticmethod
    def __cleanup_value(value):
        '''Strip out unwanted characters'''
        value = value.replace('"', '')
        value = value.replace("'", '')
        value = value.strip()
        return value


DATE_FORMATS = (
    '%m-%d-%Y',
    '%m-%d-%y',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%m%d%Y',
    '%m%d%y',
    '%m/%d',
    '%m-%d',
    '%m%d',
    '%Y%m%d',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%y%m%d',
)


def Date(date_str):
    '''Parse date in string format into a datetime object'''
    if not date_str:
        return None

    for format in DATE_FORMATS:
        try:
            formatted = datetime.strptime(date_str, format)

            if formatted.year == 1900:
                formatted = datetime(
                    year=datetime.now().year,
                    month=formatted.month,
                    day=formatted.day)
            return formatted.date()
        except ValueError:
            pass

    logger.error("Failed to parse date '{}'".format(date_strs))
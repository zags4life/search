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
        self.name = str(name)
        self.value = value
        
        self.__regex = re.compile(str(name))

    def compare_value(self, field, op_func):
        matching_value = self.__is_match(field)
        if matching_value or (matching_value is None and self.value == "None"):
            converted_value = self.__convert_type(matching_value)
            if op_func(matching_value, converted_value):
                return True
        # elif matching_value is None and self.value == "None":
            # return True
        return False

    def __is_match(self, other):
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
        '''Context manager that attempts to convert the underlying string value
        to the same type as value.  If successful, the converted value will be
        yielded else None is yielded

        Parameters:
        value - the value we need to convert to
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
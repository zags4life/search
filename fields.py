# fields.py

from abc import ABC, abstractproperty
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

DATE_FORMATS = [
    '%m/%d/%y', '%m/%d/%Y',
    '%m%d%y',' %m%d%Y',
    '%m%d', '%m/%d'
]

def Date(date_str):
    for format in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, format)
        except ValueError:
            pass

class SearchFieldDataProvider(ABC):
    @abstractproperty
    def fields(self):
        pass

def verify_name_matches(func):
    '''Decorator which ensures the Field name and QueryField name matches.
    If true, call func, else return False
    '''
    def wrapper(self, other):
        return func(self, other) if re.search(other.name, self.name) else False
    return wrapper

def convert_type(func):
    '''Decorator to convert QueryField value to that of their SearchField value
    counterparts type.

    All QueryField values are initially strings.  We need to convert them to the same type
    as the field we are comparing.  This ensures that proper comparisons occur, i.e.
    comparing integer or decimal values.
    '''
    def wrapper(field, query_field):
        assert (isinstance(query_field, QueryField) and isinstance(field, SearchField)), \
            'Invalid search field: {} - {}'.format(type(field), type(query_field))

        try:
            with query_field:
                return func(field, query_field(field.value))
        except Exception as e:
            # If we cannot convert the type, log the exception and return False
            logger.debug(e)
            logger.debug('{0: >16} {1}'.format('SearchField:', str(field)))
            logger.debug('{0: >16} {1}'.format('QueryField:', str(query_field)))
            return False
    return wrapper

class BaseField(object):
    def __init__(self, name, value):
        self.name = str(name)
        self.value = value

    @verify_name_matches
    @convert_type
    def __eq__(self, other):
        return self.value == other.value

    @verify_name_matches
    @convert_type
    def __ne__(self, other):
        return self.value != other.value

    @verify_name_matches
    @convert_type
    def __lt__(self, other):
        return self.value < other.value

    @verify_name_matches
    @convert_type
    def __le__(self, other):
        return self.value <= other.value

    @verify_name_matches
    @convert_type
    def __gt__(self, other):
        return self.value > other.value

    @verify_name_matches
    @convert_type
    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return '{0.name} = {0.value}'.format(self)
    __repr__ = __str__

    def match(self, other):
        # return True is the field name and value match the other
        # fields name and value.  Otherwise False.
        return (
            re.search(other.name, self.name) and
            re.search(str(other.value), str(self.value))
        )

class SearchField(BaseField):
    '''Represents a searchable field'''
    pass

class QueryField(BaseField):
    '''Represents a query field

    Unlike BaseField, QueryField implements __enter__/__exit__ to allow of
    intermediate type convertion, while ensuring the original value is properly
    rolled back after the operation is complete.
    '''
    def __init__(self, name, value):
        assert isinstance(value, str), 'value must be of type str'
        super().__init__('(?i){}'.format(name), value)

    def __call__(self, value):
        '''Call operator - converts the underlying string value to the appropriate type.'''

        # If the value is a date, convert the string value to a date object.
        # Else, convert the string value to the same type as the value
        if isinstance(value, (date, datetime)):
            self.value = Date(self.value)
        else:
            self.value = type(value)(self.value)
        return self

    def __enter__(self):
        self.__orig_val = self.value
        return self

    def __exit__(self, type, value, tb):
        self.value = self.__orig_val

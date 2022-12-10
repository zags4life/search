# fields.py

from datetime import date, datetime
import logging
import re

logger = logging.getLogger(__name__)

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


class BaseField(object):
    '''Represents a field, containing a name and a value, to be used for
    comparisons.  This class provides helper equality / inequality operator
    to provide a common, unified, interface for comparing unlike objects
    '''
    def __init__(self, name, value):
        self.name = str(name)
        self.value = value


class SearchField(BaseField):
    '''Represents a searchable field'''
    pass


class QueryField(BaseField):
    '''Represents a query field

    Unlike BaseField, QueryField is a context manager to allow of intermediate
    type convertion, while ensuring the original value is properly
    rolled back after the operation is complete.
    '''
    def __init__(self, name, value):
        assert isinstance(value, str), 'value must be of type str'
        super().__init__(name, value)

    def convert_type(self, value):
        '''Call operator - converts the underlying string value to the 
        appropriate type.
        
        Parameters:
        value - the value we need to convert
        
        Returns - True is the value was successfully converted, otherwise False
        '''

        try:
            # If the value is a date, convert the string value to a date object.
            # Else, convert the string value to the same type as the value
            self.value = (Date(self.value) 
                if isinstance(value, (date, datetime)) 
                else type(value)(str(self.value)))
            return True
        except Exception:
            pass
        return False

    def __enter__(self):
        '''When entered, self.value will be cached to be restored when exiting 
        the context manager
        '''
        self.__orig_val = self.value
        return self

    def __exit__(self, *args, **kwargs):
        '''Restore the cached value'''
        self.value = self.__orig_val
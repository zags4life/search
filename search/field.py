# fields.py
from contextlib import contextmanager
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


class Field(object):
    '''Represents a field, containing a name and a value, to be used for
    comparisons.  This class provides helper equality / inequality operator
    to provide a common, unified, interface for comparing unlike objects
    '''
    def __init__(self, name, value):
        assert isinstance(value, str), 'value must be of type str'
        self.name = str(name)
        self.value = value

    @contextmanager
    def convert_type(self, value):
        '''Context manager that attempts to convert the underlying string value
        to the same type as value.  If successful, the converted value will be
        yielded else None is yielded
        
        Parameters:
        value - the value we need to convert to
        '''

        try:
            # If the value is a date, convert the string value to a date object.
            # Else, convert the string value to the same type as the value
            yield (Date(self.value) 
                if isinstance(value, (date, datetime)) 
                else type(value)(str(self.value)))
        except Exception:
            yield None
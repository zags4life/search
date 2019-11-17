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

    All QueryField values are initially strings.  We need to convert them to 
    the same type as the field we are comparing.  This ensures that proper 
    comparisons occur, i.e.  comparing integer or decimal values.
    '''
    def wrapper(field, query_field):
        assert (isinstance(query_field, QueryField) and 
                isinstance(field, SearchField)), \
            'Invalid search field: {} - {}'.format(
                type(field), type(query_field))

        try:
            with query_field:
                return func(field, query_field(field.value))
        except Exception as e:
            logger.debug('{0}; {1}; {2}'.format(
                    e,
                    'SearchField: {}'.format(field),
                    'QueryField: {}'.format(query_field)
                )
            )
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

    @verify_name_matches
    def match(self, other):
        return re.search(str(other.value), str(self.value))

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
        super(QueryField, self).__init__(name, value)

    def __call__(self, value):
        '''Call operator - converts the underlying string value to the 
        appropriate type.
        '''

        # If the value is a date, convert the string value to a date object.
        # Else, convert the string value to the same type as the value
        self.value = Date(self.value) if isinstance(value, (date, datetime)) \
            else type(value)(self.value)
        return self

    def __enter__(self):
        self.__orig_val = self.value
        return self

    def __exit__(self, type, value, tb):
        self.value = self.__orig_val

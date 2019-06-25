# convertable_types.py

import collections

from .fields import SearchFieldDataProvider, SearchField

class __ImplicitlyConvertedSearchDataProvider(SearchFieldDataProvider):
    '''Used to wrap objects as SearchFieldDataProvider used for searching.
    This object will implicitly ensure the object adheres to the
    SearchFieldDataProvider interface.

    There are four supported modes:
    1) underlying object is a dictionary
    2) underlying object is a list
    3) underlying object is a class, derived from object
    4) underlying object already implements SearchFieldDataProvider interface
    '''
    def __init__(self, obj):
        '''Creates an instance of ImplicitlyConvertedSearchDataProvider.

        Parameters:
            obj - the underlying object to wrap as a SearchFieldDataProvider
        '''

        # Save the underlying object as a string for debugging
        self.__underlying_obj_str = str(obj)
        self.__fields = []

        # 1) If the object is a dictionary, wrap the key/value pairs as Field objects
        if isinstance(obj, dict):
            self.__fields = [SearchField(k,v) for k,v in obj.items()]

        # 2) If the object is a list, create Field objects for each value were the key is the index
        elif isinstance(obj, list):
            self.__fields = [SearchField(k,v) for k, v in enumerate(obj)]

        # 3) If the object does not implement SearchFieldDataProvider, iterate through all key/value pairs
        #    in the objects __dict__.  For any object that is not callable and does not start with '_',
        #    Create a SearchField object and add it to the list of fields
        elif not isinstance(obj, SearchFieldDataProvider):
            for k,v in obj.__dict__.items():
                if not k.startswith('_') and not callable(v):
                    self.__fields.append(SearchField(k,v))

        # 4) If the object implements SearchFieldDataProvider, raise an error
        else:
            raise AttributeError(
                "Cannot convert '{}' to SearchFieldDataProvider as it is " \
                "already of the correct type".format(obj.__class__.__name__)
            )

    def __getattr__(self, attr):
        for field in self.__fields:
            if field.name == attr:
                return field.value
        raise AttributeError("'ImplicitlyConvertedSearchDataProvider' object has no"
            " attribute '{}'".format(attr))

    @property
    def fields(self):
        return self.__fields

    def __str__(self):
        return self.__underlying_obj_str
    __repr__ = __str__

def implicit_conversion(func):
    '''Decorator that implicitly converts a list of values as
    SearchFieldDataProvider

    When the func is called, the list of objects will be implicitly converted
    to a list of SearchFieldDataProviders
    '''

    def convert_object(value):
        # If value is not a SearchFieldDataProvider, convert it to a
        # SearchFieldDataProvider by wrapping it in a
        # ImplicitlyConvertedSearchDataProvider.  If the value is already
        # a SearchFieldDataProvider, return value
        if not isinstance(value, SearchFieldDataProvider):
            return __ImplicitlyConvertedSearchDataProvider(value)
        return value

    def wrapper(self, values):
        # Ensure values is a list
        if not isinstance(values, collections.Collection):
            raise ValueError('values must be a list')

        return func(
            self,
            [convert_object(v) for v in values]
        )

    return wrapper
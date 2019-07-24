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
        self.__fields = []
        self.__underlying_obj = obj

        # 1) If the object is a dictionary, wrap the key/value pairs as 
        #    SearchField objects.
        if isinstance(obj, dict):
            self.__fields = [SearchField(k,v) for k,v in obj.items()]

        # 2) If the object is a list, create SearchField objects for each value
        #    were the key is the index.
        elif isinstance(obj, list):
            self.__fields = [SearchField(k,v) for k, v in enumerate(obj)]

        # 3) If the object does not implement SearchFieldDataProvider, 
        #    iterate through all attributes and properties in the object.
        #    For all properties and public (i.e. does not start with '_'),
        #    callable, attributes, create a SearchField object and add it to 
        #    the list of fields.
        elif not isinstance(obj, SearchFieldDataProvider):
            for k,v in obj.__class__.__dict__.items():
                if type(v) == property:
                    self.__fields.append(SearchField(k, getattr(obj, k)))

            for k,v in obj.__dict__.items():
                if not k.startswith('_') and not callable(v):
                    self.__fields.append(SearchField(k,v))
            
        # 4) If the object implements SearchFieldDataProvider, store the 
        #    objects fields.
        else:
            self.__fields = obj.fields

    @property
    def fields(self):
        return self.__fields

    @property
    def underlying_object(self):
        return self.__underlying_obj

    def __str__(self):
        return str(self.underlying_obj)
    __repr__ = __str__

def implicit_conversion(func):
    '''Decorator that implicitly converts a list of values as
    SearchFieldDataProvider

    When the func is called, the list of objects will be implicitly converted
    to a list of SearchFieldDataProviders
    '''
    def wrapper(self, values):
        # Ensure values is a list
        if not isinstance(values, collections.Collection):
            raise ValueError('values must be a collection')

        return [
            r.underlying_object for r in func(
                self,
                [__ImplicitlyConvertedSearchDataProvider(v) for v in values]
            )
        ]

    return wrapper
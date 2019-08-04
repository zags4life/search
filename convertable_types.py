# convertable_types.py

from collections.abc import Collection, Mapping
import logging

from .fields import SearchField
from .searchdataprovider import SearchDataProvider

logger = logging.getLogger(__name__)

def convert_dict(d):
    '''Convert the dict into a list of SearchField's, using each
    key/value pair as the SearchField'''
    return [SearchField(k,v) for k,v in d.items()]

def is_collection(v):
    return isinstance(v, Collection) and not isinstance(v, str)

class __ImplicitlyConvertedSearchDataProvider(SearchDataProvider):
    '''Used to wrap objects as SearchDataProvider used for searching.
    This object will implicitly ensure the object adheres to the
    SearchDataProvider interface.

    There are four supported modes:
    1) underlying object is a dictionary
    2) underlying object is a list
    3) underlying object implements SearchDataProvider interface
    4) underlying object is a class, derived from object
    '''
    def __init__(self, obj):
        '''Creates an instance of ImplicitlyConvertedSearchDataProvider.

        Parameters:
            obj - the underlying object to wrap as a SearchDataProvider
        '''

        self.__fields = []
        self.__underlying_obj = obj

        # 1) If the object is a dict, convert the dict to a list of
        #    SearchField objects.
        if isinstance(obj, Mapping):
            self.__fields = convert_dict(obj)

        # 2) If the object is a list, create SearchField objects for each value
        #    were the key is the index.
        elif isinstance(obj, list):
            self.__fields = [SearchField(k,v) for k, v in enumerate(obj)]

        # 3) If the object implements SearchDataProvider, retrieve objects
        #    fields and convert to a list of SearchField objects
        elif isinstance(obj, SearchDataProvider):
            # Retrieve the fields from the object
            fields = obj.fields

            # if fields is not a dict, raise an exception
            if not isinstance(fields, Mapping):
                raise InvalidFieldAttributeError(
                    "{} 'fields' property return an invalid type ('{}') - " \
                    "the fields property must return either a dict of " \
                    "key/value pairs of a list of SearchField objects".format(
                        obj.__class__.__name__,
                        type(fields).__name__
                    )
                )

            # Convert the dict to a list of SearchField objects
            self.__fields.extend(convert_dict(fields))

        # 4) If the object does not implement SearchDataProvider,
        #    iterate through all attributes and properties in the object.
        #    For all properties and public (i.e. does not start with '_')
        #    attributes, create a SearchField object and add it to
        #    the list of fields.
        else:
            # Convert all properties to SearchFields
            self.__fields.extend(convert_dict(
                {key: getattr(obj, key) for key, value in
                    obj.__class__.__dict__.items()
                    if type(value) is property}
            ))

            # Convert all public attributes to SearchFields
            self.__fields.extend(convert_dict(
                {key: value for key, value in obj.__dict__.items()
                    if not key.startswith('_')}
            ))

        # Collections are not supported.  Verify fields
        if any(is_collection(field.value) for field in self.__fields):
            invalid_fields = [f.name for f in self.__fields if is_collection(f.value)]
            self.__fields = [f for f in self.__fields if not is_collection(f.value)]

            # Log error
            msg = '{} contains invalid fields - ignoring fields "{}"'.format(
                obj.__class__.__name__, ', '.join(invalid_fields))
            logger.error(msg)

    @property
    def fields(self):
        '''Gets a list of SearchField's representing the underlying objects
        searchable fields.
        '''
        return self.__fields

    @property
    def underlying_object(self):
        '''Gets the underlying object'''
        return self.__underlying_obj

    def __str__(self):
        return str(self.underlying_object)

def implicit_conversion(func):
    '''Decorator that implicitly converts a list of values as
    SearchDataProvider

    When the func is called, the list of objects will be implicitly converted
    to a list of SearchFieldDataProviders
    '''
    def wrapper(self, values):
        # Ensure values is a list
        if not isinstance(values, Collection):
            raise ValueError('values must be a collection')

        return [
            r.underlying_object for r in func(
                self,
                {__ImplicitlyConvertedSearchDataProvider(v) for v in values}
            )
        ]

    return wrapper

class InvalidFieldAttributeError(Exception):
    pass
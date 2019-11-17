# searchdataprovider.py
from abc import ABCMeta, abstractproperty
from six import with_metaclass

class SearchDataProvider(with_metaclass(ABCMeta, object)):
    @abstractproperty
    def fields(self):
        '''Gets a dictionary of key/value pairs representing the objects 
        searchable fields.
        '''
        pass
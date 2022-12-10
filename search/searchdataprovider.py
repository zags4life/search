# searchdataprovider.py
from abc import ABCMeta, abstractmethod
from six import with_metaclass

 
class SearchDataProvider(with_metaclass(ABCMeta, object)):
    @property
    @abstractmethod
    def fields(self):
        '''Gets a dictionary of key/value pairs representing the objects 
        searchable fields.
        '''
        pass

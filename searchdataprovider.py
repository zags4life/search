# searchdataprovider.py
from abc import ABC, abstractproperty

class SearchFieldDataProvider(ABC):
    @abstractproperty
    def fields(self):
        '''Gets a dictionary of key/value pairs representing the objects 
        searchable fields.
        '''
        pass
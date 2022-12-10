# unittests/testobject.py
from ..fields import SearchField
from ..searchdataprovider import SearchDataProvider

class _TestObject(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        values = ['{}={}'.format(k,v) for k,v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')]

        return 'TestObject: {}'.format(
            ', '.join(
                ['{}={}'.format(k,v) for k,v in self.__dict__.items()
                    if not callable(v) and not k.startswith('_')]
                )
            )


class TestSearchDataProvider(_TestObject, SearchDataProvider):
    @property
    def fields(self):
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}


class TestSearchDataFieldProvider(_TestObject, SearchDataProvider):
    @property
    def fields(self):
        return [SearchField(k, v) for k,v in self.__dict__.items() if not k.startswith('_')]


TestObject = TestSearchDataProvider
TestFieldObject = TestSearchDataFieldProvider
TestObject = _TestObject
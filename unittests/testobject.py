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

    __repr__ = __str__

class InvalidTestObject(_TestObject):
    @property
    def fields(self):
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}

    @property
    def asfdff_fields(self):
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}


class TestSearchDataProvider(InvalidTestObject, SearchDataProvider):
    pass

TestObject = TestSearchDataProvider
# TestObject = _TestObject
TestObject = InvalidTestObject

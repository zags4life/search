# unittests/testobject.py
import random

from ..fields import SearchField
from ..query import query


class TestObject(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
    
        if len(self.__dict__.items()) != len(other.__dict__.items()):
            return False

        match = True
        for k in self.__dict__.keys():
            match &= k in other.__dict__

        if match:
            for attr, value in self.__dict__.items():
                other_value = getattr(other, attr)
                match &= value == other_value
        return match

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        values = [f'{k}={v}' for k,v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')]

        return '{1}({0})'.format(
            ', '.join(
                [f'{k}={v}' for k,v in self.__dict__.items()
                    if not callable(v) and not k.startswith('_')]
                ),
            self.__class__.__name__
            )
    __repr__ = __str__

TestFieldObject = TestObject
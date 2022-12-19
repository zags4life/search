# unittests/testobject.py

class TestObject(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def is_equal(self, other):
        '''Determines if two TestObject's are equal to each other.  If the two
        objects are equal, return True, otherwise False.

        Note: We are not overriding __eq__ operator because by doing so,
        TestObject will no longer be hashable.  We _could_ override __hash__,
        but for simplicity sake we will do it this way.
        '''
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

    def __str__(self):
        '''Returns a string representation of the object'''
        values = [f'{k}={v}' for k,v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')]

        return f"{self.__class__.__name__}({', '.join(values)})"
    __repr__ = __str__


class TestPropertyObject(TestObject):
    def __init__(self, **kwargs):
        def make_prop(value):
            def getter(self):
                return value
            return property(getter)

        for k,v in kwargs.items():
            setattr(self.__class__, k, make_prop(v))

    def __str__(self):
        values = []
        for k,v in self.__dict__.items():
            values.append(f'{k}={v}')

        for k, v in self.__class__.__dict__.items():
            if type(v) is property:
                values.append(f'{k}={getattr(self, k)}')

        return f"{self.__class__.__name__}({', '.join(values)})"

TestFieldObject = TestPropertyObject

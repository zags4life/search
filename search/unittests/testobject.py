# unittests/testobject.py


class TestObject(object):
    '''Test object that will create an attribute for each key/value pair in
    kwargs.
    
    This object is required to test searching for attribute values.
    '''
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
        for key in self.__dict__:
            match &= key in other.__dict__

        if match:
            for attr, value in self.__dict__.items():
                match &= value == getattr(other, attr)
        return match

    @classmethod
    def create_instance(cls, values):
        assert isinstance(values, dict)
        return cls(**values)

    def __str__(self):
        '''Returns a string representation of the object'''
        values = [f'{k}={v}' for k,v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')]

        return f"{self.__class__.__name__}({', '.join(values)})"
    __repr__ = __str__


class NestedTestObject(TestObject):
    '''A test object that supports, and created, child objects stores as 
    attributes.  Constructor only supports kwargs and support key values
    in the format of `foo.bar.gurp`.  Key values in this format will be 
    split, and each part will become a child object.
    
    E.g. kwargs = {'name.age': 42}
    
    This will result in an attribute named `name` whose value is 
    NestedTestObject, which in turn has an attribute named `age`
    with the value `42`.
    
    This object is required to test searching for nested values
    '''
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # If key contains '.', then we need to recursively build nested 
            # objects.
            if '.' in key:
                parts = key.split('.')
                assert len(parts) > 1
                key = parts[0]
                value = NestedTestObject(**{'.'.join(parts[1:]): value})
            
            # Set the attribute name and value
            setattr(self, key, value)


class PropertyTestObject(TestObject):
    '''Test object that creates a property for each key in kwargs and sets the
    properties value to value.
    
    E.g. kwargs = {'name': 'Mike', 'age': 42}
    
    The resulting object would have two properties, `name` and `age` 
    respectively.
    
    Note: Because properties are set at the class level, if you create multiple
    instances of this object, all objects will have the same properties, 
    even if you provide different kwargs when constructing each object.
    
    This object is required to test searching for property values
    '''
    def __init__(self, **kwargs):
        for prop_name, prop_value in kwargs.items():
            setattr(
                self.__class__,
                prop_name,
                self.__make_prop(prop_value)
            )

    def __str__(self):
        values = []
        for k,v in self.__dict__.items():
            values.append(f'{k}={v}')

        for k, v in self.__class__.__dict__.items():
            if type(v) is property:
                values.append(f'{k}={getattr(self, k)}')
        return f"{self.__class__.__name__}({', '.join(values)})"

    @staticmethod
    def __make_prop(value):
        '''Create a property with a getter, which returns `value`.'''
        def getter(self):
            return value
        return property(getter)
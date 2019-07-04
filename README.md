Search
======

## Introduction

The _search_ module enables users to quickly and easily query a list of generic python objects using a human readable grammar.  This is particularly useful when you need to filter frequently or wish to enable callers to filter using custom filers

* [Introduction](#introduction)
* [Grammar](#grammar)
  * [Arithmetic Expressions](#arithmetic-expressions)
    * [Equals vs Like](#equals-vs-like)
  * [Logical Statements](#logical-statements)
  * [Grouping Statements](#grouping-statements)
* [Supported Types](#supported-types)
* [API](#api)
* [Examples](#examples)

## Grammar

### Arithmetic Expressions
The most fundamental expression consists of a key/value pair separated by an operator.  Any object that contains a field that matches the field name and field value returns `True` using the supplied operator will be returned in the resulting set. 

```<field_name> <operator> <field_value>```

**Note:** `<field_name>` **can be a regular expression, regardless of the operator.**

The _search_ module enables `=`, `!=`, `‹`, `‹=`, `>`, `>=`, and `like` arithmetic operators.  The `like` operator allows for field values that are regular expressions.

For example:
```
name = tom
```

#### Equals vs Like
The equals (`=`) operator tests for equality were as the `like` operator tests for likeness using regular expressions.

### Logical Statements
Arithmetic expressions can be combine using logical statements and supports `and`, `or`, and `not` (or `!`) logical operators.

For example:
```
name like Tom and age > 25
name like Tom or age != 25
not name like Tom or age != 25
!name like Tom or age != 25
```

### Grouping Statements

Arithmetic expressions and logical statements can be grouped together using parenthesis.

For example:
```
(name like Tom and age != 25) or (name = Mike)
!(name like Tom or age != 25)
```


### Case sensitivity
The grammar is case insensitive for all logical and arithmetic operators, and field names.  The field value case will still be honored.

For example:
`Name = Tom` and `name = Tom` are functionally equivalent
`name = Tom` and `name = tom` are _not_ functionally equivalent


## Supported Types
The _search_ module automatically converts `dict`, `list`, and custom class types to searchable objects.  

For `dict`, each key/value pair becomes a searchable item where the search field name equals the key and the search field value becomes the value.

For `list`, the search field name is the list index and the search value is the value at that index.

For custom types, all public attributes become searchable key/value pairs.

## API
The _search_ module API `query` is the main entry point for querying.

```
def query(query_str, values):
    '''Queries a list of values given a query string returning the resulting 
    subset of values.
    
    Parameters:
    query_str -a string representing the query 
    values - a list of values to query
    
    Returns: 
    The resulting subset of items after the original values have been 
    filtered using the query_str, in list form.
    '''
```

### Defining Custom Search Fields
If you recall, all public attributes in a class will automatically be made searchable.  However, in some cases, a developer may wish to control which attributes are searchable.  In this case, they must derive their class from `SearchFieldDataProvider`.


#### SearchFieldDataProvider
The `SearchFieldDataProvider` is an ABC and is required for all searchable items.  Items that do not implement this interface will be automatically converted ([see Supported Types](#supported-types)).

`SearchFieldDataProvider` requires child classes to implement the `fields` property, which exposes all searchable fields to the _search_ module.  Each item in the list must be a `SearchField` item.


#### SearchField
A `SearchField` defines a searchable field and its corresponding value.

## Examples

### Searching a list of dictionaries
```
from search import query

values = [
    {'x': 1, 'y': 2 },
    {'x': 1, 'y': 3 },
    {'x': 2, 'y': 2 },
]

for result in query('y = 2', values):
    print (result)

#########
Output:

{'x': 1, 'y': 2 }
{'x': 2, 'y': 2 }
```

### Search a list of classes
```
from search import query

class TestObject(object):
    def __init__(self, **kwargs):
        self.__fields = []
        for k,v in kwargs.items():
            setattr(self, k, v)
            
if __name__ == '__main__':
    values = [
        TestObject(name=Tom, age=27),
        TestObject(name=Eric, age=34, city='Chicago'),
    ]
    
    results = query('city = Chicago', values)
    for result in query('y = 2', values):
    print (result)

#########
Output:

TestObject(name=Eric, age=34, city='Chicago')
```
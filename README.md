Search
======

* [Introduction](#introduction)
* [Grammar](#grammar)
  * [Arithmetic Expressions](#arithmetic-expressions)
    * [Equals vs Like](#equals-vs-like)
  * [Logical Statements](#logical-statements)
  * [Grouping Statements](#grouping-statements)
* [Supported Types](#supported-types)
* [API](#api)
* [Examples](#examples)

## Introduction
The _search_ module enables users to quickly and easily search a collection of generic python objects using a human readable grammar.  This is particularly useful when you need to filter frequently or wish to enable callers to filter using custom filters.


## Grammar
### Arithmetic Expressions
The most fundamental expression consists of a key / value pair separated by an operator.  Any object that contains a field, or attribute, that matches the field name and field value returns `True` using the supplied operator will be returned in the resulting set.

```<field_name> <operator> <field_value>```

**Note:** `<field_name>` **can be a regular expression, regardless of the operator.**

The _search_ module enables `=`, `!=`, `<`, `<=`, `>`, `>=`, and `like` arithmetic operators.

For example:
```
name = travis
```

#### '=' vs like
The equals (`=`) operator tests for equality were as the `like` operator tests for likeness using regular expressions.

#### Type Conversion
When a query is compiled, both the field name and field value are parsed as strings.  If we were to compare objects values using this parsed field value, queries like `x = 1` will fail because it would result in a `str` to `int` comparison.  To solve this, when an object is found to have an attribute that matches the field name, the field value will be converted to the same type as the objects attribute value.  **Type conversion assumes that a `type` can be instanciated by passing a string to the constructor.  E.g. `int('2')`.**  

Type conversion is temporary and does not affect the original value.  It is also worth noting that field name is _always_ treated as a string and is never altered or modified.


### Logical Statements
Arithmetic expressions can be combine using logical statements and supports `and`, `or`, and `not` (or `!`) logical operators.

The below are example query strings and illistrate how the string is logically interrupted by the _search_ module

```
name like Tom and age > 25  ->  [[((?i)name LIKE Tom) AND ((?i)age > 25)]

name like Tom or Age != 25  ->  [((?i)name LIKE Tom) OR ((?i)age != 25)]

not name like Tom or age != 25  ->  [[NOT ((?i)name LIKE Tom)] OR ((?i)age != 25)]

!name like Tom or age != 25  ->  [[NOT ((?i)name LIKE Tom)] OR ((?i)age != 25)]
```

### Grouping Statements

Arithmetic expressions and logical statements can be grouped together using parenthesis.

For example:
```
(name like Tom and age != 25) or (name = Mike)  ->  [[[(name LIKE Tom) AND (age != 25)] OR (name = Mike)]

!(name like Tom or age != 25)  ->  [[NOT [(name LIKE Tom) OR (age != 25)]]
```

### Case sensitivity
All logical and arithmetic operators are case insensitive (e.g. `AND` vs `and`), where as field names and value are case _sensitive_ (e.g. `name like Tom` vs `Name like Tom`).

## Supported Types
### Custom Classes
Any class object is searchable.  All "public" attributes and properties will be used for comparison.  Note, any attribute that with starts with `_` or is callback will _not_ be considered in the search collection.

### Builtin Types
Builtin types `list` and `dict` are also searchable.  Please note that `set` is not searchable.

For `dict`, each key/value pair becomes a searchable item where the search field name equals the key and the search field value becomes the value.

For `list`, the search field name is the list index and the search value is the value at that index.

## API
The _search_ module API `query` is the main entry point for querying.

```
def search(search_str, values, dry_run=False):
    '''Searches a collection of python objects based on the search string

    Parameters:
        search_str - the query string using the search grammar
        values - a collection of objects to search
        dry_run - a bool indicating whether to compile the query only, but not
            execute it.  If True, the query will be return in string form.
            This is helpful to validate the search is being compiled correctly.

    Returns - a subset, as a list, of objects from value that match the search
    '''
```

## Examples

### Searching a collection of dictionaries
```
from search import search

values = [
    {'x': 1, 'y': 2 },
    {'x': 1, 'y': 3 },
    {'x': 2, 'y': 2 },
]

for result in search('y = 2', values):
    print (result)

#########
Output:

{'x': 1, 'y': 2 }
{'x': 2, 'y': 2 }
```

### Searching a collection of lists
```
from search import search

values = [
    ['Tom', 'Travis'],
    [1, 2, 4],
]

for result in search('.* = 2', values):
    print (result)

#########
Output:

[1, 2, 4]
```

### Search a collection of classes
```
from search import search

class TestObject(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

values = [
    TestObject(name='Tom', age=27),
    TestObject(name='Eric', age=34, city='Chicago'),
]

results = search('city = Chicago', values)
for result in results:
    print (result)

#########
Output:

TestObject(name='Eric', age=34, city='Chicago')
```

### Search a mixed collection
```
from search import search

class TestObject(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

values = [
    TestObject(name='Tom', age=27),
    {'x': 1, 'y': 2 },
    {'x': 1, 'y': 3 },
    {'x': 2, 'y': 2 },
    TestObject(name='Eric', age=34, city='Chicago'),
]

results = search('(city = Chicago and age > 30) or x > 1', values)
for result in results:
    print (result)

#########
Output:

TestObject(name=Eric, age=34, city=Chicago)
{'x': 2, 'y': 2}
```
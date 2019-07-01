Search
======

## Introduction

TBD

## Grammar and Syntax

The most fundamental expression consists of a key/value pair separated by an operator.  Any object that contains a field that matches the field name and field value returns `True` using the supplied operator will be returned in the resulting set. 

```<field_name> <operator> <field_value>```

Note: `<field_name>` can be a regular expression, regardless of the operator.

```
from search import query

values = [
    {'x': 1, 'y': 2 },
    {'x': 1, 'y': 3 },
    {'x': 2, 'y': 2 }
]

for result in query('y = 2', values):
    print (result)

#########
Output:

{'x': 1, 'y': 2 }
{'x': 2, 'y': 2 }
```

The _search_ module enables `=`, `!=`, `‹`, `‹=`, `>`, `>=`, and `like` arithmetic operators.  The `like` operator allows for field values that are regular expressions.

### Equals vs. Like
The equals (`=`) operator tests for equality were as the `like` operator tests for likeness using regular expressions.


## Supported Types

The _search_ module automatically converts `dict`, `list`, and custom class types to searchable objects.  

For `dict`, each key/value pair becomes a searchable item where the search field name equals the key and the search field value becomes the value.

For `list`, the search field name is the list index and the search value is the value at that index.

For custom types, all public attributes become searchable key/value pairs.

### Custom Types - SearchDataProvider

TBD

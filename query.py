from .convertable_types import implicit_conversion
from .lexer import compile

import logging
logger = logging.getLogger(__name__)

class Query(object):
    def __init__(self, query_str):
        # Validate the query string before compiling
        self.__validate_query_str(query_str)

        # compile the query string into a condition object
        self._condition = compile(query_str)

        # if condition is none, the query string is invalid, raise
        if not self._condition:
            raise InvalidQueryError("Invalid query string '{}'".format(query_str.replace('\n', '')))

    @implicit_conversion
    def __call__(self, values):
        return self._condition(set(values))

    def __str__(self):
        return 'QUERY: {}'.format(self._condition)

    def __validate_query_str(self, query_str):
        stack = []
        try:
            for c in query_str:
                if c == '(':
                    stack.append(c)
                elif c == ')':
                    stack.pop(-1)
        except IndexError:
            raise InvalidQueryError('Unbalanced parenthesis')

        if len(stack) != 0:
            raise InvalidQueryError('Unbalanced parenthesis')

class InvalidQueryError(Exception):
    pass

def query(query_str, values):
    '''Executes a query on the set of values provided, based on the
    query string specified.

    Example:

    from search import query

    class TestObject(object):
        def __init__(self, **kwargs):
            for k,v in kwargs.items():
                setattr(self, k, v)

        def __str__(self):
            return 'TestObject({})'.format(
                ', '.join(
                    ['{}={}'.format(k,v) for k,v in self.__dict__.items() if not k.startswith('_')]
                )
            )

    values = [
        {'x': 1, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        TestObject(x=3, y=2, foo='mike'),
        {'name': 'Mike', 'fo0d': 'bar'},
    ]

    results = query('not foo = bar and y > 0', values)

    for result in results:
        print(result)

    # OUTPUT:
    # {'x': 3, 'y': 2, 'foo': 'gurp'}
    # {'x': 1, 'y': 2, 'foo': 3}
    # {'x': '3', 'y': 2, 'foo': 'gurp'}
    # TestObject(x=3, y=2, foo=mike)

    '''
    if not query_str:
        return list(values)

    q = Query(query_str)
    logger.info(str(q))
    return list(q(values))
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
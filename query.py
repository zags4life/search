# query.py

from .convertable_types import implicit_conversion
from .lexer import compile

class Query(object):
    def __init__(self, query_str):
        # Validate the query string before compiling
        self.__condition = None

        if not (not query_str or query_str == '*'):
            self.__validate_query_str(query_str)
            # compile the query string into a condition object
            self.__condition = compile(query_str)

            # if condition is none, the query string is invalid, raise
            if not self.__condition:
                raise InvalidQueryError(
                    "Invalid query string '{}'".format(
                        query_str.replace('\n', ''))
                )

    @implicit_conversion
    def __call__(self, values):
        if not self.__condition:
            return values
        return self.__condition(values)

    def __str__(self):
        return 'QUERY: {}'.format(self.__condition)

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
    return Query(query_str)(values)
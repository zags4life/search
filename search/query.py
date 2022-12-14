# query.py

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

    def __call__(self, values):
        if not self.__condition:
            return values

        converted_values = []
        for value in values:
            if isinstance(value, (list, dict)):
                converted_values.append(DictHashableWrapperObject(value))
            else:
                converted_values.append(value)
        values = converted_values
        
        results = self.__condition(values)
        converted_results = []
        for result in results:
            if isinstance(result, DictHashableWrapperObject):
                converted_results.append(result.original_object)
            else:
                converted_results.append(result)
        return converted_results

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


class DictHashableWrapperObject:
    def __init__(self, value):
        if isinstance(value, list):
            value = {str(k):v for k,v in enumerate(value)}

        for k, v in value.items():
            setattr(self, k, v)
        self.original_object = value


class InvalidQueryError(Exception):
    pass


def query(query_str, values):
    return Query(query_str)(values)
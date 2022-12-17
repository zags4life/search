# query.py

from .lexer import compile


class Query(object):
    def __init__(self, query_str):
        '''Used to search a collection of unlike python objects based on a 
        search string.
        
        Parameters:
        query_str - a string representing the query used to search subsequent 
            collections
        '''
        # Validate the query string before compiling
        self.__condition = None

        # If the query string is empty, None, or equal to '*',
        # leave __condition unset, which will result is returning 
        # the complete collection when called.
        # 
        # If the query_str is not empty, None, or equal to '*', 
        # validate and compile the query string.
        if not (not query_str or query_str == '*'):
            # Validate query string
            self.__validate_query_str(query_str)
            
            # compile the query string into a condition object
            self.__condition = compile(query_str)

            # if condition is none, the query string is invalid, 
            # raise exception
            if not self.__condition:
                query_str = query_str.replace('\\n', '')
                raise InvalidQueryError(f"Invalid query string '{query_str}'")

    def __call__(self, values):
        '''Search values collection for all elements that match the query
        
        Parameters:
        values - a collection of elements to search
        
        Returns - a collection of elements that match the search criteria
        '''
        if not self.__condition:
            return values

        converted_values = []
        for value in values:
            if isinstance(value, (list, dict)):
                converted_values.append(HashableWrapperObject(value))
            else:
                converted_values.append(value)
        values = converted_values
        
        results = self.__condition(values)
        converted_results = []
        for result in results:
            if isinstance(result, HashableWrapperObject):
                converted_results.append(result.original_object)
            else:
                converted_results.append(result)
        return converted_results

    def __str__(self):
        return f'QUERY: {self.__condition}'

    def __validate_query_str(self, query_str):
        '''Validate the query str by ensuring it has balances parenthesis'''
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


class HashableWrapperObject:
    def __init__(self, value):
        if isinstance(value, list):
            value = {str(k):v for k,v in enumerate(value)}

        for k, v in value.items():
            setattr(self, k, v)
        self.original_object = value

    def __str__(self):
        return str(self.original_object)

class InvalidQueryError(Exception):
    pass


def query(query_str, values):
    return Query(query_str)(values)
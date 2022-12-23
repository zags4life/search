# query.py

if __debug__:
    import logging
    logger = logging.getLogger(__name__)

from .decorators import validate_query
from .lexer import compile


class Query(object):
    '''Queries a collection of unlike python objects based on a
    search string.

    Parameters:
        query_str - a string representing the query used to search subsequent
            collections
    '''
    def __init__(self, query_str):
        query_str = query_str.strip()
        if __debug__:
            self.query_str = query_str

        self.__condition = None

        # If the query string is empty, None, or equal to '*',
        # leave __condition unset, which will result is returning
        # the complete collection when called.
        #
        # If the query_str is not empty, None, or equal to '*',
        # validate and compile the query string.
        if not (not query_str or query_str == '*'):
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
        
        if __debug__:
            logger.info(f'Query: {self.query_str}')
        
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
                converted_results.append(result._original_object)
            else:
                converted_results.append(result)
        return converted_results

    def __str__(self):
        return f'QUERY: {self.__condition}'


class HashableWrapperObject:
    def __init__(self, value):
        if isinstance(value, list):
            value = {str(k):v for k,v in enumerate(value)}

        for k, v in value.items():
            setattr(self, k, v)
        self._original_object = value

    def __str__(self):
        return str(self._original_object)


class InvalidQueryError(Exception):
    pass


@validate_query
def search(search_str, values, dry_run=False):
    '''Searches a collection of, potentially, unlike python objects based on the search string

    Parameters:
        search_str - the query string using the search grammar
        values - a collection of objects to search
        dry_run - a bool indicating whether to compile the query only, but not
            execute it.  If True, the query will be return in string form.
            This is helpful to validate the search is being compiled correctly.

    Returns - a subset, as a list, of objects from value that match the search
    '''
    query = Query(search_str)

    if dry_run:
        return str(query)
    return query(values)
query = search
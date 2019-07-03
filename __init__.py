# __init__.py
from .query import Query, InvalidQueryError
from .fields import SearchFieldDataProvider, SearchField

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
    if not query_str:
        return list(values)

    return list(Query(query_str)(values))


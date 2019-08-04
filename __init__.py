# __init__.py
from .convertable_types import InvalidFieldAttributeError
from .searchdataprovider import SearchDataProvider
from .query import query, Query, InvalidQueryError

# alias query
search = query

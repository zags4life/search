# __init__.py
from .query import query, Query, InvalidQueryError
from .fields import SearchField as Field

# alias query
search = query

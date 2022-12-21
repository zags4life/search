# __init__.py

PARSERS = {}

def register_parser(_type):
    def decorator(func):
        PARSERS[_type] = func
        return func
        
    return decorator

from .date import *
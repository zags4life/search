# __init__.py

from datetime import datetime
import logging
import re

from ..query import InvalidQueryError

logger = logging.getLogger(__name__)

REGISTERED_UNITTESTS = []

def test(func):
    REGISTERED_UNITTESTS.append(func)

def run(tests_to_run):
    result = 0
    for test in REGISTERED_UNITTESTS:
        if not re.search(tests_to_run, test.__name__):
            continue

        try:
            print('Running test - {}'.format(test.__name__))
            test()
            print('Test complete - {}\n'.format(test.__name__))
        except AssertionError as e:
            logger.error(e)
    return result

from ..fields import SearchFieldDataProvider, SearchField
from ..query import Query

class TestObject(object):
    def __init__(self, **kwargs):
        self.__fields = []
        for k,v in kwargs.items():
            setattr(self, k, v)
            self.__fields.append(SearchField(k,v))

    @property
    def fields(self):
        return self.__fields

    def __str__(self):
        values = ['{}={}'.format(k,v) for k,v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')]

        return 'TestObject: {}'.format(
            ', '.join(
                ['{}={}'.format(k,v) for k,v in self.__dict__.items()
                    if not callable(v) and not k.startswith('_')]
                )
            )

    __repr__ = __str__

def execute_query(search_str, dry_run=False, debug=False):
    values = [
        {'x': 2, 'y': 2, 'foo': 3},
        dict(x=1, y=2, foo='bar'),
        dict(x='3', y=2, foo='gurp'),
        dict(x=3, y=2, foo='gurp'),
        [1,2,3,4],
        TestObject(x=3, y=2, foo='travis'),
        {'name': 'Mike', 'fo0d': 'bar'},
        {'name': 'Mike', 'fo0d': 'bar', 'date': datetime.today()},


        {'name': 'mike', 'food': 'bar'},

        TestObject(name='Travis', age='None'),
    ]

    try:
        q = Query(search_str)

        if not dry_run:
            print('{}'.format(q))

        results = q(values)

        if not dry_run:
            print('\nResults:')

            for v in results:
                print(' '*4, v)

            print('{} results found - out of {} records'.format(len(results), len(values)))

    except InvalidQueryError as e:
        print('Invalid Query: {}'.format(e))
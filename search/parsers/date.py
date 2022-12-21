# date.py

from datetime import date, datetime
import logging

from . import register_parser

logger = logging.getLogger(__name__)


DATE_FORMATS = (
    '%m-%d-%Y',
    '%m-%d-%y',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%m%d%Y',
    '%m%d%y',
    '%m/%d',
    '%m-%d',
    '%m%d',
    '%Y%m%d',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%y%m%d',
)

@register_parser(date)
@register_parser(datetime)
def Date(date_str):
    '''Parse date in string format into a datetime object'''
    if not date_str:
        return None

    for format in DATE_FORMATS:
        try:
            formatted = datetime.strptime(date_str, format)

            if formatted.year == 1900:
                formatted = datetime(
                    year=datetime.now().year,
                    month=formatted.month,
                    day=formatted.day)
            return formatted.date()
        except ValueError:
            pass

    logger.error("Failed to parse date '{}'".format(date_strs))
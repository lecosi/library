
import os
from enum import Enum

OPEN_LIBRA_API_URL = os.getenv('OPEN_LIBRA_API_URL')


class OpenLibraURLEnum(Enum):
    SEARCH_BOOKS = '/api/v1/get'


FILTER_LIST_IN_SEARCH = {
    'title': 'book_title',
    'author': 'book_author',
    'category': 'category',
    'editor': 'publisher',
    'description': 'keyword',
    'publication_date': 'publisher_date',
}

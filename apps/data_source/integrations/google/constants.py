
import os
from enum import Enum

GOOGLE_API_URL = os.getenv('GOOGLE_API_URL')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class GoogleURLEnum(Enum):
    SEARCH_BOOKS = '/books/v1/volumes'


FILTER_LIST_IN_SEARCH = {
    'title': 'intitle:',
    'author': 'inauthor:',
    'category': 'subject:',
    'editor': 'inpublisher:',
    'subtitle': 'subtitle+:',
    'description': 'description+:',
    'publication_date': 'published+date+:',
}

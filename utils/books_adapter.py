from typing import Dict, Any

from apps.data_source.factories.constants import UNREGISTERED
from apps.data_source.integrations.constants import SourceSearchTypeEnum
from utils.serializers import BookDTO


class BooksAdapter:

    @staticmethod
    def transform_from_google(item: Dict[str, Any]) -> BookDTO:
        return BookDTO(
            book_id=item.get('id'),
            source=SourceSearchTypeEnum.GOOGLE_SEARCH.value,
            title=item.get('title'),
            subtitle=item.get('subtitle', UNREGISTERED),
            editor=item.get('publisher', UNREGISTERED),
            description=item.get('description', UNREGISTERED),
            publication_date=item.get('publishedDate'),
            categories=item.get('categories'),
            authors=item.get('authors')
        )

    @staticmethod
    def transform_from_openlibrary(item: Dict[str, Any]) -> BookDTO:
        categories = item['categories']
        parsed_categories = [category['name'] for category in categories]
        return BookDTO(
            book_id=item.get('ID'),
            source=SourceSearchTypeEnum.OPEN_LIBRARY_SEARCH.value,
            title=item.get('title'),
            subtitle=item.get('subtitle', UNREGISTERED),
            editor=item.get('publisher', UNREGISTERED),
            description=item.get('content', UNREGISTERED),
            publication_date=item.get('publisher_date'),
            categories=parsed_categories,
            authors=item.get('author')
        )

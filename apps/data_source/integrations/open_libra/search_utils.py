import logging
from typing import Dict, Any, Optional, List
from utils.books_adapter import BooksAdapter
from utils.serializers import BookDTO

logger = logging.getLogger(__name__)


class OpenLibraryUtil:

    @classmethod
    def parser_response(
        cls,
        *,
        items: List[Dict[str, Any]]
    ) -> Optional[List[BookDTO]]:

        parsed_items = []

        for item in items:
            try:
                book_data = BooksAdapter.transform_from_openlibrary(
                    item=item
                )
                parsed_items.append(book_data)
            except Exception as e:
                logger.error(f'OpenLibraUtil :: parser_data :: {e}')
                continue

        return parsed_items

import logging
from typing import Dict, Any, List
from utils.books_adapter import BooksAdapter
from utils.serializers import BookDTO

logger = logging.getLogger(__name__)


class GoogleSearchUtil:

    @classmethod
    def parser_response(cls, *, items: List[Dict[str, Any]]) -> List[BookDTO]:
        parsed_items = []
        for item in items:
            try:
                book_id = item['id']
                volume_info = item.get('volumeInfo')
                if not volume_info:
                    continue

                volume_info['id'] = book_id
                book_data = BooksAdapter.transform_from_google(
                    item=volume_info
                )
                parsed_items.append(book_data)
            except Exception as e:
                logger.error(f'GoogleSearch :: parser_data :: {e}')
                continue

        return parsed_items

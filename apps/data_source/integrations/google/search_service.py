import logging
from typing import Dict, Any, Optional, List

from apps.data_source.abstractions.abstract_search import AbstractSearch
from apps.data_source.factories.constants import UNREGISTERED
from apps.data_source.integrations.google.constants import \
    FILTER_LIST_IN_SEARCH
from apps.data_source.integrations.google.google_book_service import \
    GoogleSearchService

logger = logging.getLogger(__name__)


class GoogleSearch(AbstractSearch, GoogleSearchService):
    def search_books(
        self,
        data: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        query = self.build_query(data=data)
        try:
            book_service = GoogleSearchService()
            response_data = book_service.get_books(query=query)
        except Exception as e:
            logger.error(f'GoogleSearch :: search_books :: {e}')
            return
        total_items = response_data.get('totalItems', 0)
        if total_items <= 0:
            return

        parsed_data = self.parser_data(items=response_data['items'])

        return parsed_data

    def build_query(self, *, data: Dict[str, Any]) -> str:
        query = ''
        for _filter in data:
            filter_str = self.validate_filter(
                filter_name=_filter,
                filter_value=data[_filter]
            )
            if not filter_str:
                continue

            query += filter_str

        return query

    @staticmethod
    def validate_filter(
        *,
        filter_name: str,
        filter_value: str
    ) -> Optional[str]:
        filter_field = FILTER_LIST_IN_SEARCH.get(filter_name)
        if not filter_field:
            return

        filter_value = filter_value.replace(' ', '+')
        return f'{filter_field}{filter_value}+'

    @staticmethod
    def parser_data(*, items: List[Dict[str, Any]]):
        parsed_items = []
        for item in items:
            try:
                book_id = item['id']
                volume_info = item.get('volumeInfo')
                if not volume_info:
                    continue

                title = volume_info['title']
                subtitle = volume_info.get('subtitle', UNREGISTERED)
                description = volume_info.get('description', UNREGISTERED)

                data = {
                    'id': book_id,
                    'title': title,
                    'subtitle': subtitle,
                    'authors': volume_info.get('authors'),
                    'editor': volume_info.get('publisher', UNREGISTERED),
                    'published_date': volume_info.get('publishedDate', None),
                    'description': description,
                    'categories': volume_info.get('categories'),
                }
                parsed_items.append(data)
            except Exception as e:
                logger.error(f'GoogleSearch :: parser_data :: {e}')
                continue

        return parsed_items

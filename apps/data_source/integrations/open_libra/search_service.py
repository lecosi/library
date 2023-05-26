import logging
from typing import Dict, Any, Optional, List

from apps.data_source.abstractions.abstract_search import AbstractSearch
from apps.data_source.factories.constants import UNREGISTERED
from apps.data_source.integrations.open_libra.constants import \
    FILTER_LIST_IN_SEARCH
from apps.data_source.integrations.open_libra.open_libra_service import \
    OpenLibraSearchService

logger = logging.getLogger(__name__)


class OpenLibraSearch(AbstractSearch, OpenLibraSearchService):
    def search_books(
        self,
        data: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:

        query = self.build_query(data=data)

        try:
            book_service = OpenLibraSearchService()
            response_data = book_service.get_books(query=query)
        except Exception as e:
            logger.error(f'OpenLibraSearch :: search_books :: {e}')
            return

        if not response_data:
            return

        parsed_data = self.parser_data(items=response_data)

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

        return f'{filter_field}="{filter_value}"&'

    def parser_data(self, *, items: List[Dict[str, Any]]):

        parsed_items = []

        for item in items:
            try:
                book_id = item['ID']
                title = item['title']
                subtitle = item.get('subtitle', UNREGISTERED)
                description = item.get('content', UNREGISTERED)
                categories = item.get('categories')
                if categories:
                    categories = self.parse_categories(categories=categories)

                data = {
                    'id': book_id,
                    'title': title,
                    'subtitle': subtitle,
                    'authors': [item.get('author')],
                    'editor': item.get('publisher', UNREGISTERED),
                    'published_date': item.get('publisher_date', None),
                    'description': description,
                    'categories': categories,
                }
                parsed_items.append(data)
            except Exception as e:
                logger.error(f'GoogleSearch :: parser_data :: {e}')
                continue

        return parsed_items

    @staticmethod
    def parse_categories(
        *,
        categories: List[Dict[str, Any]]
    ) -> Optional[List]:
        category_lst = []
        for category in categories:
            try:
                name = category['name']
                category_lst.append(name)
            except Exception as e:
                logger.error(f'OpenLibraSearch :: parse_categories :: {e}')
                continue

        return category_lst

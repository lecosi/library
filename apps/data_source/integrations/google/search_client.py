from apps.data_source.abstractions.abstract_search import SearchMethod
from apps.data_source.integrations.google.constants import (
    GOOGLE_API_URL,
    GOOGLE_API_KEY, GoogleURLEnum, FILTER_LIST_IN_SEARCH
)
from typing import Dict, Any, Optional

from aiohttp import ClientSession


class GoogleSearchClient(SearchMethod):
    async def get_books(
        self,
        data_to_filter: Dict[str, Any],
        session: ClientSession
    ) -> Optional[str]:
        query = self.build_query(data=data_to_filter)
        endpoint = GoogleURLEnum.SEARCH_BOOKS.value
        url = f'{GOOGLE_API_URL}{endpoint}?q={query}' \
              f'&printType=books&key={GOOGLE_API_KEY}'

        async with session.get(url) as response:
            book = await response.text()
            return book

    def build_query(self, *, data: Dict[str, Any]) -> str:
        query = ''
        for _filter in data:
            filter_str = self.build_filter(
                filter_name=_filter,
                filter_value=data[_filter]
            )
            if not filter_str:
                continue

            query += filter_str

        return query

    @staticmethod
    def build_filter(
        *,
        filter_name: str,
        filter_value: str
    ) -> Optional[str]:
        filter_field = FILTER_LIST_IN_SEARCH.get(filter_name)
        if not filter_field:
            return

        filter_value = filter_value.replace(' ', '+')
        return f'{filter_field}{filter_value}+'


from typing import Any, Dict, Optional

from aiohttp import ClientSession

from apps.data_source.abstractions.abstract_search import SearchMethod
from apps.data_source.integrations.open_libra.constants import \
    OpenLibraURLEnum, OPEN_LIBRA_API_URL, FILTER_LIST_IN_SEARCH


class OpenLibraSearchClient(SearchMethod):

    async def get_books(
        self,
        data_to_filter: Dict[str, Any],
        session: ClientSession
    ) -> Optional[str]:
        query = self.build_query(data=data_to_filter)
        endpoint = OpenLibraURLEnum.SEARCH_BOOKS.value
        url = f'{OPEN_LIBRA_API_URL}{endpoint}/?{query}?json=true'

        async with session.get(url) as response:
            books = await response.text()
            return books

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

        return f'{filter_field}="{filter_value}"&'

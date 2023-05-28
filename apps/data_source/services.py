import logging
import asyncio
import json
from typing import List, Optional, Dict, Union

import aiohttp

from apps.data_source.integrations.google.search_client import \
    GoogleSearchClient
from apps.data_source.integrations.google.search_utils import GoogleSearchUtil
from apps.data_source.integrations.open_libra.open_libra_client import \
    OpenLibraSearchClient
from apps.data_source.integrations.open_libra.search_utils import \
    OpenLibraryUtil
from utils.serializers import BookDTO


logger = logging.getLogger(__name__)


class SearchBook:

    async def search_and_parser_book_data(
        self,
        *,
        params_to_search: Dict[str, Union[str, int]]
    ) -> Optional[List[BookDTO]]:
        source_search_lst = await self.search_book_in_sources(
            params_to_search=params_to_search
        )
        google_data = self.serialize_google_data(
            data=source_search_lst[0]
        )
        open_library_data = self.serialize_open_library_data(
            data=source_search_lst[1]
        )
        google_data.extend(open_library_data)

        return google_data

    @staticmethod
    async def search_book_in_sources(
        *,
        params_to_search: Dict[str, Union[str, int]]
    ) -> Optional[List[str]]:
        async with aiohttp.ClientSession() as session:
            google_client = GoogleSearchClient()
            open_library_client = OpenLibraSearchClient()
            google_search_async = google_client.get_books(
                data_to_filter=params_to_search,
                session=session
            )
            open_library_search_async = open_library_client.get_books(
                data_to_filter=params_to_search,
                session=session
            )

            tasks = [
                google_search_async,
                open_library_search_async
            ]

            data_list = await asyncio.gather(*tasks)
            return data_list

    @staticmethod
    def serialize_google_data(data: str) -> Optional[List[BookDTO]]:
        try:
            formatted_source_data = json.loads(data)
            total_items = formatted_source_data.get('totalItems', 0)
            if total_items <= 0:
                return []
            return GoogleSearchUtil.parser_response(
                items=formatted_source_data['items']
            )
        except Exception as e:
            logger.error(f'SearchBook :: serialize_google_data :: {e}')
            return []

    @staticmethod
    def serialize_open_library_data(data: str) -> Optional[List[BookDTO]]:
        try:
            formatted_source_data = json.loads(data)
            return OpenLibraryUtil.parser_response(
                items=formatted_source_data
            )
        except Exception as e:
            logger.error(f'SearchBook :: serialize_open_library_data :: {e}')
            return []

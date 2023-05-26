
from typing import Any, Dict, Optional, List

from apps.data_source.integrations.open_libra.constants import \
    OpenLibraURLEnum, OPEN_LIBRA_API_URL
from apps.data_source.integrations.open_libra.exceptions import \
    OpenLibraSearchConnectionError, OpenLibraSearchServerError

from utils.rest_api_client import RestAPIClient


class OpenLibraSearchService:

    def __init__(
        self,
        rest_api_client: RestAPIClient = RestAPIClient()
    ):
        self.rest_api = rest_api_client

    def get_books(self, query: str) -> Optional[List[Dict[str, Any]]]:

        endpoint = OpenLibraURLEnum.SEARCH_BOOKS.value
        url = f'{OPEN_LIBRA_API_URL}{endpoint}/?{query}?json=true'
        print('*' * 30)
        print(url)
        print('*' * 30)
        status_code, data = self.rest_api.request_get(url=url)

        if 300 <= status_code <= 499:
            raise OpenLibraSearchConnectionError(data)

        if status_code >= 500:
            raise OpenLibraSearchServerError(data)

        return data

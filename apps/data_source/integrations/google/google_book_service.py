from typing import Any, Dict, Optional

from apps.data_source.integrations.google.constants import (
    GOOGLE_API_URL,
    GOOGLE_API_KEY, GoogleURLEnum
)
from apps.data_source.integrations.google.exceptions import \
    GoogleSearchConnectionError, GoogleSearchServerError
from utils.rest_api_client import RestAPIClient


class GoogleSearchService(RestAPIClient):

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def get_books(self, query: str) -> Optional[Dict[str, Any]]:
        endpoint = GoogleURLEnum.SEARCH_BOOKS.value
        url = f'{GOOGLE_API_URL}{endpoint}?q={query}' \
              f'&printType=books&key={GOOGLE_API_KEY}'
        status_code, data = self.request_get(
            url=url,
            headers=self.HEADERS
        )

        if 300 <= status_code <= 499:
            raise GoogleSearchConnectionError(data)

        if status_code >= 500:
            raise GoogleSearchServerError(data)

        return data

import logging
from typing import Dict, Any, Union, Tuple, Optional
from requests import get, post

logger = logging.getLogger(__name__)


class RestAPIClient:

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def request_get(
        self,
        *,
        url: str,
        headers: Dict[str, Any] = None
    ) -> Tuple[int, Union[Dict, None]]:

        if not headers:
            headers = self.HEADERS

        response = get(
            url=url,
            headers=headers
        )
        return response.status_code, response.json()

    def request_post(
        self,
        *,
        url: str,
        data: Dict[str, Any],
        kwargs: Optional[Dict[str, Any]] = dict,
        headers: Dict[str, Any] = None
    ) -> Tuple[int, Union[Dict, None]]:

        if not headers:
            headers = self.HEADERS

        response = post(
            url=url,
            headers=headers,
            data=data,
            **kwargs
        )
        return response.status_code, response.json()

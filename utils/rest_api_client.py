import logging
from typing import Dict, Any, Union, Tuple, Optional
from requests import get, post

logger = logging.getLogger(__name__)


class RestAPIClient:

    @staticmethod
    def request_get(
        *,
        url: str,
        headers: Dict[str, Any]
    ) -> Tuple[int, Union[Dict, None]]:
        response = get(
            url=url,
            headers=headers
        )
        return response.status_code, response.json()

    @staticmethod
    def request_post(
        *,
        url: str,
        headers: Dict[str, Any],
        data: Dict[str, Any],
        kwargs: Optional[Dict[str, Any]] = dict
    ) -> Tuple[int, Union[Dict, None]]:
        response = post(
            url=url,
            headers=headers,
            data=data,
            **kwargs
        )
        return response.status_code, response.json()

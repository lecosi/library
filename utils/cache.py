import logging

from typing import Optional, Dict, Any, Union

from django.core.cache import cache

from utils.constants import DEFAULT_CACHE_EXPIRATION_TIME

logger = logging.getLogger(__name__)


class CacheService:

    @staticmethod
    def get_cache_data_by_key(
        *,
        key_name: str
    ) -> Optional[Dict[str, Any]]:
        try:
            return cache.get(key_name, None)

        except Exception as e:
            logger.error(f'CacheService :: get_cache_data_by_key '
                         f':: key_name {key_name} :: {e}')
            return

    @staticmethod
    def set_data(
        *,
        key_name: str,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:

        try:
            return cache.get_or_set(
                key_name, data, DEFAULT_CACHE_EXPIRATION_TIME)

        except Exception as e:
            logger.error(f'CacheService :: set_data '
                         f':: key_name {key_name} :: {e}')
            return

    @staticmethod
    def delete_cached_data_by_key(
        *,
        key_name: str,
    ) -> Union[None]:

        try:
            return cache.delete(key_name)

        except Exception as e:
            logger.error(f'CacheService :: delete_cached_data_by_key '
                         f':: key_name {key_name} :: {e}')
            return

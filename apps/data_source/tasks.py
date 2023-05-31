import logging
import asyncio
from typing import List, Union

from utils.cache import CacheService
from utils.serializers import BookDTO


logger = logging.getLogger(__name__)


def save_search_data_in_cache_task(
    *,
    book_list: List[BookDTO]
) -> Union[None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    group = asyncio.gather(
        *[process_to_save_book_in_cache(book=book) for book in book_list]
    )

    loop.run_until_complete(group)
    loop.close()


async def process_to_save_book_in_cache(
    *,
    book: BookDTO
) -> Union[None]:
    try:
        key_name = book.business_key()
        data = book.parse_to_dict()
        cache_service = CacheService()
        cache_service.set_data(key_name=key_name, data=data)
    except Exception as e:
        logger.error(f'process_to_save_book_in_cache :: {e}')
        return

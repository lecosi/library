
from apps.data_source.factories.constants import SearchSourceTypeEnum
from apps.data_source.integrations.google.search_client import \
    GoogleSearchClient
from apps.data_source.integrations.open_libra.open_libra_client import \
    OpenLibraSearchClient


class SearchFactory:
    @staticmethod
    def get_search_source(*, source_type: int):
        if source_type == SearchSourceTypeEnum.GOOGLE_BOOKS.value:
            return GoogleSearchClient()

        elif source_type == SearchSourceTypeEnum.OPEN_LIBRA.value:
            return OpenLibraSearchClient()

        raise ValueError('search source not defined')

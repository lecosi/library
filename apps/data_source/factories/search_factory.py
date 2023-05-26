
from apps.data_source.factories.constants import SearchSourceTypeEnum
from apps.data_source.integrations.google.search_service import GoogleSearch
from apps.data_source.integrations.open_libra.search_service import \
    OpenLibraSearch


class SearchFactory:
    @staticmethod
    def get_search_source(*, source_type: int):
        if source_type == SearchSourceTypeEnum.GOOGLE_BOOKS.value:
            return GoogleSearch()

        elif source_type == SearchSourceTypeEnum.OPEN_LIBRA.value:
            return OpenLibraSearch()

        raise ValueError('search source not defined')

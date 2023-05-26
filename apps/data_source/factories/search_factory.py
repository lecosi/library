from apps.data_source.factories.constants import SearchSourceTypeEnum
from apps.data_source.integrations.google.search_service import GoogleSearch


class SearchFactory:
    @staticmethod
    def get_search_source(*, source_type: int):
        if source_type == SearchSourceTypeEnum.GOOGLE_BOOKS.value:
            return GoogleSearch()

        elif source_type == SearchSourceTypeEnum.INTERNET_ARCHIVE.value:
            return None

        raise ValueError('search source not defined')

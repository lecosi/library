from enum import Enum

UNREGISTERED = 'NO REGISTRADO'


class SourceSearchTypeEnum(Enum):
    GOOGLE_SEARCH = 'google'
    OPEN_LIBRARY_SEARCH = 'open_library'


class SearchTypeEnum(Enum):
    INTERNAL_DB = 'internal_db'
    EXTERNAL_DB = 'external_db'
    INTERNAL_AND_EXTERNAL = 'internal_and_external_db'

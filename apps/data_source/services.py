import logging
import asyncio
import json
from typing import List, Optional, Dict, Union

import aiohttp
import dateparser
from rest_framework.exceptions import ValidationError

from apps.data_source.abstractions.abstract_data_source import BookMethod
from apps.data_source.integrations.constants import SearchTypeEnum
from apps.data_source.integrations.google.search_client import \
    GoogleSearchClient
from apps.data_source.integrations.google.search_utils import GoogleSearchUtil
from apps.data_source.integrations.open_libra.open_libra_client import \
    OpenLibraSearchClient
from apps.data_source.integrations.open_libra.search_utils import \
    OpenLibraryUtil
from apps.data_source.models import Book, Category, Author
from apps.data_source.tasks import save_search_data_in_cache_task
from utils.cache import CacheService
from utils.serializers import BookDTO

from apps.data_source import selectors


logger = logging.getLogger(__name__)


class ExternalSearchBook:

    async def search_and_parser_book_data(
        self,
        *,
        params_to_search: Dict[str, Union[str, int]]
    ) -> Optional[List[BookDTO]]:
        source_search_lst = await self.search_book_in_sources(
            params_to_search=params_to_search
        )
        google_data = self.serialize_google_data(
            data=source_search_lst[0]
        )
        open_library_data = self.serialize_open_library_data(
            data=source_search_lst[1]
        )
        google_data.extend(open_library_data)

        return google_data

    @staticmethod
    async def search_book_in_sources(
        *,
        params_to_search: Dict[str, Union[str, int]]
    ) -> Optional[List[str]]:
        async with aiohttp.ClientSession() as session:
            google_client = GoogleSearchClient()
            open_library_client = OpenLibraSearchClient()
            google_search_async = google_client.get_books(
                data_to_filter=params_to_search,
                session=session
            )
            open_library_search_async = open_library_client.get_books(
                data_to_filter=params_to_search,
                session=session
            )

            tasks = [
                google_search_async,
                open_library_search_async
            ]

            data_list = await asyncio.gather(*tasks)
            return data_list

    @staticmethod
    def serialize_google_data(data: str) -> Optional[List[BookDTO]]:
        try:
            formatted_source_data = json.loads(data)
            total_items = formatted_source_data.get('totalItems', 0)
            if total_items <= 0:
                return []
            return GoogleSearchUtil.parser_response(
                items=formatted_source_data['items']
            )
        except Exception as e:
            logger.error(f'SearchBook :: serialize_google_data :: {e}')
            return []

    @staticmethod
    def serialize_open_library_data(data: str) -> Optional[List[BookDTO]]:
        try:
            formatted_source_data = json.loads(data)
            return OpenLibraryUtil.parser_response(
                items=formatted_source_data
            )
        except Exception as e:
            logger.error(f'SearchBook :: serialize_open_library_data :: {e}')
            return []


class BookListService:
    def get_book_list(
        self,
        title: str = None,
        external_id: str = None,
        subtitle: str = None,
        editor: str = None,
        category: str = None,
        description: str = None,
        publication_date: str = None,
        author: str = None
    ):
        response_data = {
            'source': SearchTypeEnum.INTERNAL_AND_EXTERNAL.value,
            'data': []
        }
        internal_data_lst = self.search_from_internal_db(
            title=title,
            external_id=external_id,
            subtitle=subtitle,
            editor=editor,
            category=category,
            description=description,
            publication_date=publication_date,
            author=author
        )
        if internal_data_lst:
            response_data['source'] = SearchTypeEnum.INTERNAL_DB.value
            response_data['data'] = internal_data_lst
            return response_data

        external_data_lst = self.search_from_external_db(
            title=title,
            external_id=external_id,
            subtitle=subtitle,
            editor=editor,
            category=category,
            description=description,
            publication_date=publication_date,
            author=author
        )
        if external_data_lst:
            response_data['source'] = SearchTypeEnum.EXTERNAL_DB.value
            response_data['data'] = external_data_lst
            return response_data

        return response_data

    def search_from_internal_db(
        self,
        title: str = None,
        external_id: str = None,
        subtitle: str = None,
        editor: str = None,
        category: str = None,
        description: str = None,
        publication_date: str = None,
        author: str = None
    ) -> Optional[List[Dict[str, str]]]:

        query_for_orm = self.build_query_for_orm(
            title=title,
            external_id=external_id,
            subtitle=subtitle,
            editor=editor,
            category=category,
            description=description,
            publication_date=publication_date,
            author=author
        )
        if not query_for_orm:
            raise ValidationError({
                'component': 'BookService',
                'msg': 'you must select at least one filter'
            })

        book_lst_from_db = selectors.filter_books_by_params(
            params=query_for_orm
        )

        if not book_lst_from_db:
            return

        book_lst = []
        for book in book_lst_from_db:
            data = {
                'book_id': book.id,
                'title': book.title,
                'external_id': book.external_id,
                'subtitle': book.subtitle,
                'editor': book.editor,
                'category': book.category.values_list('name', flat=True),
                'description': book.description,
                'publication_date': book.publication_date,
                'author': book.author.values_list('name', flat=True)
            }
            book_lst.append(data)

        return book_lst

    def search_from_external_db(
        self,
        title: str = None,
        external_id: str = None,
        subtitle: str = None,
        editor: str = None,
        category: str = None,
        description: str = None,
        publication_date: str = None,
        author: str = None
    ) -> Optional[List[Dict[str, str]]]:
        query_data = self.build_query_data_for_external_source(
            title=title,
            external_id=external_id,
            subtitle=subtitle,
            editor=editor,
            category=category,
            description=description,
            publication_date=publication_date,
            author=author
        )

        search_book = ExternalSearchBook()
        search_result_lst = asyncio.run(
            search_book.search_and_parser_book_data(
                params_to_search=query_data
            )
        )
        if not search_result_lst:
            return

        save_search_data_in_cache_task(book_list=search_result_lst)

        data_lst = []
        for book in search_result_lst:
            data_lst.append(book.parse_to_dict())

        return data_lst

    @staticmethod
    def build_query_for_orm(
        title: str = None,
        external_id: str = None,
        subtitle: str = None,
        editor: str = None,
        category: str = None,
        description: str = None,
        publication_date: str = None,
        author: str = None
    ) -> Dict[str, str]:
        data = {}
        if title is not None:
            data['title__contains'] = title

        if external_id is not None:
            data['external_id'] = external_id

        if subtitle is not None:
            data['subtitle__contains'] = subtitle

        if editor is not None:
            data['editor__contains'] = editor

        if category is not None:
            data['categories__name__contains'] = category

        if description is not None:
            data['description__contains'] = description

        if publication_date is not None:
            data['publication_date__date'] = publication_date

        if author is not None:
            data['authors__name__contains'] = author

        return data

    @staticmethod
    def build_query_data_for_external_source(
        title: str = None,
        external_id: str = None,
        subtitle: str = None,
        editor: str = None,
        category: str = None,
        description: str = None,
        publication_date: str = None,
        author: str = None
    ) -> Dict[str, str]:
        data = {}
        if title is not None:
            data['title'] = title

        if external_id is not None:
            data['external_id'] = external_id

        if subtitle is not None:
            data['subtitle'] = subtitle

        if editor is not None:
            data['editor'] = editor

        if category is not None:
            data['category'] = category

        if description is not None:
            data['description'] = description

        if publication_date is not None:
            data['publication_date'] = publication_date

        if author is not None:
            data['author'] = author

        return data


class BookService(BookMethod):

    def create_book(
        self,
        book_id: str,
        source: str
    ) -> Optional[Book]:
        cache_service = CacheService()
        key_name = f'{source}_{book_id}'
        cached_data = cache_service.get_cache_data_by_key(key_name=key_name)
        if not cached_data:
            raise ValidationError({
                'component': 'BookService',
                'msg': f'book_id {book_id} not found data for create'
            })
        book_id = cached_data.get('id')
        book_qs = selectors.filter_book_by_external_id(
            book_external_id=book_id
        )
        if book_qs.exists():
            raise ValidationError({
                'component': 'BookService',
                'msg': f'book_id {book_id} already exists'
            })

        publication_date = cached_data.get('publication_date')
        if publication_date:
            publication_date = dateparser.parse(publication_date)

        new_book = Book.objects.create(
            title=cached_data['title'],
            external_id=book_id,
            subtitle=cached_data.get('subtitle'),
            editor=cached_data.get('editor'),
            description=cached_data.get('description'),
            publication_date=publication_date
        )

        categories = cached_data.get('categories', [])
        if categories:
            category_ins_lst = self.get_or_create_categories(
                categories=categories
            )
            new_book.category.add(*category_ins_lst)

        authors = cached_data.get('authors', [])
        if authors:
            author_ins_lst = self.get_or_create_authors(
                authors=authors
            )
            new_book.author.add(*author_ins_lst)

        return new_book

    @staticmethod
    def get_or_create_categories(
        *,
        categories: List[Dict[str, str]]
    ) -> List[Category]:
        category_lst = []
        for category_name in categories:
            category_ins, _ = Category.objects.get_or_create(
                name=category_name,
                defaults=dict(name=category_name)
            )
            category_lst.append(category_ins)

        return category_lst

    @staticmethod
    def get_or_create_authors(
        *,
        authors: List[Dict[str, str]]
    ) -> List[Author]:
        author_lst = []
        for author_name in authors:
            author_ins, _ = Author.objects.get_or_create(
                name=author_name,
                defaults=dict(name=author_name)
            )
            author_lst.append(author_ins)

        return author_lst

    def delete_book(
        self,
        book_id: str
    ) -> Optional[bool]:
        book_qs = selectors.filter_book_by_external_id(
            book_external_id=book_id
        )
        if not book_qs.exists():
            raise ValidationError({
                'component': 'Book',
                'msg': 'Book not found'
            })

        book_qs.delete()

        return True

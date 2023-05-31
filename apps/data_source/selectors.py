from typing import Dict, Any

from django.db.models import QuerySet

from apps.data_source.models import Book


def filter_book_by_external_id(*, book_external_id: str) -> 'QuerySet[Book]':
    return Book.objects.filter(external_id=book_external_id)


def filter_books_by_params(*, params: Dict[str, Any]) -> 'QuerySet[Book]':
    return Book.objects.filter(**params)

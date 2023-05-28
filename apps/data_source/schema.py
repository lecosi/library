import asyncio

import graphene
from graphene import String

from graphene_django.types import DjangoObjectType

from .models import Book, Category, Author
from .services import SearchBook


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"


class Query:
    book = graphene.Field(
        BookType,
        tittle=graphene.String()
    )
    all_books = graphene.List(BookType)
    all_books_async = String()

    def resolve_all_books(self, info, **kwargs):
        title = kwargs.get("title")

        if title is not None:
            return Book.objects.filter(title__contains=title)

        return Book.objects.all()

    async def resolve_all_books_async(self, info, **kwargs):
        #title = kwargs.get("title")
        #search = SearchBook()
        #await search.search_books_in_apis({})
        await asyncio.sleep(1)

        return "Hello world"

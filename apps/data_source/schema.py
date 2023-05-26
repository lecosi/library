
import graphene

from graphene_django.types import DjangoObjectType

from .models import Book, Category, Author


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

    def resolve_all_books(self, info, **kwargs):
        title = kwargs.get("title")

        if title is not None:
            return Book.objects.filter(title__contains=title)

        return Book.objects.all()

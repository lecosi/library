from apps.authentication.authenticator import JWTAuthenticator
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED, HTTP_204_NO_CONTENT
)
from rest_framework.views import APIView

from apps.data_source.serializers import (
    InputCreateBookSerializer,
    InputSearchBookSerializer
)
from apps.data_source.services import BookListService, BookService


class SearchBookView(APIView):
    book_service = BookListService()
    input_serializer = InputSearchBookSerializer

    authentication_classes = [JWTAuthenticator]

    def post(self, request):
        input_serializer = self.input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        response_data = self.book_service.get_book_list(
            **input_serializer.data
        )
        return Response(response_data, status=HTTP_200_OK)


class BookView(APIView):
    book_service = BookService()
    input_create_serializer = InputCreateBookSerializer

    authentication_classes = [JWTAuthenticator]

    def post(self, request):
        input_serializer = self.input_create_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        self.book_service.create_book(
            **input_serializer.data
        )
        return Response(status=HTTP_201_CREATED)

    def delete(self, request, book_id):
        self.book_service.delete_book(
            book_id=book_id
        )
        return Response(status=HTTP_204_NO_CONTENT)

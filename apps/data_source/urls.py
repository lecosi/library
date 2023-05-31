from django.urls import path

from .views import SearchBookView, BookView

urlpatterns = [
    path(
        '',
        view=SearchBookView.as_view(),
        name='get_book_list'
    ),
    path(
        'new/',
        view=BookView.as_view(),
        name='new_book'
    ),
    path(
        '<str:book_id>/delete/',
        view=BookView.as_view(),
        name='delete_book'
    ),
]

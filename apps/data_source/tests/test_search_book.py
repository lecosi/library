import pytest


@pytest.mark.django_db
class TestSearchBook:
    def test_search_book_success(
        self,
        user_initial
    ):
        user = user_initial

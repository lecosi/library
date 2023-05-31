from abc import ABC, abstractmethod


class BookMethod(ABC):

    @abstractmethod
    def create_book(
        self,
        id: str,
        source: str
    ):
        """abstract method for create a book"""

    @abstractmethod
    def delete_book(
        self,
        book_id: int
    ):
        """abstract method for delete a book"""
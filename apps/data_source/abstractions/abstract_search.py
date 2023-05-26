from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractSearch(ABC):

    @abstractmethod
    def search_books(self, data: Dict[str, Any]):
        pass

from abc import ABC, abstractmethod
from typing import Dict, Any

from aiohttp import ClientSession


class AbstractSearch(ABC):

    @abstractmethod
    def get_books(
        self,
        data: Dict[str, Any],
        session: ClientSession
    ):
        pass

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    content: str


class Fetcher(ABC):
    @abstractmethod
    async def fetch(self, url: str) -> HttpResponse:
        pass

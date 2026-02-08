from abc import ABC, abstractmethod


class PageRepository(ABC):
    @abstractmethod
    async def save(self, content: str, url: str, title: str) -> None:
        pass

    @abstractmethod
    async def search(
        self, url: str, title: str, page: int, page_size: int
    ) -> list[dict]:
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> dict:
        pass

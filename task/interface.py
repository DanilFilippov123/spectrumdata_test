from abc import ABC, abstractmethod


class TaskExecutor(ABC):
    @abstractmethod
    async def add_task(self, url: str, depth: int) -> None:
        pass

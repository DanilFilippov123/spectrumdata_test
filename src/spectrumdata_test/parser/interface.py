from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ParserResult:
    title: str
    body: str
    urls: list[str]


class Parser(ABC):
    @abstractmethod
    def parse(self, content: str, base_url: str) -> ParserResult:
        pass

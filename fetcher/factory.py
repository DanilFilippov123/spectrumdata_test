from fetcher.httpx_fetcher import HttpxFetcher
from fetcher.interface import Fetcher


def make_fetcher() -> Fetcher:
    return HttpxFetcher()

from spectrumdata_test.fetcher.httpx_fetcher import HttpxFetcher
from spectrumdata_test.fetcher.interface import Fetcher


def make_fetcher() -> Fetcher:
    return HttpxFetcher()

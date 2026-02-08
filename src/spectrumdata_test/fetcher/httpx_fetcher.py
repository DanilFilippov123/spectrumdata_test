from httpx import AsyncClient

from spectrumdata_test.fetcher.interface import Fetcher, HttpResponse


class HttpxFetcher(Fetcher):
    async def fetch(self, url: str) -> HttpResponse:
        async with AsyncClient() as client:
            response = await client.get(url)
            return HttpResponse(status_code=response.status_code, content=response.text)

from spectrumdata_test.fetcher.interface import Fetcher
from spectrumdata_test.parser.interface import Parser
from spectrumdata_test.repository.interface import PageRepository
from spectrumdata_test.task.error import ParsePageError
from spectrumdata_test.task.interface import TaskExecutor


class ParsePagesTask:
    def __init__(
        self,
        parser: Parser,
        fetcher: Fetcher,
        task_executor: TaskExecutor,
        page_repository: PageRepository,
    ) -> None:
        self._page_repository = page_repository
        self._task_executor = task_executor
        self._fetcher = fetcher
        self._parser = parser

    async def execute(self, url: str, depth: int) -> None:
        response = await self._fetcher.fetch(url)
        if not 200 <= response.status_code < 300:
            raise ParsePageError(f"Status code {response.status_code} is not OK")
        parsed_page = self._parser.parse(response.content, base_url=url)
        await self._page_repository.save(parsed_page.body, url, parsed_page.title)
        for url in parsed_page.urls:
            await self._task_executor.add_task(url, depth + 1)

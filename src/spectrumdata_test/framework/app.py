from fastapi import FastAPI

from spectrumdata_test.framework.scheme import (
    ParseTaskScheme,
    ParseResponseSchema,
    PageScheme,
    PageContentScheme,
)
from spectrumdata_test.repository.factory import make_page_repository
from spectrumdata_test.task_queue.asyncio_task_queue import AsyncioTaskQueue

app = FastAPI(title="Parser")


@app.post("/parse")
async def parse(task: ParseTaskScheme) -> ParseResponseSchema:
    task_queue = AsyncioTaskQueue(
        url=task.url.unicode_string(),
        depth=task.depth,
        max_concurrency=task.max_concurrency,
    )
    return ParseResponseSchema(uuid=task_queue.uuid)


@app.post("/pages", response_model=list[PageScheme])
async def find_pages(
    url: str = "", title: str = "", page: int = 1, page_size: int = 10
) -> list[dict]:
    """
    url - Часть или полный url для поиска по url\n
    title - Часть или полный title для поиска по title
    """
    return await make_page_repository().search(
        url=url, title=title, page=page, page_size=page_size
    )


@app.get("/pages", response_model=PageContentScheme)
async def get_page(url: str) -> dict:
    return await make_page_repository().get_by_url(url=url)

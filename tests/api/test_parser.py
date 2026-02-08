import asyncio

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import HttpUrl
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture
from starlette.testclient import TestClient

from spectrumdata_test.framework.app import app
from spectrumdata_test.framework.scheme import ParseTaskScheme
from spectrumdata_test.task_queue.asyncio_task_queue import TASKS


async def test_parser(
    mocker: MockerFixture,
    mongo_collection: AsyncIOMotorCollection,
    httpx_mock: HTTPXMock,
async_client
):
    example_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
      <meta charset="UTF-8">
      <title>Пример HTML</title>
    </head>
    <body>
      <h1>Небольшой заголовок</h1>
    
      <p>
        Это простой текст для примера HTML-страницы.
      </p>
    
      <p>
        <a href="/about.html">Относительная ссылка</a><br>
        <a href="https://example.com">Абсолютная ссылка</a>
      </p>
    </body>
    </html>
    """
    #client = TestClient(app)
    mocker.patch(
        "spectrumdata_test.repository.mongo_repository.pages_collection",
        new=mongo_collection,
    )
    request = ParseTaskScheme(
        url=HttpUrl("https://example.com"), depth=0, max_concurrency=1
    )
    httpx_mock.add_response(text=example_html)

    response = await async_client.post("/parse", data=request.model_dump_json())
    await asyncio.gather(*(y for x in TASKS.values() for y in x.workers), return_exceptions=True)

    assert response.status_code == 200
    pages = await mongo_collection.find().to_list()
    assert len(pages) == 1
    page = pages[0]
    del page["_id"]
    assert page == {
        "url": "https://example.com/",
        "content": example_html,
        "title": "Пример HTML"
    }

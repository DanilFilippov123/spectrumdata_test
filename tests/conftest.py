import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

from spectrumdata_test.framework.app import app
from spectrumdata_test.framework.settings import settings

TEST_DB_NAME = "test_db"


@pytest.fixture
async def mongo_client():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    yield client
    client.close()


@pytest.fixture
async def test_db(mongo_client):
    return mongo_client[TEST_DB_NAME]


@pytest.fixture
async def mongo_collection(test_db):
    collection_name = "test_collection"

    await test_db.drop_collection(collection_name)

    collection = test_db[collection_name]
    yield collection


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

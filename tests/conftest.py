import uuid

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from framework.settings import settings

TEST_DB_NAME = "test_db"


@pytest.fixture(scope="session")
def mongo_client():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    yield client
    client.close()


@pytest.fixture(scope="session")
def test_db(mongo_client):
    return mongo_client[TEST_DB_NAME]


@pytest.fixture
async def mongo_collection(test_db):
    collection_name = f"test_collection_{uuid.uuid4().hex}"
    collection = test_db[collection_name]

    yield collection

    await test_db.drop_collection(collection_name)

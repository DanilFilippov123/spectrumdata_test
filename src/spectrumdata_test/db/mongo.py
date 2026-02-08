from motor.motor_asyncio import AsyncIOMotorClient

from spectrumdata_test.framework.settings import settings

async_client = AsyncIOMotorClient(settings.DATABASE_URL)
db = async_client.get_database(settings.DB_NAME)
pages_collection = db.get_collection("pages")

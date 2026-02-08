from spectrumdata_test.repository.interface import PageRepository
from spectrumdata_test.repository.mongo_repository import MongoPageRepository


def make_page_repository() -> PageRepository:
    return MongoPageRepository()

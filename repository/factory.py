from repository.interface import PageRepository
from repository.mongo_repository import MongoPageRepository


def make_page_repository() -> PageRepository:
    return MongoPageRepository()

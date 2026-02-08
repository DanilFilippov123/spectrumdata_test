import re

from spectrumdata_test.db.mongo import pages_collection
from spectrumdata_test.repository.interface import PageRepository


class MongoPageRepository(PageRepository):
    async def save(self, content: str, url: str, title: str) -> None:
        return await pages_collection.replace_one(
            {"url": url}, {"url": url, "content": content, "title": title}, upsert=True
        )

    def _make_query(self, url: str, title: str) -> dict:
        conditions = []

        if url:
            conditions.append({"url": {"$regex": re.compile(url, re.IGNORECASE)}})

        if title:
            conditions.append({"title": {"$regex": re.compile(title, re.IGNORECASE)}})

        if not conditions:
            return {}

        if len(conditions) == 1:
            return conditions[0]

        return {"$or": conditions}

    async def search(
        self, url: str, title: str, page: int, page_size: int
    ) -> list[dict]:
        query = self._make_query(url=url, title=title)

        skip = (page - 1) * page_size

        return await (
            pages_collection.search(query, {"url": 1, "title": 1, "_id": 0})
            .sort("_id", 1)
            .skip(skip)
            .limit(page_size)
        ).to_list(length=page_size)

    async def get_by_url(self, url: str) -> dict:
        return await pages_collection.find_one({"url": url})

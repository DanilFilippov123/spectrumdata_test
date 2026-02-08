from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field


class ParseTaskScheme(BaseModel):
    url: HttpUrl
    depth: int = Field(ge=0)
    max_concurrency: int = Field(ge=1)


class ParseResponseSchema(BaseModel):
    uuid: UUID


class PageScheme(BaseModel):
    url: HttpUrl
    title: str


class PageContentScheme(PageScheme):
    content: str

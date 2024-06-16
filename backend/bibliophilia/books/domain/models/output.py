from bibliophilia.books.domain.models.basic import BookBase, OverExtendedBookBase
from backend.bibliophilia.books.domain.models.basic import BookBase, ExtendedBookBase


class BookCard(BookBase):
    idx: int
    title: str
    author: list[str]
    genre: list[str]
    image_url: str


class BookInfo(OverExtendedBookBase):
    image_url: str
    formats: list[str] = []

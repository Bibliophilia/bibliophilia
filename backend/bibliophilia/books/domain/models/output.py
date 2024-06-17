from bibliophilia.books.domain.models.basic import BookBase, OverExtendedBookBase


class BookCard(BookBase):
    idx: int
    title: str
    author: list[str]
    genre: list[str]
    image_url: str


class BookInfo(OverExtendedBookBase):
    image_url: str
    formats: list[str] = []

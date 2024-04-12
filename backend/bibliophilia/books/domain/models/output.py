from bibliophilia.books.domain.models.basic import BookBase, FileFormat, ExtendedBookBase


class BookCard(BookBase):
    idx: int
    title: str
    author: str
    image_url: str


class BookInfo(ExtendedBookBase):
    image_url: str
    formats: list[str] = []

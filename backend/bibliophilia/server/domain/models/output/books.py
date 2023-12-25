from bibliophilia.server.domain.models.basic.books import BookBase, FileFormat


class BookCard(BookBase):
    idx: int
    title: str
    author: str
    image_url: str

class BookInfo(BookBase):
    image_url: str
    formats: list[str] = []

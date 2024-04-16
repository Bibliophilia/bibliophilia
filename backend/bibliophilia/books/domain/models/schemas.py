from sqlmodel import Field, Relationship

from bibliophilia.books.domain.models.basic import ExtendedBookBase, FileFormat, BookFileBase
from bibliophilia.books import settings


class Book(ExtendedBookBase, table=True):
    __tablename__ = "books"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})

    files: list["BookFile"] = Relationship(back_populates="book")

    @property
    def image_url(self) -> str:
        return f"{settings.URL}/images/{self.idx}.{settings.IMAGE_EXTENSION}"

    @property
    def image_path(self) -> str:
        return f"{settings.IMAGES_PATH}/{self.idx}.{settings.IMAGE_EXTENSION}"


class BookFile(BookFileBase, table=True):
    __tablename__ = "files"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    format: FileFormat
    book_idx: int = Field(foreign_key="books.idx")

    book: Book = Relationship(back_populates="files")

    @property
    def bookfile_path(self) -> str:
        return f"{settings.FILES_PATH}/{self.book_idx}.{self.format.value}"

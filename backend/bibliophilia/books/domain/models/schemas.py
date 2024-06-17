from sqlmodel import Field, Relationship

from bibliophilia.books.domain.models.basic import ExtendedBookBase, FileFormat, BookFileBase, AuthorBase, GenreBase
from bibliophilia.books import settings


class Book(ExtendedBookBase, table=True):
    __tablename__ = "books"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    genre: list["Genre"] = Relationship(back_populates="book")
    author: list["Author"] = Relationship(back_populates="book")
    files: list["BookFile"] = Relationship(back_populates="book")
    reviews: list["Review"] = Relationship(back_populates="book")

    @property
    def image_url(self) -> str:
        return f"{settings.URL}/images/{self.idx}.{settings.IMAGE_EXTENSION}"

    @property
    def image_path(self) -> str:
        return f"{settings.IMAGES_PATH}/{self.idx}.{settings.IMAGE_EXTENSION}"

    @property
    def authors(self):
        return [author for author in self.author if author.book_idx == self.idx]

    @property
    def genres(self):
        return [genre for genre in self.genre if genre.book_idx == self.idx]


class BookFile(BookFileBase, table=True):
    __tablename__ = "files"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    format: FileFormat
    book_idx: int = Field(foreign_key="books.idx")

    book: Book = Relationship(back_populates="files")

    @property
    def bookfile_path(self) -> str:
        return f"{settings.FILES_PATH}/{self.book_idx}.{self.format.value}"


class Genre(GenreBase, table=True):
    __tablename__ = "genres"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    book_idx: int = Field(foreign_key="books.idx")
    book: Book = Relationship(back_populates="genre")


class Author(AuthorBase, table=True):
    __tablename__ = "authors"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    book_idx: int = Field(foreign_key="books.idx")
    book: Book = Relationship(back_populates="author")

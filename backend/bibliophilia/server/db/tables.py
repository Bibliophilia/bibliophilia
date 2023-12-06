from enum import Enum, auto
from typing import Optional

from fastapi import UploadFile
from sqlmodel import Field, Relationship
from sqlmodel import SQLModel


class BibilophiliaDB(SQLModel):
    pass


class FileFormat(Enum):
    PDF = auto()
    TXT = auto()
    EPUB = auto()
    DOC = auto()


# ==================== Book ====================
class BookBase(BibilophiliaDB):
    title: str
    author: str
    description: str


class Book(BookBase, table=True):
    __tablename__ = "books"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    title: str
    author: str
    description: str
    image_url: str = ""
    files: list["BookFile"] = Relationship(back_populates="book")

    @property
    def formats(self) -> list[str]:
        unique_formats = set(file.file_format.name for file in self.files)
        return list(unique_formats)


class BookCreate(BookBase):
    pass
    # image: Optional[UploadFile] = None
    # files: Optional[list[UploadFile]] = []


class BookES(BookBase):
    tokens: list[str]


class BookCard(BibilophiliaDB):
    title: str
    author: str
    image_url: str

class BookInfo(BookBase):
    image_url: str


# ==================== BookFile ====================
class BookFile(BibilophiliaDB, table=True):
    __tablename__ = "files"
    file_path: str = Field(primary_key=True)
    file_format: FileFormat
    book_idx: int = Field(foreign_key="books.idx")

    book: Book = Relationship(back_populates="files")

from enum import Enum, auto
from typing import Optional

from fastapi import UploadFile
from sqlmodel import Field, Relationship
from sqlmodel import SQLModel


class BibilophiliaDB(SQLModel):
    pass


class FileFormat(Enum):
    PDF = "pdf"
    TXT = "txt"
    EPUB = "epub"
    DOC = "doc"

    @staticmethod
    def get_by_name(name: str):
        for item in FileFormat:
            if item.value == name:
                return item
        raise ValueError("No such FileFormat")


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
        unique_formats = set(file.format.value for file in self.files)
        return list(unique_formats)


class BookCreate(BookBase):
    image_file: Optional[UploadFile]
    files: list[UploadFile]


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
    path: str = Field(primary_key=True)
    format: FileFormat
    book_idx: int = Field(foreign_key="books.idx")

    book: Book = Relationship(back_populates="files")

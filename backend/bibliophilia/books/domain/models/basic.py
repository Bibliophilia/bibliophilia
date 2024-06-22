from enum import Enum
from typing import Optional

from backend.bibliophilia.core.models import BPModel


class BookBase(BPModel):
    title: str


class ExtendedBookBase(BookBase):
    year: int
    description: str


class OverExtendedBookBase(ExtendedBookBase):
    author: list[str]
    genre: list[str]


class BookFileBase(BPModel):
    book_idx: int


class FileFormat(Enum):
    PDF = "pdf"
    TXT = "txt"
    EPUB = "epub"
    DOC = "doc"

    @staticmethod
    def get_by_name(name: str) -> Optional["FileFormat"]:
        for item in FileFormat:
            if item.value == name:
                return item
        return None


class FacetBase(BPModel):
    book_idx: int


class GenreBase(FacetBase):
    book_idx: int


class AuthorBase(FacetBase):
    book_idx: int


class TokenizedBook(BPModel):
    book_idx: int
    tokens: list[str]

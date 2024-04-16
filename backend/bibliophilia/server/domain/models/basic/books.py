from enum import Enum
from typing import Optional

from backend.bibliophilia.server.domain.models import BPModel


class BookBase(BPModel):
    title: str
    author: str

class ExtendedBookBase(BookBase):
    description: str

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

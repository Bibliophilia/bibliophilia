from abc import abstractmethod, ABC
from typing import Optional

from bibliophilia.server.domain.models.basic.books import FileFormat
from bibliophilia.server.domain.models.input.books import BookCreate
from bibliophilia.server.domain.models.schemas.books import Book, BookFile


class BookRepository(ABC):

    @abstractmethod
    def create_book(self, book: BookCreate) -> Optional[Book]:
        pass

    @abstractmethod
    def read_book(self, idx: int) -> Optional[Book]:
        pass

    @abstractmethod
    def get_book_formats(self, idx: int) -> set[FileFormat]:
        pass

    @abstractmethod
    def read_books(self, ids: list[int]) -> list[Book]:
        pass

    @abstractmethod
    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        pass


class SearchRepository(ABC):
    @abstractmethod
    def base_search(self, query: str) -> [int]:
        pass

    @abstractmethod
    def semantic_search(self, tokens: list[float]):
        pass

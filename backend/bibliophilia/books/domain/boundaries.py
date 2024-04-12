from abc import abstractmethod, ABC
from typing import Optional

from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate
from bibliophilia.books.domain.models.schemas import Book, BookFile


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

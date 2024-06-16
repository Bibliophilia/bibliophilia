from abc import abstractmethod, ABC
from typing import Optional

from bibliophilia.books.domain.entity.facet import Facet
from bibliophilia.books.domain.models.basic import FileFormat, TokenizedBook
from bibliophilia.books.domain.models.input import BookCreate, ImageFileSave, BookFileSave
from bibliophilia.books.domain.models.schemas import Book, BookFile


class BookRepository(ABC):

    @abstractmethod
    def create_book(self, book: BookCreate) -> Optional[Book]:
        pass

    @abstractmethod
    def add_rights(self, credentials: Credentials, book_idx: int, user_idx: int):
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

    @abstractmethod
    def create_image(self, image: ImageFileSave) -> str:
        pass

    @abstractmethod
    def create_bookfile(self, bookfile: BookFileSave) -> Optional[BookFile]:
        pass

    @abstractmethod
    def is_tokenized(self, idx: int) -> bool:
        pass

    @abstractmethod
    def update_book(self, book: BookCreate) -> bool:
        pass


class SearchRepository(ABC):
    @abstractmethod
    def base_search(self, query: str, filter=None) -> [int]:
        pass

    @abstractmethod
    def semantic_search(self, tokens: list[float], filter=None):
        pass

    @abstractmethod
    def read_hints(self, query: str, facet: Facet) -> list[str]:
        pass

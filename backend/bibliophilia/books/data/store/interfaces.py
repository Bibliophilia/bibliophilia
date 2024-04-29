from abc import abstractmethod, ABC
from typing import Optional

from bibliophilia.books.domain.entity.facet import Facet
from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate, BookFileCreate, BookSearch, BookFileSave, ImageFileSave
from bibliophilia.books.domain.models.schemas import Book, BookFile


class FSBookStorage(ABC):
    @abstractmethod
    def save_bookfile(self, bookfile: BookFileSave) -> bool:
        pass

    @abstractmethod
    def get_bookfile(self, book: BookFile) -> Optional[bytes]:
        pass

    @abstractmethod
    def delete_bookfile(self, book: BookFile) -> bool:
        pass

    @abstractmethod
    def save_bookimage(self, bookimage: ImageFileSave) -> Optional[str]:
        pass

    @abstractmethod
    def delete_bookimage(self, book_idx: int) -> bool:
        pass


class DBBookStorage(ABC):
    @abstractmethod
    def create_book(self, book: BookCreate) -> Optional[Book]:
        pass

    @abstractmethod
    def read_book(self, idx: int = None) -> Optional[Book]:
        pass

    @abstractmethod
    def get_book_formats(self, idx: int) -> set[FileFormat]:
        pass

    @abstractmethod
    def create_bookfile(self, book: BookFileCreate) -> Optional[BookFile]:
        pass

    @abstractmethod
    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        pass

    @abstractmethod
    def get_all_formats(self, book_idx: int) -> set[FileFormat]:
        pass

    @abstractmethod
    def remove_book(self, book: Book) -> bool:
        pass

    @abstractmethod
    def remove_bookfile(self, bookfile: BookFile) -> bool:
        pass

    @abstractmethod
    def read_books(self, idxs: list[int]) -> list[Book]:
        pass


class SearchBookStorage(ABC):
    @abstractmethod
    def index_book(self, book_idx: int, es_book: BookSearch) -> bool:
        pass


class SearchStorage(ABC):
    @abstractmethod
    def base_search(self, query: str, filter=None) -> [int]:
        pass

    @abstractmethod
    def semantic_search(self, tokens: list[float], filter=None) -> [int]:
        pass

    @abstractmethod
    def read_hints(self, query: str, facet: Facet):
        pass

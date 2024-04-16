import logging
from typing import Optional

from bibliophilia.books.data.store.interfaces import FSBookStorage, SearchBookStorage, DBBookStorage, SearchStorage
from bibliophilia.books.domain.boundaries import BookRepository, SearchRepository
from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate, BookSearch, BookFileCreate, BookFileSave, ImageFileSave
from bibliophilia.books.domain.models.schemas import Book, BookFile


class BookRepositoryImpl(BookRepository):
    def __init__(self,
                 db_storage: DBBookStorage,
                 fs_storage: FSBookStorage,
                 search_storage: SearchBookStorage):
        self.db_storage = db_storage
        self.fs_storage = fs_storage
        self.search_storage = search_storage

    def create_book(self, book: BookCreate) -> Optional[Book]:
        logging.info("create_book() starting")
        db_bookfiles = []
        db_book = self.db_storage.create_book(book)
        if not db_book:
            logging.info("Error while creating book at DBBookStorage")
            self._rollback_book(db_book, db_bookfiles)
            return None
        is_indexed = self.search_storage.index(db_book.idx, BookSearch(title=book.title,
                                                                       author=book.author,
                                                                       description=book.description,
                                                                       tokens=book.tokens))
        if not is_indexed:
            logging.info("Error while indexing book at SearchStorage")
            self._rollback_book(db_book, db_bookfiles)
            return None
        is_saved = self.fs_storage.save_bookimage(ImageFileSave(book_idx=db_book.idx,
                                                                image=book.image))
        if not is_saved:
            logging.info("Error while saving book image at FSBookStorage")
            self._rollback_book(db_book, db_bookfiles)
            return None

        for file in book.files:
            filename = file.filename
            file_extension = filename.split('.')[-1]
            logging.info(f"File name: {filename}")
            logging.info(f"File format: {file_extension}")
            if not FileFormat.get_by_name(file_extension):
                logging.info("Invalid book file format")
                self._rollback_book(db_book, db_bookfiles)
                return None
            logging.info(f"Saving to DB")
            db_bookfile = self.db_storage.create_bookfile(BookFileCreate(book_idx=db_book.idx,
                                                                         format=FileFormat.get_by_name(file_extension)))
            if not db_bookfile:
                logging.info("Error while saving book file at DBBookStorage")
                self._rollback_book(db_book, db_bookfiles)
                return None
            db_bookfiles.append(db_bookfile)
            logging.info(f"Saving to FS")
            is_saved = self.fs_storage.save_bookfile(BookFileSave(book_idx=db_book.idx,
                                                                  file=file))
            logging.info(f"fookfile is_saved:{is_saved}")
            if not is_saved:
                logging.info("Error while saving book file at FSBookStorage")
                self._rollback_book(db_book, db_bookfiles)
                return None
        return db_book

    def _rollback_book(self, db_book: Book, db_bookfiles: [BookFile]):
        logging.info("Book saving rollback")
        is_deleted = self.fs_storage.delete_bookimage(db_book.idx)
        if not is_deleted:
            raise Exception("Couldn't delete book image")
        is_removed = self.db_storage.remove_book(db_book)
        if not is_removed:
            raise Exception("Couldn't delete book")
        for prev_db_bookfile in db_bookfiles:
            is_removed = self.db_storage.remove_bookfile(prev_db_bookfile)
            is_deleted = self.fs_storage.delete_bookfile(prev_db_bookfile)
            if not is_removed or not is_deleted:
                raise Exception("Couldn't delete bookfile")

    def read_book(self, idx: int) -> Book:
        return self.db_storage.read_book(idx)

    def get_book_formats(self, idx: int) -> set[FileFormat]:
        return self.db_storage.get_book_formats(idx)

    def read_books(self, idxs: list[int]) -> list[Book]:
        return self.db_storage.read_books(idxs)

    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        return self.db_storage.read_bookfile(idx=idx, file_format=file_format)


class SearchRepositoryImpl(SearchRepository):
    def __init__(self, search_storage: SearchStorage):
        self.search_storage = search_storage

    def base_search(self, query: str) -> [int]:
        return self.search_storage.base_search(query=query)

    def semantic_search(self, tokens: list[float]):
        return self.search_storage.semantic_search(tokens=tokens)

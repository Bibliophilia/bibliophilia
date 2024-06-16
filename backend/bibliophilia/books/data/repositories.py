import logging
from typing import Optional

from backend.bibliophilia.books.data.store.interfaces import FSBookStorage, SearchBookStorage, DBBookStorage, SearchStorage
from backend.bibliophilia.books.domain.boundaries import BookRepository, SearchRepository
from backend.bibliophilia.books.domain.entity.facet import Facet
from backend.bibliophilia.books.domain.models.basic import FileFormat, FacetBase
from backend.bibliophilia.books.domain.models.input import (BookCreate, BookSearch, BookFileCreate, BookFileSave,
                                                    ImageFileSave,
                                                    GenreCreate, AuthorCreate)
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile
from backend.bibliophilia.books.data.store.interfaces import FSBookStorage, SearchBookStorage, DBBookStorage, SearchStorage
from backend.bibliophilia.books.domain.boundaries import BookRepository, SearchRepository
from backend.bibliophilia.books.domain.models.basic import FileFormat
from backend.bibliophilia.books.domain.models.input import BookCreate, BookSearch, BookFileCreate, BookFileSave, \
    ImageFileSave, Rights
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile


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
        db_facets = []
        db_book = self.db_storage.create_book(book)
        if not db_book:
            logging.info("Error while creating book at DBBookStorage")
            self._rollback_book(db_book, db_facets)
            return None

        is_indexed = self.search_storage.index_book(db_book.idx, BookSearch(title=book.title,
                                                                            year=book.year,
                                                                            publisher=book.publisher,
                                                                            description=book.description,
                                                                            author=book.author,
                                                                            genre=book.genre,
                                                                            tokens=book.tokens))
        if not is_indexed:
            logging.info("Error while indexing book at SearchStorage")
            self._rollback_book(db_book, db_facets)
            return None

        for author in book.author:
            db_author = self.db_storage.create_facet(value=AuthorCreate(book_idx=db_book.idx,
                                                                        name=author),
                                                     facet=Facet.author)
            db_facets.append(db_author)
            is_indexed = self.search_storage.index_facet(author, Facet.author)
            if not db_author or not is_indexed:
                logging.info("Error while creating author at DBBookStorage or indexing at SearchStorage")
                self._rollback_book(db_book, db_facets)
                return None

        for genre in book.genre:
            db_genre = self.db_storage.create_facet(value=GenreCreate(book_idx=db_book.idx,
                                                                      name=genre),
                                                    facet=Facet.genre)
            db_facets.append(db_genre)
            is_indexed = self.search_storage.index_facet(genre, Facet.genre)
            if not db_genre or not is_indexed:
                logging.info("Error while creating author at DBBookStorage or indexing at SearchStorage")
                self._rollback_book(db_book, db_facets)
                return None
        return db_book

    def create_image(self, image: ImageFileSave) -> str:
        url = self.fs_storage.save_bookimage(image)
        if not url:
            logging.info("Error while saving book image at FSBookStorage")
        return url

    def create_bookfile(self, bookfile: BookFileSave) -> Optional[BookFile]:
        filename = bookfile.file.filename
        file_extension = filename.split('.')[-1]
        logging.info(f"File name: {filename}")
        logging.info(f"File format: {file_extension}")
        if not FileFormat.get_by_name(file_extension):
            logging.info("Invalid book file format")
            return None
        logging.info(f"Saving to DB")
        db_bookfile = self.db_storage.create_bookfile(BookFileCreate(book_idx=bookfile.book_idx,
                                                                     format=FileFormat.get_by_name(file_extension)))
        if not db_bookfile:
            logging.info("Error while saving book file at DBBookStorage")
            return None
        logging.info(f"Saving to FS")
        is_saved = self.fs_storage.save_bookfile(BookFileSave(book_idx=bookfile.book_idx,
                                                              file=bookfile.file))
        logging.info(f"fookfile is_saved:{is_saved}")
        if not is_saved:
            logging.info("Error while saving book file at FSBookStorage")
            self._rollback_bookfile(db_bookfile)
            return None
        return db_bookfile

    def add_rights(self, rights: Rights, book_idx: int, user_idx: int):
        self.db_storage.create_book_rights(user_idx=user_idx, book_idx=book_idx, rights=rights)

    def delete_rights(self, book_idx: int):
        self.db_storage.delete_book_rights(book_idx)

    def _rollback_book(self, db_book: Book, db_facets: [FacetBase]):
        logging.info("Book saving rollback")
        is_deleted = self.fs_storage.delete_bookimage(db_book.idx)
        if not is_deleted:
            raise Exception("Couldn't delete book image")
        is_removed = self.db_storage.remove_book(db_book)
        if not is_removed:
            raise Exception("Couldn't delete book")
        is_deleted = self.search_storage.delete_indexed_book(db_book.idx)
        if not is_deleted:
            raise Exception("Couldn't delete book index")
        for db_facet in db_facets:
            is_removed = self.db_storage.remove_facet(db_facet)
            if not is_removed or not is_deleted:
                raise Exception("Couldn't delete facet")

    def _rollback_bookfile(self, db_bookfile: BookFile):
        is_removed = self.db_storage.remove_bookfile(db_bookfile)
        is_deleted = self.fs_storage.delete_bookfile(db_bookfile)
        if not is_removed or not is_deleted:
            raise Exception("Couldn't delete bookfile")

    def is_tokenized(self, idx: int) -> bool:
        # TODO
        pass

    def update_book(self, book: BookCreate) -> bool:
        # TODO
        pass

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

    def base_search(self, query: str, filter=None) -> [int]:
        return self.search_storage.base_search(query=query, filter=filter)

    def semantic_search(self, tokens: list[float], filter=None):
        return self.search_storage.semantic_search(tokens=tokens, filter=filter)

    def read_hints(self, query: str, facet: Facet) -> list[str]:
        return self.search_storage.read_hints(query=query, facet=facet)

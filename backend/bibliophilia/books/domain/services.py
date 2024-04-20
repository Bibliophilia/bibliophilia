import logging
from typing import Optional

from fastapi import status
from bibliophilia.books import settings
from bibliophilia.books.domain.boundaries import BookRepository, SearchRepository
from bibliophilia.books.domain.entity.facet import Facet
from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate
from bibliophilia.books.domain.models.output import BookInfo
from bibliophilia.books.domain.models.schemas import Book, BookFile

from bibliophilia.books.domain.utils.texttokeniser import TextTokeniser


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self.repository = book_repository

    def create(self, book: BookCreate) -> (Optional[int], status):
        # TODO: скорее всего сделать токенизацию асинхронной, т.к. долго выполняется
        book.tokens = TextTokeniser().book_to_tokens(book)
        book = self.repository.create_book(book)
        if book:
            logging.info(f"book created: {book.idx}")
            return book, status.HTTP_201_CREATED
        else:
            logging.info(f"book not created")
            return None, status.HTTP_409_CONFLICT

    def read_book(self, idx: int) -> Optional[BookInfo]:
        book = self.repository.read_book(idx)
        formats = self.repository.get_book_formats(idx)
        if book:
            return BookInfo(title=book.title,
                            author=book.author,
                            image_url=book.image_url,
                            description=book.description,
                            formats=[book_format.value for book_format in formats])
        return None

    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        return self.repository.read_bookfile(idx=idx, file_format=file_format)


class SearchService:
    def __init__(self, search_repository: SearchRepository, book_repository: BookRepository) -> None:
        self.search_repository = search_repository
        self.book_repository = book_repository

    def search(self, query: str, facets: list[{str: str}], page: int) -> list[Book]:
        # TODO: facets
        # Какой то слооожный поиск
        logging.info("Base Search started")
        ids = []
        base_search_ids = self.search_repository.base_search(query)
        ids.extend(base_search_ids)
        logging.info(f"Base Search finished:{ids}")
        logging.info("Semantic Search started")
        tokens = TextTokeniser().text_to_tokens(query)
        semantic_search_ids = self.search_repository.semantic_search(tokens)
        ids.extend(semantic_search_ids)
        logging.info(f"Semantic Search finished:{ids}")
        page_ids = []
        for item in ids:
            if item not in page_ids:
                page_ids.append(item)
        page_ids = page_ids[(settings.BOOKS_IN_PAGE * (page - 1)): (settings.BOOKS_IN_PAGE * page)]
        logging.info(f"Final books:{page_ids}")
        books = self.book_repository.read_books(page_ids)
        return books

    def read_facets(self) -> set[Facet]:
        return set(Facet)

    def read_hints(self, query: str, facet: str) -> list[str]:
        return self.search_repository.read_hints(query, Facet(facet))[:settings.MAX_HINTS]

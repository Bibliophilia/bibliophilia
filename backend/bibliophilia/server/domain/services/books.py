import logging
from typing import Optional

from fastapi import status
from bibliophilia.server import settings
from bibliophilia.server.domain.boundaries.books import BookRepository, SearchRepository
from bibliophilia.server.domain.models.basic.books import FileFormat
from bibliophilia.server.domain.models.input.books import BookCreate
from bibliophilia.server.domain.models.output.books import BookInfo
from bibliophilia.server.domain.models.schemas.books import Book, BookFile

from backend.bibliophilia.server.utils.parser import Parser


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self.repository = book_repository

    def create(self, book: BookCreate) -> (Optional[int], status):
        # TODO: скорее всего сделать токенизацию асинхронной, т.к. долго выполняется
        book.tokens = Parser().book_to_tokens(book)
        book = self.repository.create_book(book)
        logging.info(f"book created: {book.idx}")
        if book:
            return book, status.HTTP_201_CREATED
        else:
            return None, status.HTTP_409_CONFLICT

    def read_book(self, idx: int) -> Optional[BookInfo]:
        book = self.repository.read_book(idx)
        formats = self.repository.get_book_formats(idx)
        if book:
            return BookInfo(title=book.title,
                            author=book.author,
                            image_url=book.image_url,
                            formats=[book_format.value for book_format in formats])
        return None

    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        return self.repository.read_bookfile(idx=idx, file_format=file_format)


class SearchService:
    def __init__(self, search_repository: SearchRepository, book_repository: BookRepository) -> None:
        self.search_repository = search_repository
        self.book_repository = book_repository

    def search(self, query: str, page: int) -> list[Book]:
        # Какой то слооожный поиск
        ids = self.search_repository.base_search(query)
        page_ids = ids[settings.BOOKS_IN_PAGE * (page - 1)::settings.BOOKS_IN_PAGE * page + 1]
        books = self.book_repository.read_books(page_ids)

        # semantic search
        books_sem = []
        if len(books) < settings.BOOKS_IN_PAGE:
            ids = self.search_repository.semantic_search(query)
            # TODO: исправить индексы
            page_ids = ids[::settings.BOOKS_IN_PAGE - len(books)]
            books_sem, request_tokens = self.book_repository.read_books(page_ids)

            #здесь мы ищем книги, у которых больше всего совпадений с query
            books_priority = []
            for book in books_sem:
                tokens = book.tokens
                priority = 0
                for request_token in request_tokens:
                    for i, token in enumerate(tokens):
                        if token == request_token:
                            priority += i
                            break
                books_priority.append((book, priority))

            books_sem = books_priority.sort(key=lambda x: x[1])[0]

        return books + books_sem

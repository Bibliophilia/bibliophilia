import logging
from typing import Optional

from fastapi import status
from backend.bibliophilia.books.domain.entity.facet import Facet
from backend.bibliophilia.books.domain.models.basic import FileFormat, TokenizedBook
from backend.bibliophilia.books.domain.models.input import BookCreate, ImageFileSave, BookFileSave, BookUpdate, \
    BookSearch
from backend.bibliophilia.books.domain.models.output import BookInfo, BookCard
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile
from backend.bibliophilia.books.domain.utils.parse import parse_facets
from backend.bibliophilia.books.domain.utils.texttokeniser import TextTokeniser
from backend.bibliophilia.books import settings
from backend.bibliophilia.books.domain.boundaries import BookRepository, SearchRepository
from backend.bibliophilia.books.domain.models.basic import FileFormat
from backend.bibliophilia.books.domain.models.input import BookCreate, Rights
from backend.bibliophilia.books.domain.models.output import BookInfo
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile



class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self.repository = book_repository

    def create_book(self, book: BookCreate) -> (Optional[int], status):
        book = self.repository.create_book(book)
        if book:
            logging.info(f"book created: {book.idx}")
            return book, status.HTTP_201_CREATED
        else:
            logging.info(f"book not created")
            return None, status.HTTP_409_CONFLICT

    def create_image(self, image: ImageFileSave) -> (Optional[str], status):
        url = self.repository.create_image(image)
        if url:
            logging.info(f"image created: {url}")
            return url, status.HTTP_201_CREATED
        else:
            logging.info(f"image not created")
            return None, status.HTTP_409_CONFLICT

    def create_file(self, bookfile: BookFileSave) -> status:
        is_tokenized = self.repository.is_tokenized(bookfile.book_idx)
        if not is_tokenized:
            book = self.repository.read_book(bookfile.book_idx)
            tokens = TextTokeniser().book_to_tokens(bookfile.file)

            booksearch = BookSearch(title=book.title,
                                    year=book.year,
                                    publisher=book.publisher,
                                    description=book.description,
                                    author=[author.name for author in book.authors],
                                    genre=[genre.name for genre in book.genres],
                                    tokens=tokens)
            if book:  # TODO
                is_tokenized = self.repository.update_book(book)
            self.repository.create_booksearch(booksearch, book.idx)
        bookfile = self.repository.create_bookfile(bookfile)
        return status.HTTP_201_CREATED

    def add_rights(self, book_idx: int, rights: Rights, user_idx: int):
        self.repository.add_rights(rights, book_idx, user_idx)

    def delete_rights(self, book_idx: int):
        self.repository.delete_rights(book_idx)

    def read_book(self, idx: int) -> Optional[BookInfo]:
        book = self.repository.read_book(idx)
        formats = self.repository.get_book_formats(idx)
        if book:
            return BookInfo(title=book.title,
                            author=[author.name for author in book.authors],
                            genre=[genre.name for genre in book.genres],
                            year=book.year,
                            publisher=book.publisher,
                            description=book.description,
                            image_url=book.image_url,
                            formats=[book_format.value for book_format in formats])
        return None

    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        return self.repository.read_bookfile(idx=idx, file_format=file_format)


class SearchService:
    def __init__(self, search_repository: SearchRepository, book_repository: BookRepository) -> None:
        self.search_repository = search_repository
        self.book_repository = book_repository

    def search(self, query: str, page: int) -> list[BookCard]:
        if query == '':
            query = '.'
        query, filter = parse_facets(query)
        print(f"Parsed query: {query}")
        # TODO: facets
        # Какой то слооожный поиск
        logging.info("Base Search started")
        ids = []
        base_search_ids = self.search_repository.base_search(query, filter=filter)
        ids.extend(base_search_ids)
        logging.info(f"Base Search finished:{ids}")
        if query != "":
            logging.info("Semantic Search started")
            tokens = TextTokeniser().text_to_tokens(query)
            semantic_search_ids = self.search_repository.semantic_search(tokens, filter=filter)
            for idx in semantic_search_ids:
                if idx not in ids:
                    ids.append(idx)
            logging.info(f"Semantic Search finished:{ids}")
        page_ids = []
        for item in ids:
            if item not in page_ids:
                page_ids.append(item)
        page_ids = page_ids[(settings.BOOKS_IN_PAGE * (page - 1)): (settings.BOOKS_IN_PAGE * page)]
        logging.info(f"Final books:{page_ids}")
        books = self.book_repository.read_books(page_ids)
        return [BookCard(idx=book.idx,
                         title=book.title,
                         author=[author.name for author in book.authors],
                         genre=[genre.name for genre in book.genres],
                         image_url=book.image_url) for book in books]

    def read_facets(self) -> set[Facet]:
        return set(Facet)

    def read_hints(self, query: str, facet: str) -> list[str]:
        return self.search_repository.read_hints(query, Facet(facet))[:settings.MAX_HINTS]

import logging
import os
from typing import Optional

from backend.bibliophilia.server.data.storages.interfaces.books import DBBookStorage, SearchStorage, \
    SearchBookStorage, FSBookStorage
from backend.bibliophilia.server.domain.models.basic.books import FileFormat
from backend.bibliophilia.server.domain.models.input.books import BookCreate, BookFileCreate, BookSearch, \
    BookFileSave, ImageFileSave
from backend.bibliophilia.server.domain.models.schemas.books import Book, BookFile
from sqlmodel import select, Session
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
from sqlalchemy import func


class FSBookStorageImpl(FSBookStorage):

    def __init__(self,
                 url: str,
                 images_path: str,
                 files_path: str,
                 image_extension: str):
        self.url = url
        self.images_path = images_path
        self.files_path = files_path
        self.image_extension = image_extension

    def save_bookfile(self, bookfile: BookFileSave) -> bool:
        path = bookfile.bookfile_path
        if bookfile.file:
            content = bookfile.file.file.read()
            with open(path, "wb") as file_object:
                file_object.write(content)
        return True

    def get_bookfile(self, book: BookFile) -> Optional[bytes]:
        # TODO: не уверена так ли надо передавать файл
        with open(book.bookfile_path, "rb") as file:
            return file.read()

    def delete_bookfile(self, book: BookFile) -> bool:
        try:
            if os.path.exists(book.bookfile_path):
                os.remove(book.bookfile_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
        return True

    def save_bookimage(self, bookimage: ImageFileSave) -> Optional[str]:
        path = bookimage.image_path
        url = bookimage.image_url
        if bookimage.image:
            content = bookimage.image.file.read()
            with open(path, "wb") as image_object:
                image_object.write(content)
        return url

    def delete_bookimage(self, book_idx: int) -> bool:
        image_path = ImageFileSave(book_idx=book_idx, image=None).image_path
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
        return True


class DBBookStorageImpl(DBBookStorage):
    def __init__(self, engine):
        self.engine = engine

    def create_book(self, book: BookCreate) -> Optional[Book]:
        with Session(self.engine) as session:
            db_book = Book.from_orm(book)
            session.add(db_book)
            session.commit()
            session.refresh(db_book)
            return db_book

    def read_book(self, idx: int = None) -> Optional[Book]:
        with Session(self.engine) as session:
            return session.exec(select(Book).where(Book.idx == idx)).one_or_none()

    def get_book_formats(self, idx: int) -> set[FileFormat]:
        with Session(self.engine) as session:
            bookfiles = session.exec(select(BookFile).where(BookFile.book_idx == idx)).all()
            return set(file.format for file in bookfiles)

    def create_bookfile(self, book: BookFileCreate) -> Optional[BookFile]:
        with Session(self.engine) as session:
            db_bookfile = BookFile.from_orm(book)
            logging.info("BookFile from orm")
            session.add(db_bookfile)
            logging.info("Added")
            session.commit()
            logging.info("Commited")
            session.refresh(db_bookfile)
            logging.info("Refreshed")
            return db_bookfile

    def read_bookfile(self, idx: int, file_format: FileFormat) -> Optional[BookFile]:
        with Session(self.engine) as session:
            return session.exec(select(BookFile)
                                .where(BookFile.book_idx == idx)
                                .where(BookFile.format == file_format)).one_or_none()

    def get_all_formats(self, book_idx: int) -> set[FileFormat]:
        with Session(self.engine) as session:
            book_files = session.exec(select(BookFile)
                                      .where(BookFile.book_idx == book_idx)).all()
            formats = [file.format for file in book_files]
            return set(formats)

    def remove_book(self, book: Book) -> bool:
        with Session(self.engine) as session:
            session.delete(book)
            session.commit()
            return True

    def remove_bookfile(self, bookfile: BookFile) -> bool:
        with Session(self.engine) as session:
            session.delete(bookfile)
            session.commit()
            return True

    def read_books(self, idxs: list[int]) -> list[Book]:
        with Session(self.engine) as session:
            books: list[Book] = session.query(Book).filter(Book.idx.in_(idxs)).all()
            books_by_indexes = {str(book.idx): book for book in books}
            result_books = [None] * len(idxs)
            logging.info(idxs)
            logging.info(books_by_indexes)
            for i, idx in enumerate(idxs):
                result_books[i] = books_by_indexes[str(idx)]
            logging.info(result_books)
            return result_books


class ESBookStorageImpl(SearchBookStorage, SearchStorage):
    def __init__(self, elasticsearch: Elasticsearch):
        self.es = elasticsearch

    def index(self, book_idx: int, es_book: BookSearch) -> bool:
        response = self.es.index(
            index=Book.__tablename__,
            id=str(book_idx),
            body={
                "title": es_book.title,
                "author": es_book.author,
                "description": es_book.description,
                "tokens": es_book.tokens
            },
        )
        logging.info(f"ES indexing status: {response['result']}")
        return True

    def base_search(self, query: str) -> [int]:
        query = Q('bool', should=[
            Q('match', title=query),
            Q('match', author=query),
            Q('match', description=query)
        ])
        search = Search(using=self.es, index=Book.__tablename__).query(query)
        response = search.execute()
        return [hit.meta.id for hit in response]

    def semantic_search(self, tokens: list[float]) -> [int]:
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.queryVector, 'tokens') + 1.0",
                    "params": {
                        "queryVector": tokens
                    }
                }
            }
        }
        s = Search(using=self.es, index='books').query(script_query)
        response = s.execute()
        # Extracting IDs from Elasticsearch response
        return [hit.meta.id for hit in response]

import logging
import os
from typing import Optional, Any

from backend.bibliophilia.books.data.store.interfaces import DBBookStorage, SearchStorage, SearchBookStorage, FSBookStorage
from backend.bibliophilia.books.domain.entity.facet import Facet
from backend.bibliophilia.books.domain.models.basic import FileFormat, FacetBase
from backend.bibliophilia.books.domain.models.input import BookCreate, BookFileCreate, BookSearch, BookFileSave, ImageFileSave
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile, Author, Genre
from backend.bibliophilia.books.data.store.interfaces import DBBookStorage, SearchStorage, SearchBookStorage, FSBookStorage
from backend.bibliophilia.books.domain.models.basic import FileFormat
from backend.bibliophilia.books.domain.models.input import BookCreate, BookFileCreate, BookSearch, BookFileSave, \
    ImageFileSave, Rights
from backend.bibliophilia.books.domain.models.schemas import Book, BookFile, UserBookRights, RightsEnum, \
    GroupBookRights
from sqlmodel import select, Session
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from sqlalchemy.orm import contains_eager

from backend.bibliophilia.core.models import BPModel
from backend.bibliophilia.users.domain.models.schemas import User, Group


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
            #db_book = Book.from_orm(book)
            db_book = Book(title=book.title, year=book.year, publisher=book.publisher, description=book.description, public=RightsEnum.NONE)
            session.add(db_book)
            session.commit()
            session.refresh(db_book)
            return db_book

    def check_author_exists(self, author: str) -> bool:
        with Session(self.engine) as session:
            db_author = session.exec(select(Author).where(Author.name == author)).first()
            if db_author:
                return True
            return False

    def check_genre_exists(self, genre: str) -> bool:
        with Session(self.engine) as session:
            db_genre = session.exec(select(Genre).where(Genre.name == genre)).first()
            if db_genre:
                return True
            return False

    def create_book_rights(self, user_idx: int, book_idx: int, rights: Rights):
        with Session(self.engine) as session:
            for username in rights.users_see:
                user = session.exec(select(User).where(User.email == username)).one_or_none()
                if user is None:
                    raise Exception(f"No such user \"{username}\"")
                user_book_rights = UserBookRights(user_idx=user.idx, book_idx=book_idx,
                                                            rights=RightsEnum.SEARCH)
                session.add(user_book_rights)
                #session.commit()

            for username in rights.users_see_read:
                user = session.exec(select(User).where(User.name == username)).one_or_none()
                if user is None:
                    raise Exception(f"No such user \"{username}\"")
                user_book_rights = UserBookRights(user_idx=user.idx, book_idx=book_idx,
                                                            rights=RightsEnum.SEARCH_READ)
                session.add(user_book_rights)
                #session.commit()

            for username in rights.users_see_read_download:
                user = session.exec(select(User).where(User.name == username)).one_or_none()
                if user is None:
                    raise Exception(f"No such user \"{username}\"")
                user_book_rights = UserBookRights(user_idx=user.idx, book_idx=book_idx,
                                                            rights=RightsEnum.SEARCH_READ_DOWNLOAD)
                session.add(user_book_rights)
                #session.commit()

            for group_name in rights.group_see:
                group = session.exec(select(Group).where(Group.group_name == group_name).where(Group.creator_idx == user_idx)).one_or_none()
                if group is None:
                    raise Exception(f"No such group \"{group_name}\"")
                group_book_rights = GroupBookRights(group_idx=group.idx, book_idx=book_idx,
                                                              rights=RightsEnum.SEARCH)
                session.add(group_book_rights)
                #session.commit()

            for group_name in rights.group_see_read:
                group = session.exec(select(Group).where(Group.group_name == group_name).where(Group.creator_idx == user_idx)).one_or_none()
                if group is None:
                    raise Exception(f"No such group \"{group_name}\"")
                group_book_rights = GroupBookRights(group_idx=group.idx, book_idx=book_idx,
                                                              rights=RightsEnum.SEARCH_READ)
                session.add(group_book_rights)
                #session.commit()

            for group_name in rights.group_see_read_download:
                group = session.exec(select(Group).where(Group.group_name == group_name).where(Group.creator_idx == user_idx)).one_or_none()
                if group is None:
                    raise Exception(f"No such group \"{group_name}\"")
                group_book_rights = GroupBookRights(group_idx=group.idx, book_idx=book_idx,
                                                              rights=RightsEnum.SEARCH_READ_DOWNLOAD)
                session.add(group_book_rights)
                #session.commit()

            book = session.exec(select(Book).where(Book.idx == book_idx)).one_or_none()
            if rights.is_see_all == False and rights.is_see_read_all == False and rights.is_see_read_download_all == False:
                book.public = RightsEnum.NONE
            elif rights.is_see_read_download_all == True:
                book.public = RightsEnum.SEARCH_READ_DOWNLOAD
            elif rights.is_see_read_all == True:
                book.public = RightsEnum.SEARCH_READ
            elif rights.is_see_all == True:
                book.public = RightsEnum.SEARCH

            session.add(book)
            session.commit()
            session.refresh(book)

    def delete_book_rights(self, book_idx: int):
        with Session(self.engine) as session:
            user_rights = session.exec(select(UserBookRights).where(UserBookRights.book_idx == book_idx)).all()
            for user_right in user_rights:
                session.delete(user_right)
            group_rights = session.exec(select(GroupBookRights).where(GroupBookRights.book_idx == book_idx)).all()
            for group_right in group_rights:
                session.delete(group_right)
            book = session.exec(select(Book).where(Book.idx == book_idx)).one_or_none()
            book.public = RightsEnum.NONE
            session.add(book)
            session.commit()

    def read_book(self, idx: int = None) -> Optional[Book]:
        with Session(self.engine) as session:
            select_book = (
                select(Book)
                .options(contains_eager(Book.author), contains_eager(Book.genre))
                .where(Book.idx == idx))
            return session.exec(select_book).unique().one_or_none()

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
            books: list[Book] = (session.
                                 query(Book)
                                 .options(contains_eager(Book.author), contains_eager(Book.genre))
                                 .filter(Book.idx.in_(idxs)).all())
            books_by_indexes = {str(book.idx): book for book in books}
            sorted_books = [books_by_indexes[str(idx)] for idx in idxs]
            return sorted_books

    def create_facet(self, value: FacetBase, facet: Facet) -> Optional[Author | Genre]:
        with Session(self.engine) as session:
            db_facet = None
            match facet:
                case Facet.author:
                    db_facet = Author.from_orm(value)
                case Facet.genre:
                    db_facet = Genre.from_orm(value)
            logging.info("BookFile from orm")
            session.add(db_facet)
            logging.info("Added")
            session.commit()
            logging.info("Commited")
            session.refresh(db_facet)
            logging.info("Refreshed")
            return db_facet

    def remove_facet(self, facet: FacetBase) -> bool:
        with Session(self.engine) as session:
            session.delete(facet)
            session.commit()
            return True


class ESBookStorageImpl(SearchBookStorage, SearchStorage):

    def __init__(self, elasticsearch: Elasticsearch):
        self.es = elasticsearch

    def index_book(self, book_idx: int, es_book: BookSearch) -> bool:
        book_data = {
            "title": es_book.title,
            "author": [{"value": {"key": author, "text": author}} for i, author in enumerate(es_book.author)],
            "genre": [{"value": {"key": genre, "text": genre}} for i, genre in enumerate(es_book.genre)],
            "year": es_book.year,
            "publisher": es_book.publisher,
            "description": es_book.description,
            "tokens": es_book.tokens
        }
        self.es.index(index=Book.__tablename__, id=str(book_idx), body=book_data, )
        logging.info(f"Book: \"{book_idx}\" successfully added to the index")
        return True

    def delete_indexed_book(self, book_idx: int):
        response = self.es.delete(index=Book.__tablename__, id=str(book_idx))
        logging.info(f"ES indexing status: {response['result']}")
        return True

    def index_facet(self, value: str, facet: Facet) -> bool:
        response = self.es.search(index=facet, body={
            "query": {
                "term": {
                    "value": value
                }
            }
        })
        hits = response["hits"]["hits"]
        print(f"hits: {hits}")
        if hits:
            logging.info(f"Facet: \"{value}\" already exists")
            return False
        facet_data = {"value": value}
        self.es.index(index=facet, body=facet_data)
        logging.info(f"Facet: \"{value}\" successfully added to the index")
        return True

    def delete_indexed_facet(self, value: str, facet: Facet) -> bool:
        facet_data = {"value": value}
        self.es.delete(index=facet, body=facet_data)
        logging.info(f"Facet: \"{value}\" successfully deleted from es")
        return True

    def base_search(self, query: str, filter=None) -> [int]:
        query = {
            "bool": {
                "should": [
                    {"match": {"title": query}},
                    {"match": {"author": query}},
                    {"match": {"description": query}},
                ]
            }
        }
        if filter:
            query = {"bool": {"should": [query], "filter": filter}}
        search = Search(using=self.es, index=Book.__tablename__).query(query)
        response = search.execute()
        return [hit.meta.id for hit in response]

    def semantic_search(self, tokens: list[float], filter=None) -> [int]:
        query = {
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
        if filter:
            query = {"bool": {"should": [query], "filter": filter}}
        s = Search(using=self.es, index=Book.__tablename__).query(query)
        response = s.execute()
        return [hit.meta.id for hit in response]

    def read_hints(self, query: str, facet: Facet) -> list[str]:
        es_query = {
            "bool": {
                "should": {
                    "prefix": {
                        "value": f"{query}"
                    }
                }
            }
        }
        search = Search(using=self.es, index=facet).query(es_query)
        response = search.execute()
        return [hit["value"] for hit in response.hits]

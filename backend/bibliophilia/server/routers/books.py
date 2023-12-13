from elasticsearch_dsl import Q, Search
from fastapi import status, APIRouter, Query
from fastapi import Response
from sqlmodel import select, Session

from bibliophilia.server import settings
from bibliophilia.server.db.tables import Book, BookCreate, BookES, BookInfo, BookCard, BookFile, FileFormat
from bibliophilia.server.dependencies import es, engine, BOOKS_IN_PAGE
from typing import Optional, Annotated
from fastapi import UploadFile, File

router = APIRouter()


@router.post("/", response_model=Optional[int])
def handle_create_book(title: str,
                       author: str,
                       description: str,
                       image_file: Optional[UploadFile],
                       files: list[UploadFile],
                       response: Response):
    db_book, response.status_code = create_book(BookCreate(title=title,
                                                           author=author,
                                                           description=description,
                                                           image_file=image_file,
                                                           files=files))
    if db_book:
        return db_book.idx
    return None


def save_image(book_idx: int, book: UploadFile) -> str:
    extension = book.filename.split('.')[-1]
    path = f"{settings.IMAGES_PATH}/{book_idx}.{extension}"
    url = f"{settings.URL}/images/{book_idx}.{extension}"
    if book:
        content = book.file.read()
        with open(path, "wb") as file_object:
            file_object.write(content)
    return url


def save_files(book_idx: int, files: list[UploadFile], session) -> list[BookFile]:
    bd_book_files = []
    if files:
        for file in files:
            extension = file.filename.split('.')[-1]
            path = f"{settings.FILES_PATH}/{book_idx}.{extension}"
            content = file.file.read()
            with open(path, "wb") as file_object:
                file_object.write(content)
            book_file = BookFile(path=path, format=FileFormat.get_by_name(extension), book_idx=book_idx)
            bd_book_files.append(book_file)
            session.add(book_file)
        session.commit()
    return bd_book_files


def create_book(book: BookCreate) -> (Book, status):
    with Session(engine) as session:
        existing_book = session.exec(select(Book).where(Book.title == book.title)).one_or_none()
        if existing_book:
            return None, status.HTTP_409_CONFLICT
        db_book = Book.from_orm(book)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        if book.image_file:
            db_book.image_url = save_image(db_book.idx, book.image_file)
        if book.files:
            db_book.files = save_files(db_book.idx, book.files, session)
        session.commit()
        es_book = BookES(title=db_book.title, author=db_book.author, description=db_book.description, tokens=[])
        es.index(index=db_book.__tablename__, id=db_book.idx, document=es_book.dict())
        return db_book, status.HTTP_201_CREATED


@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    with Session(engine) as session:
        return session.exec(select(Book).where(Book.idx == idx)).one_or_none()


@router.get("/", response_model=list[BookCard])
def search_books(q: str = Query("", title="Query string"), page: int = Query(1, title="Page number")):
    ids = base_search(q)[BOOKS_IN_PAGE * (page - 1)::BOOKS_IN_PAGE * page + 1]
    with Session(engine) as session:
        books = session.query(Book).filter(Book.idx.in_(ids)).all()
        return [BookCard(title=book.title,
                         author=book.author,
                         image_url=book.image_url) for book in books]


def base_search(text: str) -> list[int]:
    query = Q('bool', should=[
        Q('match', title=text),
        Q('match', author=text),
        Q('match', description=text)
    ])
    search = Search(using=es, index=Book.__tablename__).query(query)
    response = search.execute()
    return [hit.meta.id for hit in response]

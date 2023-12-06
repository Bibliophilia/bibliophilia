from typing import Optional

from elasticsearch_dsl import Q, Search
from fastapi import status, APIRouter, Query
from fastapi import Response
from sqlmodel import select, Session

from bibliophilia.server.db.tables import Book, BookCreate, BookES, BookInfo, BookCard
from bibliophilia.server.dependencies import es, engine, BOOKS_IN_PAGE

router = APIRouter()


@router.post("/", response_model=Optional[int])
def handle_create_book(book: BookCreate, response: Response):
    db_book, response.status_code = create_book(book)
    if db_book:
        return db_book.idx
    return None


def create_book(book: BookCreate) -> (Book, status):
    with Session(engine) as session:
        existing_book = session.exec(select(Book).where(Book.title == book.title)).one_or_none()
        if existing_book:
            return None, status.HTTP_409_CONFLICT
        db_book = Book.from_orm(book)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
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

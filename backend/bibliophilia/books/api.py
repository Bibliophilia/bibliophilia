import logging

from fastapi import APIRouter, Query
from fastapi import Response

import backend.bibliophilia.books.settings as settings
from backend.bibliophilia.books.domain.models.basic import FileFormat
from backend.bibliophilia.books.domain.models.input import BookCreate, Credentials
from backend.bibliophilia.books.domain.models.output import BookInfo, BookCard

import backend.bibliophilia.books.dependencies as dependencies
from typing import Optional
from fastapi import UploadFile
from starlette.responses import FileResponse

from backend.bibliophilia.books.domain.models.schemas import UserBookCredentials, CredentialsEnum, GroupBookCredentials, \
    Book
from backend.bibliophilia.core.dependencies import engine
from sqlmodel import Session, select

from backend.bibliophilia.users.domain.models.schemas import UserGroupLink, User, Group

router = APIRouter()


@router.post("/upload", response_model=Optional[int])
def handle_create_book(title: str,
                       author: str,
                       description: str,
                       credentials: Credentials,
                       image_file: Optional[UploadFile],
                       files: list[UploadFile],
                       response: Response):

    book, response.status_code = dependencies.book_service.create(BookCreate(title=title,
                                                                             author=author,
                                                                             description=description,
                                                                             image=image_file,
                                                                             files=files))
    logging.info(f"Book created: {book.idx}")
    return book.idx


def create_book_credentials(credentials: Credentials, book_idx: int):
    with Session(engine) as session:
        for username in credentials.users_see:
            user = session.exec(select(User).where(User.name == username)).one_or_none()
            user_book_credentials = UserBookCredentials(user_idx=user.idx, book_idx=book_idx, credentials=CredentialsEnum.SEE)
            session.add(user_book_credentials)
            session.commit()

        for username in credentials.users_see_read:
            user = session.exec(select(User).where(User.name == username)).one_or_none()
            user_book_credentials = UserBookCredentials(user_idx=user.idx, book_idx=book_idx, credentials=CredentialsEnum.SEE_READ)
            session.add(user_book_credentials)
            session.commit()

        for username in credentials.users_see_read_download:
            user = session.exec(select(User).where(User.name == username)).one_or_none()
            user_book_credentials = UserBookCredentials(user_idx=user.idx, book_idx=book_idx, credentials=CredentialsEnum.SEE_READ_DOWNLOAD)
            session.add(user_book_credentials)
            session.commit()

        for group_name in credentials.group_see:
            group = session.exec(select(Group).where(Group.name == group_name)).one_or_none()
            group_book_credentials = GroupBookCredentials(group_idx=group.idx, book_idx=book_idx,
                                                        credentials=CredentialsEnum.SEE)
            session.add(group_book_credentials)
            session.commit()

        for group_name in credentials.group_see_read:
            group = session.exec(select(Group).where(Group.name == group_name)).one_or_none()
            group_book_credentials = GroupBookCredentials(group_idx=group.idx, book_idx=book_idx,
                                                          credentials=CredentialsEnum.SEE_READ)
            session.add(group_book_credentials)
            session.commit()

        for group_name in credentials.group_see_read_download:
            group = session.exec(select(Group).where(Group.name == group_name)).one_or_none()
            group_book_credentials = GroupBookCredentials(group_idx=group.idx, book_idx=book_idx,
                                                          credentials=CredentialsEnum.SEE_READ_DOWNLOAD)
            session.add(group_book_credentials)
            session.commit()

        book = session.exec(select(Book).where(Book.idx == book_idx)).one_or_none()
        if credentials.is_see_all == False and credentials.is_see_read_all == False and credentials.is_see_read_download_all == False:
            book.public = CredentialsEnum.NONE
        elif credentials.is_see_read_download_all == True:
            book.public = CredentialsEnum.SEE_READ_DOWNLOAD
        elif credentials.is_see_read_all == True:
            book.public = CredentialsEnum.SEE_READ
        elif credentials.is_see_all == True:
            book.public = CredentialsEnum.SEE

        session.add(book)
        session.commit()
        session.refresh(book)



@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    book = dependencies.book_service.read_book(idx=idx)
    logging.info(f"Book Info: {book.title}")
    return book


@router.get("/search/", response_model=list[BookCard])
def handle_search_books(q: str = Query("", title="Query string"), page: int = Query(1, title="Page number")):
    books = dependencies.search_service.search(query=q, page=page)
    logging.info(f"Books Founded: {len(books)}\n{books}")
    return books


@router.get("/download/")
def handle_download_bookfile(idx: int, book_format: str):
    book = dependencies.book_service.read_book(idx=idx)
    bookfile = dependencies.book_service.read_bookfile(idx=idx, file_format=FileFormat.get_by_name(book_format))
    if bookfile and book:
        filename = f"{book.title}-{book.author}.{bookfile.format.value}"
        filename = filename.replace(' ', '-')
        logging.info(f"File downloaded: {filename}")
        return FileResponse(path=bookfile.bookfile_path,
                            filename=filename,
                            media_type=f'application/{settings.MEDIA_TYPES[bookfile.format.value]}')
    logging.info(f"File not found for download")
    return None

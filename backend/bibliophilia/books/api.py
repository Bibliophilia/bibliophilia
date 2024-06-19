import logging

from fastapi import APIRouter, Query, HTTPException, status
from fastapi import Response
from starlette.requests import Request

import backend.bibliophilia.books.settings as settings
from backend.bibliophilia.books.domain.entity.facet import Facet
from backend.bibliophilia.books.domain.models.basic import FileFormat
from backend.bibliophilia.books.domain.models.input import BookCreate, BookCreateInfo, ImageFileSave, BookFileSave
from backend.bibliophilia.books.domain.models.output import BookInfo, BookCard

import backend.bibliophilia.books.dependencies as dependencies
from typing import Optional, Set, AnyStr, List
from fastapi import UploadFile
from starlette.responses import FileResponse, RedirectResponse

from backend.bibliophilia.books.domain.models.input import Rights
from backend.bibliophilia.books.domain.utils.security import check_book_right, check_is_publisher

from backend.bibliophilia.core.models import BPModel

router = APIRouter()


@router.post("/data/upload", response_model=Optional[int])
def handle_create_book(request: Request,
                       book: BookCreateInfo,
                       response: Response):
    logging.info(request)
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to upload books")
    book, response.status_code = dependencies.book_service.create_book(BookCreate(**book.dict()))
    logging.info(f"Book created: {book.idx}")
    return book.idx


@router.post("/image/upload")
def handle_upload_image(request: Request,
                        book_idx: str,
                        image: Optional[UploadFile],
                        response: Response):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to upload image")
    if not check_is_publisher(int(book_idx), request.session.get('user').get('email')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the publisher can upload an image")
    _, response.status_code = dependencies.book_service.create_image(ImageFileSave(book_idx=book_idx,
                                                                                   image=image))


@router.post("/file/upload")
def handle_upload_file(request: Request,
                       book_idx: str,
                       file: Optional[UploadFile],
                       response: Response):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to upload file")
    if not check_is_publisher(int(book_idx), request.session.get('user').get('email')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the publisher can upload a file")
    response.status_code = dependencies.book_service.create_file(BookFileSave(book_idx=book_idx,
                                                                              file=file))


@router.post("/add-rights")
def handle_add_rights(request: Request, book_idx: int, user_idx: int, rights: Rights):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to add rights")
    if not check_is_publisher(book_idx, request.session.get('user').get('email')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the publisher can add rights")
    dependencies.book_service.add_rights(book_idx=book_idx, rights=rights, user_idx=user_idx)


@router.delete("/delete-rights")
def handle_delete_rights(request: Request, book_idx: int):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to delete rights")
    if not check_is_publisher(book_idx, request.session.get('user').get('email')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the publisher can add rights")
    dependencies.book_service.delete_rights(book_idx)


@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    book = dependencies.book_service.read_book(idx=idx)
    if book:
        logging.info(f"Book Info: {book.title}")
    return book


@router.get("/search/", response_model=list[BookCard])
def handle_search_books(request: Request,
                        q: str = Query("", title="Query string"),
                        page: int = Query(1, title="Page number")):
    books = dependencies.search_service.search(query=q, page=page)
    show_books = []
    for book in books:
        access = check_book_right(book.idx, request.session.get('user'), "search")
        if access == True:
            show_books.append(book)

    logging.info(f"Books Founded: {len(books)}\n{books}")
    return show_books


@router.get("/search/facets", response_model=Set[Facet])
def handle_get_facets():
    return dependencies.search_service.read_facets()


@router.get("/search/hints", response_model=list[str])
def handle_get_hints(q: str = Query("", title="Query"), facet: Facet = Query(None, title="Facet type")):
    if facet in dependencies.search_service.read_facets() and facet.hints():
        return dependencies.search_service.read_hints(q, facet)
    else:
        return []


@router.get("/download/")
def handle_download_bookfile(request: Request, idx: int, book_format: str):
    access = check_book_right(idx, request.session.get('user'), "download")
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights for download this book!")
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

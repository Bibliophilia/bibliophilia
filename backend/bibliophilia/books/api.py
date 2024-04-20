import logging

from fastapi import APIRouter, Query
from fastapi import Response

import bibliophilia.books.settings as settings
from bibliophilia.books.domain.entity.facet import Facet
from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate
from bibliophilia.books.domain.models.output import BookInfo, BookCard

import bibliophilia.books.dependencies as dependencies
from typing import Optional, Set
from fastapi import UploadFile
from starlette.responses import FileResponse

router = APIRouter()


@router.post("/upload", response_model=Optional[int])
def handle_create_book(title: str,
                       author: str,
                       description: str,
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


@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    book = dependencies.book_service.read_book(idx=idx)
    logging.info(f"Book Info: {book.title}")
    return book


@router.get("/search/", response_model=list[BookCard])
def handle_search_books(q: str = Query("", title="Query string"),
                        page: int = Query(1, title="Page number")):
    books = dependencies.search_service.search(query=q, facets=[], page=page)
    logging.info(f"Books Founded: {len(books)}\n{books}")
    return books


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

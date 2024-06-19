import logging

from fastapi import APIRouter, Query
from fastapi import Response

import bibliophilia.books.settings as settings
from bibliophilia.books.domain.entity.facet import Facet
from bibliophilia.books.domain.models.basic import FileFormat
from bibliophilia.books.domain.models.input import BookCreate, BookCreateInfo, ImageFileSave, BookFileSave
from bibliophilia.books.domain.models.output import BookInfo, BookCard

import bibliophilia.books.dependencies as dependencies
from typing import Optional, Set, AnyStr, List
from fastapi import UploadFile
from starlette.responses import FileResponse

from bibliophilia.core.models import BPModel

router = APIRouter()


@router.get("/data/upload", response_model=Optional[int])
def handle_create_book(response: Response,
                       title: str = Query("", title="title"),
                       year: int = Query(0, title="title"),
                       publisher: str = Query("", title="publisher"),
                       description: str = Query("", title="description"),
                       author: List[str] = Query([], title="author"),
                       genre: List[str] = Query([], title="genre")):
    book_data = BookCreate(title=title,
                           year=year,
                           publisher=publisher,
                           description=description,
                           author=author,
                           genre=genre)
    book, response.status_code = dependencies.book_service.create_book(book_data)
    logging.info(f"Book created: {book.idx}")
    return book.idx


@router.post("/image/upload")
def handle_upload_image(image: Optional[UploadFile],
                        response: Response,
                        idx: int = Query(-1, title="index")):
    _, response.status_code = dependencies.book_service.create_image(ImageFileSave(book_idx=idx,
                                                                                   image=image))


@router.post("/file/upload")
def handle_upload_file(file: Optional[UploadFile],
                       response: Response,
                       idx: int = Query(-1, title="index")):
    response.status_code = dependencies.book_service.create_file(BookFileSave(book_idx=idx,
                                                                              file=file))


@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    book = dependencies.book_service.read_book(idx=idx)
    logging.info(f"Book Info: {book.title}")
    return book


@router.get("/search/", response_model=list[BookCard])
def handle_search_books(q: str = Query("", title="Query string"),
                        page: int = Query(1, title="Page number")):
    books = dependencies.search_service.search(query=q, page=page)
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

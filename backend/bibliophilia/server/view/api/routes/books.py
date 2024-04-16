from fastapi import APIRouter, Query
from fastapi import Response

from backend.bibliophilia.server import settings
from backend.bibliophilia.server.domain.models.basic.books import FileFormat
from backend.bibliophilia.server.domain.models.input.books import BookCreate
from backend.bibliophilia.server.domain.models.output.books import BookInfo, BookCard

import bibliophilia.server.dependencies as dependencies
from typing import Optional
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
    return book.idx


@router.get("/{idx}", response_model=Optional[BookInfo])
def handle_get_book_info(idx: int):
    return dependencies.book_service.read_book(idx=idx)


@router.get("/search/", response_model=list[BookCard])
def handle_search_books(q: str = Query("", title="Query string"), page: int = Query(1, title="Page number")):
    return dependencies.search_service.search(query=q, page=page)


@router.get("/download/")
def handle_download_bookfile(idx: int, book_format: str):
    book = dependencies.book_service.read_book(idx=idx)
    bookfile = dependencies.book_service.read_bookfile(idx=idx, file_format=FileFormat.get_by_name(book_format))
    if bookfile and book:
        filename = f"{book.title}-{book.author}.{bookfile.format.value}"
        filename = filename.replace(' ', '-')
        return FileResponse(path=bookfile.bookfile_path,
                            filename=filename,
                            media_type=f'application/{settings.MEDIA_TYPES[bookfile.format.value]}')
    return None

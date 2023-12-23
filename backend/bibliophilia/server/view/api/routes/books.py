from fastapi import APIRouter, Query
from fastapi import Response

from bibliophilia.server.domain.models.input.books import BookCreate
from bibliophilia.server.domain.models.output.books import BookInfo, BookCard

import bibliophilia.server.dependencies as dependencies
from typing import Optional
from fastapi import UploadFile

router = APIRouter()


@router.post("/", response_model=Optional[int])
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


@router.get("/", response_model=list[BookCard])
def search_books(q: str = Query("", title="Query string"), page: int = Query(1, title="Page number")):
    return dependencies.search_service.search(query=q, page=page)

from fastapi import APIRouter, Query
from fastapi import Response

from backend.bibliophilia.users import dependencies
from backend.bibliophilia.users.domain.models.input import ReviewCreate
from backend.bibliophilia.users.domain.models.output import ReviewCard

router = APIRouter()


@router.post("/upload", response_model=bool)
def handle_create_review(review: ReviewCreate, response: Response):
    result, response.status_code = dependencies.review_service.create_review(review)
    return result


@router.get("/", response_model=list[ReviewCard])
def handle_get_book_reviews(book_idx: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    return dependencies.review_service.read_reviews(book_idx=book_idx, page=page)


@router.get("/rating/{idx}", response_model=float)
def handle_get_rating(idx: int):
    return dependencies.review_service.read_rating(idx)

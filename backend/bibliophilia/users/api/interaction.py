from fastapi import APIRouter, Query
from fastapi import Response

from bibliophilia.users import dependencies
from bibliophilia.users.domain.models.input import ReviewCreate
from bibliophilia.users.domain.models.output import ReviewCard

router = APIRouter()


@router.post("/review", response_model=bool)
def handle_create_review(review: ReviewCreate, response: Response):
    result, response.status_code = dependencies.review_service.create_review(review)
    return result


@router.get("/reviews/", response_model=list[ReviewCard])
def handle_get_book_reviews(book: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    reviews = dependencies.review_service.read_reviews(book_idx=book, page=page)
    return reviews

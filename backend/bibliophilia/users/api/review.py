

from fastapi import APIRouter, Query, HTTPException
from fastapi import Response, status
from starlette.requests import Request
from backend.bibliophilia.books.domain.utils.security import check_is_creator
from backend.bibliophilia.users import dependencies
from backend.bibliophilia.users.domain.models.input import ReviewCreate
from backend.bibliophilia.users.domain.models.output import ReviewCard


router = APIRouter()


@router.post("/upload", response_model=bool)
def handle_create_review(request: Request, review: ReviewCreate, response: Response):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to create review")
    if not check_is_creator(request.session.get('user').get('email'), review.user_idx):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to create review")
    result, response.status_code = dependencies.review_service.create_review(review)
    return result


@router.get("/", response_model=list[ReviewCard])
def handle_get_book_reviews(book_idx: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    return dependencies.review_service.read_reviews(book_idx=book_idx, page=page)


@router.get("/rating/{idx}", response_model=float)
def handle_get_rating(idx: int):
    return dependencies.review_service.read_rating(idx)




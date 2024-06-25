import threading
import time

import schedule
from sqlalchemy import func
from sqlmodel import Session, select

from backend.bibliophilia.books.domain.models.schemas import Book
from backend.bibliophilia.core.dependencies import engine
from backend.bibliophilia.users.domain.models.schemas import Review

from fastapi import APIRouter, Query, HTTPException
from fastapi import Response, status
from starlette.requests import Request
from backend.bibliophilia.books.domain.utils.security import check_is_creator
from backend.bibliophilia.users import dependencies
from backend.bibliophilia.users.domain.models.input import ReviewCreate
from backend.bibliophilia.users.domain.models.output import ReviewCard
from backend.bibliophilia.users.domain.models.basic import ExtendedReviewBase

router = APIRouter()


@router.post("/upload", response_model=bool)
def handle_create_review(request: Request, review_data: ExtendedReviewBase, response: Response):
    review = ReviewCreate(rating=review_data.rating,
                          review=review_data.review,
                          book_idx=review_data.book_idx,
                          user_idx=request.session.get('user').get('email'))
    #if not check_is_creator(request.session.get('user').get('email'), request.session.get('user')):
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to create review")
    result, response.status_code = dependencies.review_service.create_review(review)
    return result


@router.get("/", response_model=list[ReviewCard])
def handle_get_book_reviews(book_idx: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    return dependencies.review_service.read_reviews(book_idx=book_idx, page=page)


@router.get("/rating/{idx}", response_model=float)
def handle_get_rating(idx: int):
    return dependencies.review_service.read_rating(idx)


def update_books_rating():
    with Session(engine) as session:
        list_book_idx_and_rating = session.query(
            Review.book_idx,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.book_idx).all()

        for book_idx_and_rating in list_book_idx_and_rating:
            book = session.exec(select(Book).where(Book.idx == book_idx_and_rating.book_idx)).first()
            book.avg_rating = book_idx_and_rating.avg_rating
            session.add(book)

        session.commit()


#schedule.every().day.at("00:00").do(update_books_rating)
schedule.every().minute.do(update_books_rating)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()





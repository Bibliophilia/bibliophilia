from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter()


@router.post("/auth", response_model=bool)
def handle_authorize():
    return True


@router.post("/review", response_model=bool)
def handle_review_book():
    return True


@router.get("/reviews/", response_model=list[str])
def handle_get_book_reviews(idx: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    return ["Some review will be here"]

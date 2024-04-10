from fastapi import APIRouter, Query

router = APIRouter()


@router.post("/auth")
def handle_authorize():
    pass


@router.post("/review")
def handle_review_book():
    pass


@router.get("/reviews/")
def handle_get_book_reviews(idx: int = Query("", title="Book index"), page: int = Query(1, title="Page number")):
    pass

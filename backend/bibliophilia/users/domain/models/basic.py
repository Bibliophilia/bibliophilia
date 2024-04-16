from bibliophilia.core.models import BPModel


class ReviewBase(BPModel):
    book_idx: int
    rating: int
    review: str


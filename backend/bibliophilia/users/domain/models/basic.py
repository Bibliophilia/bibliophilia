from bibliophilia.core.models import BPModel


class UserBase(BPModel):
    email: str
    name: str


class ReviewBase(BPModel):
    book_idx: int
    rating: int
    review: str

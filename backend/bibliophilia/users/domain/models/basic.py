from backend.bibliophilia.core.models import BPModel


class UserBase(BPModel):
    email: str
    name: str


class ReviewBase(BPModel):
    rating: int
    review: str


class ExtendedReviewBase(ReviewBase):
    book_idx: int


class GroupBase(BPModel):
    group_name: str
    creator_idx: int


class ExtendedGroupBase(GroupBase):
    users: list[str]

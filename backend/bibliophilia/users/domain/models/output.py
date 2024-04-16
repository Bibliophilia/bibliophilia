from typing import Any

from bibliophilia.users.domain.models.basic import ReviewBase


class ReviewCard(ReviewBase):
    rating: int
    review: str
    username: str

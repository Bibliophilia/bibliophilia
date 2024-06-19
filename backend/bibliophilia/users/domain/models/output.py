from typing import Any

from backend.bibliophilia.users.domain.models.basic import ReviewBase, GroupBase

from backend.bibliophilia.users.domain.models.basic import ExtendedGroupBase


class ReviewCard(ReviewBase):
    rating: int
    review: str
    username: str


class GroupInfo(ExtendedGroupBase):
    pass

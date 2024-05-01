from backend.bibliophilia.users.domain.models.basic import UserBase, ExtendedReviewBase

from backend.bibliophilia.users.domain.models.basic import ExtendedGroupBase


class UserCreate(UserBase):
    pass


class ReviewCreate(ExtendedReviewBase):
    user_idx: str


class GroupCreate(ExtendedGroupBase):
    pass

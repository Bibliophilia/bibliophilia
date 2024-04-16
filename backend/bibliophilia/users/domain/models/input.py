from bibliophilia.users.domain.models.basic import UserBase, ExtendedReviewBase


class UserCreate(UserBase):
    pass


class ReviewCreate(ExtendedReviewBase):
    user_idx: str

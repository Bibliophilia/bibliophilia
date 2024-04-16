from bibliophilia.users.domain.models.basic import UserBase, ReviewBase


class UserCreate(UserBase):
    pass


class ReviewCreate(ReviewBase):
    user_idx: str

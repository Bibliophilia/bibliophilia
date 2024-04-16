from bibliophilia.users.domain.models.basic import ReviewBase


class ReviewCreate(ReviewBase):
    user_idx: str

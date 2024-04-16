from bibliophilia.users.domain.models.basic import ReviewBase


class ReviewCard(ReviewBase):
    username: str


class ReviewRead(ReviewBase):
    user_identifier: str

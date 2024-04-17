from typing import Optional

from bibliophilia.users.data.store.interfaces import UserStorage, ReviewStorage
from bibliophilia.users.domain.boundaries import UserRepository, ReviewRepository
from bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from bibliophilia.users.domain.models.schemas import User, Review


class UserRepositoryImpl(UserRepository):

    def __init__(self, user_storage: UserStorage):
        self.user_storage = user_storage

    def create_user(self, user: UserCreate) -> Optional[User]:
        db_user = self.user_storage.create_user(user)
        return db_user

    def get_users(self, users_idxs: list[str]) -> list[User]:
        return self.user_storage.get_users(users_idxs)


class ReviewRepositoryImpl(ReviewRepository):
    def __init__(self, review_storage: ReviewStorage):
        self.storage = review_storage

    def create_review(self, review: ReviewCreate) -> Optional[Review]:
        return self.storage.create_review(review)

    def read_review(self, book_idx: int, user_idx: str) -> Optional[Review]:
        return self.storage.read_review(book_idx, user_idx)

    def read_reviews(self, book_idx: int) -> list[Review]:
        return self.storage.read_reviews(book_idx)

    def update_review(self, review: ReviewCreate) -> Optional[Review]:
        return self.storage.update_review(review)

    def delete_review(self, review: Review) -> bool:
        return self.storage.delete_review(review)

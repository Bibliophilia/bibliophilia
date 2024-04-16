from typing import Optional

from bibliophilia.users.data.store.storages import ReviewStorage
from bibliophilia.users.domain.boundaries import ReviewRepository
from bibliophilia.users.domain.models.input import ReviewCreate
from bibliophilia.users.domain.models.shemas import Review


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

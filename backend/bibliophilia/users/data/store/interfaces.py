from abc import ABC, abstractmethod
from typing import Optional

from bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from bibliophilia.users.domain.models.schemas import User, Review


class DBUserStorage(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> Optional[User]:
        pass


class ReviewStorage(ABC):
    @abstractmethod
    def create_review(self, review: ReviewCreate) -> Optional[Review]:
        pass

    @abstractmethod
    def read_review(self, book_idx: int, user_idx: str) -> Optional[Review]:
        pass

    @abstractmethod
    def read_reviews(self, book_idx: int) -> list[Review]:
        pass

    @abstractmethod
    def update_review(self, review: ReviewCreate) -> Optional[Review]:
        pass

    @abstractmethod
    def delete_review(self, review: Review) -> bool:
        pass

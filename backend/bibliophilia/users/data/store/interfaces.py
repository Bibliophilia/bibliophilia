from abc import ABC, abstractmethod
from typing import Optional

from bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from bibliophilia.users.domain.models.schemas import User, Review


class UserStorage(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> Optional[User]:
        pass

    @abstractmethod
    def get_users(self, users_idxs: list[str]) -> list[User]:
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

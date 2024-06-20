from abc import ABC, abstractmethod
from typing import Optional

from backend.bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from backend.bibliophilia.users.domain.models.schemas import User, Review

from backend.bibliophilia.users.domain.models.input import GroupCreate


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: UserCreate) -> Optional[User]:
        pass

    @abstractmethod
    def get_users(self, users_idxs: list[str]) -> list[User]:
        pass


class ReviewRepository(ABC):

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


class GroupRepository(ABC):

    @abstractmethod
    def create(self, group: GroupCreate):
        pass

    @abstractmethod
    def edit(self, old_group_name: str, group: GroupCreate):
        pass

    @abstractmethod
    def delete(self, group_name: str, user_idx: int):
        pass

    @abstractmethod
    def get_all_by_user_idx(self, user_idx: int):
        pass


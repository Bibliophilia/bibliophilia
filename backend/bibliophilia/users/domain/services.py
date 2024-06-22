import logging
from typing import Optional

from backend.bibliophilia.users import settings
from backend.bibliophilia.users.domain.boundaries import UserRepository, ReviewRepository, GroupRepository
from backend.bibliophilia.users.domain.models.input import UserCreate, ReviewCreate, GroupCreate
from fastapi import status, HTTPException

from backend.bibliophilia.users.domain.models.output import ReviewCard
from backend.bibliophilia.users.domain.models.schemas import User, Review, Group


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def create(self, user: UserCreate) -> Optional[User]:
        user = self.repository.create_user(user)
        return user


class ReviewService:
    def __init__(self, review_repository: ReviewRepository, user_repository: UserRepository):
        self.user_repository = user_repository
        self.review_repository = review_repository

    def create_review(self, review: ReviewCreate) -> (bool, status):
        review = self.review_repository.create_review(review)
        if review:
            logging.info(f"review created: book {review.book_idx}, user {review.user_idx}")
            return True, status.HTTP_201_CREATED
        else:
            return False, status.HTTP_400_BAD_REQUEST

    def read_review(self, book_idx: int, user_idx: str) -> Optional[Review]:
        return self.review_repository.read_review(book_idx, user_idx)

    def read_reviews(self, book_idx: int, page: int) -> list[ReviewCard]:
        reviews = self.review_repository.read_reviews(book_idx)
        users_idxs: list[str] = [review.user_idx for review in reviews]
        users: list[User] = self.user_repository.get_users(users_idxs)
        user_map: dict[str, str] = {user.email: user.name for user in users}
        review_cards = [ReviewCard(rating=review.rating,
                                   review=review.review,
                                   username=user_map[review.user_idx]) for review in reviews]
        return review_cards[(settings.REVIEWS_IN_PAGE * (page - 1)): (settings.REVIEWS_IN_PAGE * page)]

    def read_rating(self, book_idx: int) -> float:
        rating = self.review_repository.read_rating(book_idx)
        if rating is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No book with idx \"{book_idx}\"")
        return rating



class GroupService:

    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def create(self, group: GroupCreate) -> Optional[tuple[Group, list[str]]]:
        return self.group_repository.create(group)

    def edit(self, old_group_name: str, group: GroupCreate) -> Optional[tuple[Group, list[str]]]:
        return self.group_repository.edit(old_group_name, group)

    def delete(self, group_name: str, user_idx: int):
        self.group_repository.delete(group_name, user_idx)

    def get_all_by_user_idx(self, user_idx: int) -> list[tuple[Group, list[str]]]:
        return self.group_repository.get_all_by_user_idx(user_idx)


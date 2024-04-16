from typing import Optional

from bibliophilia.users.data.store.interfaces import DBUserStorage, ReviewStorage
from bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from bibliophilia.users.domain.models.schemas import User, Review
from sqlmodel import Session, select


class DBUserStorageImpl(DBUserStorage):
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, user: UserCreate) -> Optional[User]:
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.email == user.email)).one_or_none()
            if user:
                return None
            db_user = User.from_orm(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user


class ReviewStorageImpl(ReviewStorage):
    def __init__(self, engine):
        self.engine = engine

    def create_review(self, review: ReviewCreate) -> Optional[Review]:
        with Session(self.engine) as session:
            db_review = Review.from_orm(review)
            session.add(db_review)
            session.commit()
            session.refresh(db_review)
            return db_review

    def read_review(self, book_idx: int, user_idx: str) -> Optional[Review]:
        with Session(self.engine) as session:
            return session.exec(select(Review).where(
                Review.book_idx == book_idx and Review.user_idx == user_idx
            )).one_or_none()

    def read_reviews(self, book_idx: int) -> list[Review]:
        with Session(self.engine) as session:
            return session.query(Review).filter(Review.book_idx.in_([book_idx])).all()

    def update_review(self, review: ReviewCreate) -> Optional[Review]:
        with Session(self.engine) as session:
            db_review = session.exec(select(Review).where(
                Review.book_idx == review.book_idx and Review.user_idx == review.user_idx)).one_or_none()
            if db_review in None:
                return None
            db_review.rating = review.rating
            db_review.review = review.review
            session.commit()
            session.refresh(db_review)
            return db_review

    def delete_review(self, review: Review) -> bool:
        with Session(self.engine) as session:
            session.delete(review)
            session.commit()
            return True

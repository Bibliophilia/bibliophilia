from typing import Optional

from fastapi import Depends

from backend.bibliophilia.core.dependencies import get_session
from backend.bibliophilia.users.data.store.interfaces import UserStorage, ReviewStorage, GroupStorage
from backend.bibliophilia.users.domain.models.input import UserCreate, ReviewCreate, GroupCreate
from backend.bibliophilia.users.domain.models.schemas import User, Review, Group
from sqlmodel import Session, select


class DBUserStorageImpl(UserStorage):
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, user: UserCreate) -> Optional[User]:
        with Session(self.engine) as session:
            db_user = session.exec(select(User).where(User.email == user.email)).one_or_none()
            if db_user:
                return db_user
            db_user = User.from_orm(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def get_users(self, users_idxs: list[str]) -> list[User]:
        with Session(self.engine) as session:
            return session.query(User).filter(User.email.in_(users_idxs)).all()


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


class GroupStorageImpl(GroupStorage):

    def __init__(self, engine):
        self.engine = engine

    def create(self, group: GroupCreate) -> Optional[tuple[Group, list[str]]]:
        with Session(self.engine) as session:
            db_group = session.exec(select(Group)
                                    .where(Group.group_name == group.group_name)
                                    .where(Group.creator_idx == group.creator_idx)
                                    ).one_or_none()
            if db_group:
                return None

            users = []
            users_email = []
            for group_user in group.users:
                user = session.exec(select(User).where(User.email == group_user)).one_or_none()
                if user is None:
                    raise Exception(f"User with email {group_user} not found!")
                users.append(user)
                users_email.append(user.email)
            db_group = Group(group_name=group.group_name, creator_idx=group.creator_idx, users=users)
            session.add(db_group)
            session.commit()
            session.refresh(db_group)
            return db_group, users_email

    def edit(self, old_group_name: str, group: GroupCreate) -> Optional[tuple[Group, list[str]]]:
        with Session(self.engine) as session:
            db_group = session.exec(select(Group)
                                    .where(Group.group_name == group.group_name)
                                    .where(Group.creator_idx == group.creator_idx)
                                    ).one_or_none()

            users = []
            users_email = []
            for group_user in group.users:
                user = session.exec(select(User).where(User.email == group_user)).one_or_none()
                if user is None:
                    raise Exception(f"User with email {group_user} not found!")
                users.append(user)
                users_email.append(user.email)

            if old_group_name == group.group_name:
                db_group.users = users
                session.commit()
                session.refresh(db_group)
                return db_group, users_email

            if db_group:
                return None

            db_group = session.exec(select(Group)
                                    .where(Group.group_name == old_group_name)
                                    .where(Group.creator_idx == group.creator_idx)
                                    ).one_or_none()

            if db_group is None:
                return None

            db_group.group_name = group.group_name
            db_group.users = users
            session.commit()
            session.refresh(db_group)
            return db_group, users_email

    def delete(self, group_name: str, user_idx: int):
        with Session(self.engine) as session:
            db_group = session.exec(select(Group)
                                    .where(Group.group_name == group_name)
                                    .where(Group.creator_idx == user_idx)
                                    ).one_or_none()
            if db_group is None:
                raise Exception(f"Group with name {group_name} not found!")

            session.delete(db_group)
            session.commit()

    def get_all_by_user_idx(self, user_idx: int) -> list[tuple[Group, list[str]]]:
        with Session(self.engine) as session:
            groups = session.exec(select(Group).where(Group.creator_idx == user_idx)).all()
            groups_list = []
            for group in groups:
                users_email = []
                for user in group.users:
                    users_email.append(user.email)
                groups_list.append((group, users_email))
            return groups_list




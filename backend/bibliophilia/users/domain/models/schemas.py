from backend.bibliophilia.books.domain.models.schemas import Book, UserBookCredentials
from backend.bibliophilia.users.domain.models.basic import UserBase, ExtendedReviewBase, ExtendedGroupBase
from sqlmodel import Field, Relationship

from backend.bibliophilia.users.domain.models.basic import GroupBase

from backend.bibliophilia.core.models import BPModel


class UserGroupLink(BPModel, table=True):
    user_idx: int = Field(None, foreign_key="users.idx", primary_key=True)
    group_idx: int = Field(None, foreign_key="groups.idx", primary_key=True)


class User(UserBase, table=True):
    __tablename__ = "users"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    email: str = Field(None, unique=True)
    reviews: list["Review"] = Relationship(back_populates="user")
    groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
    books: list["Book"] = Relationship(back_populates="users", link_model=UserBookCredentials)


class Review(ExtendedReviewBase, table=True):
    __tablename__ = "reviews"
    book_idx: int = Field(foreign_key="books.idx", primary_key=True)
    user_idx: str = Field(foreign_key="users.email", primary_key=True)
    user: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")


class Group(GroupBase, table=True):
    __tablename__ = "groups"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    group_name: str = Field(None)
    creator_idx: int = Field(foreign_key="users.idx")
    users: list["User"] = Relationship(back_populates="groups", link_model=UserGroupLink, sa_relationship_kwargs={"lazy":"joined"})

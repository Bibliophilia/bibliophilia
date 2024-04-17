from bibliophilia.books.domain.models.schemas import Book
from bibliophilia.users.domain.models.basic import UserBase, ExtendedReviewBase
from sqlmodel import Field, Relationship


class User(UserBase, table=True):
    __tablename__ = "users"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    email: str = Field(None, unique=True)
    reviews: list["Review"] = Relationship(back_populates="user")


class Review(ExtendedReviewBase, table=True):
    __tablename__ = "reviews"
    book_idx: int = Field(foreign_key="books.idx", primary_key=True)
    user_idx: str = Field(foreign_key="users.email", primary_key=True)
    user: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")

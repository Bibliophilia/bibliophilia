from bibliophilia.books.domain.models.schemas import Book
from bibliophilia.users.domain.models.basic import UserBase, ReviewBase
from sqlmodel import Field, Relationship


class User(UserBase, table=True):
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})


class Review(ReviewBase, table=True):
    __tablename__ = "reviews"
    book_idx: int = Field(foreign_key="books.idx")
    user_idx: str = Field(foreign_key="users.mail")
    user: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")
    # TODO: User

from enum import Enum, auto

from sqlmodel import Field, Relationship

from backend.bibliophilia.books.domain.models.basic import ExtendedBookBase, FileFormat, BookFileBase
from backend.bibliophilia.books import settings
from backend.bibliophilia.core.models import BPModel
from backend.bibliophilia.users.domain.models.schemas import User, UserGroupLink, Group


class CredentialsEnum(Enum):
    SEE = "1"
    SEE_READ = "2"
    SEE_READ_DOWNLOAD = "3"
    NONE = "4"


class GroupBookCredentials(BPModel, table=True):
    #group_idx: int = Field(None, foreign_key="groups.idx", primary_key=True)
    group_idx: int = Field(None, foreign_key="group.idx", primary_key=True)
    #user_group_idx: int = Field(None, foreign_key="user_group.idx", primary_key=True)
    book_idx: int = Field(None, foreign_key="books.idx", primary_key=True)
    credentials: CredentialsEnum


class UserBookCredentials(BPModel, table=True):
    #group_idx: int = Field(None, foreign_key="groups.idx", primary_key=True)
    user_idx: int = Field(None, foreign_key="users.idx", primary_key=True)
    #user_group_idx: int = Field(None, foreign_key="user_group.idx", primary_key=True)
    book_idx: int = Field(None, foreign_key="books.idx", primary_key=True)
    credentials: CredentialsEnum


class Book(ExtendedBookBase, table=True):
    __tablename__ = "books"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})

    files: list["BookFile"] = Relationship(back_populates="book")
    reviews: list["Review"] = Relationship(back_populates="book")

    public: Credentials
    users: list["User"] = Relationship(back_populates="books", link_model=UserBookCredentials)
    groups: list["Group"] = Relationship(back_populates="books", link_model=GroupBookCredentials)
    #user_group: list["UserGroupLink"] = Relationship(back_populates="books", link_model=UserBookCredentials)

    @property
    def image_url(self) -> str:
        return f"{settings.URL}/images/{self.idx}.{settings.IMAGE_EXTENSION}"

    @property
    def image_path(self) -> str:
        return f"{settings.IMAGES_PATH}/{self.idx}.{settings.IMAGE_EXTENSION}"


class BookFile(BookFileBase, table=True):
    __tablename__ = "files"
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    format: FileFormat
    book_idx: int = Field(foreign_key="books.idx")

    book: Book = Relationship(back_populates="files")

    @property
    def bookfile_path(self) -> str:
        return f"{settings.FILES_PATH}/{self.book_idx}.{self.format.value}"

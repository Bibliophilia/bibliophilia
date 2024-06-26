from typing import Optional, List

from fastapi import UploadFile

from backend.bibliophilia.books import settings
from backend.bibliophilia.books.domain.models.basic import ExtendedBookBase, BookFileBase, FileFormat, GenreBase, AuthorBase, \
    OverExtendedBookBase

from backend.bibliophilia.books import settings
from backend.bibliophilia.books.domain.models.basic import ExtendedBookBase, BookFileBase, FileFormat
from backend.bibliophilia.books.domain.models.schemas import RightsEnum
from backend.bibliophilia.core.models import BPModel


class BookCreateInfo(ExtendedBookBase):
    author: list[str]
    genre: list[str]


class BookCreate(BookCreateInfo):
    publisher: str
    image: Optional[UploadFile] = None
    files: list[UploadFile] = []
    tokens: list[float] = []
    public: RightsEnum = RightsEnum.NONE


class BookUpdate(BookCreate):
    pass


class BookSearch(OverExtendedBookBase):
    publisher: str
    tokens: list[float]


class BookFileCreate(BookFileBase):
    format: FileFormat


class BookFileSave(BookFileBase):
    file: UploadFile

    @property
    def bookfile_path(self) -> str:
        extension = self.file.filename.split('.')[-1]
        return f"{settings.FILES_PATH}/{self.book_idx}.{extension}"


class ImageFileSave(BookFileBase):
    image: Optional[UploadFile]

    @property
    def image_url(self) -> str:
        return f"{settings.URL}/images/{self.book_idx}.{settings.IMAGE_EXTENSION}"

    @property
    def image_path(self) -> str:
        return f"{settings.IMAGES_PATH}/{self.book_idx}.{settings.IMAGE_EXTENSION}"


class Rights(BPModel):
    users_see: list[str]
    users_see_read: list[str]
    users_see_read_download: list[str]
    group_see: list[str]
    group_see_read: list[str]
    group_see_read_download: list[str]
    is_see_all: bool
    is_see_read_all: bool
    is_see_read_download_all: bool


class GenreCreate(GenreBase):
    name: str


class AuthorCreate(AuthorBase):
    name: str


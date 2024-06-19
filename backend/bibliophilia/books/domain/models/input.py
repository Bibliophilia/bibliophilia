from typing import Optional, List

from fastapi import UploadFile

from bibliophilia.books import settings
from bibliophilia.books.domain.models.basic import ExtendedBookBase, BookFileBase, FileFormat, GenreBase, AuthorBase, \
    OverExtendedBookBase


class BookCreateInfo(ExtendedBookBase):
    author: list[str]
    genre: list[str]


class BookCreate(BookCreateInfo):
    image: Optional[UploadFile] = None
    files: list[UploadFile] = []
    tokens: list[float] = []


class BookUpdate(BookCreate):
    pass


class BookSearch(OverExtendedBookBase):
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


class GenreCreate(GenreBase):
    name: str


class AuthorCreate(AuthorBase):
    name: str

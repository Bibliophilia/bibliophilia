from typing import Optional

import numpy
from fastapi import UploadFile

from bibliophilia.server import settings
from bibliophilia.server.domain.models.basic.books import ExtendedBookBase, BookBase, BookFileBase, FileFormat


class BookCreate(ExtendedBookBase):
    image: Optional[UploadFile]
    files: list[UploadFile]
    tokens: list[float] = []


class BookSearch(ExtendedBookBase):
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

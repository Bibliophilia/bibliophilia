from typing import Optional

from bibliophilia.users.data.store.interfaces import DBUserStorage
from bibliophilia.users.domain.boundaries import UserRepository
from bibliophilia.users.domain.models.input import UserCreate
from bibliophilia.users.domain.models.schemas import User


class UserRepositoryImpl(UserRepository):
    def __init__(self, db_storage: DBUserStorage):
        self.db_storage = db_storage

    def create_book(self, user: UserCreate) -> Optional[User]:
        db_user = self.db_storage.create_user(user)
        return db_user

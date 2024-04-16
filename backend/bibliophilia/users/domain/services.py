from typing import Optional

from backend.bibliophilia.users.domain.boundaries import UserRepository
from backend.bibliophilia.users.domain.models.input import UserCreate
from fastapi import status

from backend.bibliophilia.users.domain.models.schemas import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def create(self, user: UserCreate) -> Optional[User]:
        user = self.repository.create_user(user)
        return user

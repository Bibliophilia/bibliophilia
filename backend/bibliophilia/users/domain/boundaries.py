from abc import ABC, abstractmethod
from typing import Optional

from backend.bibliophilia.users.domain.models.input import UserCreate
from backend.bibliophilia.users.domain.models.schemas import User


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: UserCreate) -> Optional[User]:
        pass

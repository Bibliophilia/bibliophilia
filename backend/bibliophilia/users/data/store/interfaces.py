from abc import ABC, abstractmethod
from typing import Optional

from bibliophilia.users.domain.models.input import UserCreate
from bibliophilia.users.domain.models.schemas import User


class DBUserStorage(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> Optional[User]:
        pass

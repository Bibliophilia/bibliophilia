from typing import Optional

from backend.bibliophilia.users.data.store.interfaces import DBUserStorage
from backend.bibliophilia.users.domain.models.input import UserCreate
from backend.bibliophilia.users.domain.models.schemas import User
from sqlmodel import Session, select


class DBUserStorageImpl(DBUserStorage):
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, user: UserCreate) -> Optional[User]:
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.email == user.email)).one_or_none()
            if user:
                return None
            db_user = User.from_orm(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

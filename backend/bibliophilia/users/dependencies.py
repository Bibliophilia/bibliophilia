from backend.bibliophilia.core.dependencies import engine
from backend.bibliophilia.users.data.repositories import UserRepositoryImpl
from backend.bibliophilia.users.data.store.storages import DBUserStorageImpl
from backend.bibliophilia.users.domain.services import UserService

db_storage = DBUserStorageImpl(engine)

user_repository = UserRepositoryImpl(db_storage)

user_service = UserService(user_repository)
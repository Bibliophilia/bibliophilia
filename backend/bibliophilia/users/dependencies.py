from bibliophilia.core.dependencies import engine
from bibliophilia.users.data.repositories import UserRepositoryImpl
from bibliophilia.users.data.store.storages import DBUserStorageImpl
from bibliophilia.users.domain.services import UserService

db_storage = DBUserStorageImpl(engine)

user_repository = UserRepositoryImpl(db_storage)

user_service = UserService(user_repository)
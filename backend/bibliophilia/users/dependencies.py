from bibliophilia.core.dependencies import engine
from bibliophilia.users.data.repositories import UserRepositoryImpl, ReviewRepositoryImpl
from bibliophilia.users.data.store.storages import DBUserStorageImpl, ReviewStorageImpl
from bibliophilia.users.domain.services import UserService, ReviewService

db_storage = DBUserStorageImpl(engine)

user_repository = UserRepositoryImpl(db_storage)
user_service = UserService(user_repository)


review_storage = ReviewStorageImpl(engine)
review_repository = ReviewRepositoryImpl(review_storage=review_storage)
review_service = ReviewService(review_repository=review_repository)

from backend.bibliophilia.core.dependencies import engine
from backend.bibliophilia.users.data.repositories import UserRepositoryImpl, ReviewRepositoryImpl, GroupRepositoryImpl
from backend.bibliophilia.users.data.store.storages import DBUserStorageImpl, ReviewStorageImpl, GroupStorageImpl
from backend.bibliophilia.users.domain.services import UserService, ReviewService, GroupService

db_storage = DBUserStorageImpl(engine)
user_repository = UserRepositoryImpl(user_storage=db_storage)
user_service = UserService(user_repository=user_repository)


review_storage = ReviewStorageImpl(engine)
review_repository = ReviewRepositoryImpl(review_storage=review_storage)
review_service = ReviewService(review_repository=review_repository, user_repository=user_repository)

group_storage = GroupStorageImpl(engine)
group_repository = GroupRepositoryImpl(group_storage)
group_service = GroupService(group_repository)

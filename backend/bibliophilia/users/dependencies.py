from bibliophilia.core.dependencies import engine
from bibliophilia.users.data.repositories import ReviewRepositoryImpl
from bibliophilia.users.data.store.storages import ReviewStorageImpl
from bibliophilia.users.domain.services import ReviewService


review_storage = ReviewStorageImpl(engine)
review_repository = ReviewRepositoryImpl(review_storage=review_storage)
review_service = ReviewService(review_repository=review_repository)

import logging

import bibliophilia.books.settings as settings
from bibliophilia.books.data.repositories import BookRepositoryImpl, SearchRepositoryImpl
from bibliophilia.books.data.store.storages import DBBookStorageImpl, FSBookStorageImpl, ESBookStorageImpl
from bibliophilia.books.domain.services import BookService, SearchService
from bibliophilia.core.dependencies import es, engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

search_storage = ESBookStorageImpl(es)
db_storage = DBBookStorageImpl(engine)
fs_storage = FSBookStorageImpl(url=settings.URL,
                               images_path=settings.IMAGES_PATH,
                               files_path=settings.FILES_PATH,
                               image_extension=settings.IMAGE_EXTENSION)

book_repository = BookRepositoryImpl(fs_storage=fs_storage,
                                     db_storage=db_storage,
                                     search_storage=search_storage)
search_repository = SearchRepositoryImpl(search_storage=search_storage)

book_service = BookService(book_repository=book_repository)
search_service = SearchService(search_repository=search_repository,
                               book_repository=book_repository)

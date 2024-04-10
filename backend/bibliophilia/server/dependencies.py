import logging

from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bibliophilia.server import settings
from bibliophilia.server.data.repositories.books import BookRepository, BookRepositoryImpl, SearchRepositoryImpl
from bibliophilia.server.data.storages.books import DBBookStorageImpl, FSBookStorageImpl, ESBookStorageImpl
from bibliophilia.server.domain.services.books import BookService, SearchService

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
index_mapping = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "author": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "tokens": {
                "type": "dense_vector",
                "dims": 96
            }
        }
    }
}
es.indices.create(index="books", ignore=400, body=index_mapping)

Base = declarative_base()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


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

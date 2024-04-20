from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bibliophilia.books.domain.entity.facet import Facet

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
book_mapping = {
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
es.indices.create(index="books", ignore=400, body=book_mapping)
for facet in Facet:
    mapping = {
        "mappings": {
            "properties": {
                "value": {
                    "type": "text"
                }
            }
        }
    }
    es.indices.create(index=facet, ignore=400, body=mapping)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

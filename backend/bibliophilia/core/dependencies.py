from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bibliophilia.books.domain.entity.facet import Facet

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
text_keyword_mapping = {
    "value": {
        "type": "nested",
        "fields": {
            "key": {
                "type": "keyword",
                "ignore_above": 256
            },
            "text": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }
}
book_mapping = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "author": {
                "type": "nested",
                "properties": text_keyword_mapping
            },
            "genre": {
                "type": "nested",
                "properties": text_keyword_mapping
            },
            "year": "short",
            "publisher": "text",
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
Base = declarative_base()
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

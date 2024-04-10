from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
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


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

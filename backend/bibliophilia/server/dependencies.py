import json

from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
es.indices.create(index="books", ignore=400)
BOOKS_IN_PAGE = 10
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

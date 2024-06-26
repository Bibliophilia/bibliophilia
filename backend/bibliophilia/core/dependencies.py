from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.bibliophilia.books.domain.entity.facet import Facet

engine = create_engine("postgresql+psycopg2://bibliophilia:bibliophilia@postgres:5432/bibliophiliadb", echo=True)
es = Elasticsearch('http://elasticsearch:9200')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
text_keyword_mapping = {
            "key": {
                "type": "keyword",
                "ignore_above": 256
            },
            "text": {
                "type": "text",
                "analyzer": "standard"
            }
        }

book_mapping = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "author": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "object",
                        "properties": text_keyword_mapping
                    }
                }
            },
            "genre": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "object",
                        "properties": text_keyword_mapping
                    }
                }
            },
            "year": {
                "type": "short"
            },
            "publisher": {
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

response = es.indices.create(index="books", ignore=400, body=book_mapping)

if 'acknowledged' in response:
    if response['acknowledged']:
        print("Index 'books' created successfully.")
    else:
        print("Index 'books' creation failed.")
else:
    print("Error:", response)


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

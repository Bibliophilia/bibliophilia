from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class ElasticsearchService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.es = Elasticsearch('http://elasticsearch:9200')

    def save_book(self, book_id, book_data):
        res = self.es.index(index='books', id=book_id, document=book_data)
        return res['result']

    def search_book(self, text, size=10):
        query = Q('bool', should=[
            Q('match', title=text),
            Q('match', author=text)
        ])
        search = Search(using=self.es, index="books").query(query)
        response = search.execute()
        serialized_results = [hit.to_dict() for hit in response.hits]
        return serialized_results

    def get_book(self, book_id):
        return self.es.search(index='books', id=book_id)

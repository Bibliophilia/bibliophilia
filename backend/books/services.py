from elasticsearch import Elasticsearch


class ElasticsearchService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200')

    def save_book(self, book_id, book_data):
        res = self.es.index(index='books', id=book_id, document=book_data)
        return res['result']

    def query(self, request, title, size=10):
        return self.query(request=request, title=title, size=size)

    def get_book(self, book_id):
        return self.query(index='books', id=book_id)


class FilesystemService:
    def save_image(self, book_id, image):
        # Реализация сохранения изображения в файловой системе по book_id
        pass

    def save_book_file(self, book_id, file):
        # Реализация сохранения файла книги в файловой системе по book_id
        pass
from elasticsearch import Elasticsearch


def run():
    # Подключение к экземпляру Elasticsearch
    es = Elasticsearch('http://localhost:9200')

    book = {
        "title": "Romeo and Juliet2",
        "author": "William Shakespeare",
        "year": "2023",
        "genre": "Tragedy",
        "description": "The tragedy of William Shakespeare, which tells about the love of a young man and a girl from two warring Veronese families — Montagues and Capulets."
    }

    # Индексирование данных в Elasticsearch
    res = es.index(index='book1', id=2, document=book)
    print(res['result'])


if __name__ == "__main__":
    run()

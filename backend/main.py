from elasticsearch import Elasticsearch


def run():
    # Подключение к экземпляру Elasticsearch
    es = Elasticsearch('http://localhost:9200')

    # Пример данных для индексации
    data = {
        "author": "John Doe",
        "text": "Elasticsearch is a powerful search engine",
        "timestamp": "2023-11-08"
    }

    # Индексирование данных в Elasticsearch
    res = es.index(index='something', id=1, document=data)
    print(res['result'])


if __name__ == "__main__":
    run()

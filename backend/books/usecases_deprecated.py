import json

from elasticsearch_dsl import Q

from .services_deprecated import ElasticsearchService


def perform_search(query):
    return perform_base_search(query)


def perform_base_search(text):
    query = Q('bool', should=[
        Q('match', title=text),
        Q('match', author=text)
    ])
    books_info = ElasticsearchService().apply_search(query)

    print(books_info)
    return books_info


def save_book(book):
    book_data = {
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "formats": [file.file_format for file in book.files.all()],
        "image_url": f"book-images/{book.id}.jpg",
        "file_path": f"private/book-files/{book.id}",
        "tokens": []
    }
    return ElasticsearchService().save_book(book.id, book_data)

    # FilesystemService().save_image(book.id, book.image)
    # for file in book.files.all():
    #     FilesystemService().save_book_file(book.id, file)


def get_book_info(book_id):
    ElasticsearchService().get_book(book_id)

# API Documentation

## Books

### Add a Book

POST upload/

Adds a new book to the library.

#### `Request`
```json
{
  "title": "Book Title",
  "author": "Book Author",
  "description": "Book Description",
  "image": "book_image.jpg",
  "files": [
    {
      "file": "book_file.pdf",
      "file_format": "PDF"
    },
    {
      "file": "another_book_file.txt",
      "file_format": "TXT"
    }
  ],
  "links": "Some Link"
}
```

#### Response

- Status: `201 Created` if successful
- Status: `4xx` or `5xx` if an error occurs

---
### Search Books

GET search?q={text-search}&page={page-number}

Searches for books.

#### Request

Send a GET request with the `q` parameter containing the query text.

#### Response

```json
[
  {
    "id": 1,
    "title": "Book Title",
    "author": "Book Author",
    "description": "Book Description",
    "image_url": "http://bibliophilia.com/images/some_image.jpg"
  },
  {
    "id": 2,
    "title": "Another Book",
    "author": "Another Author",
    "description": "Description of another book",
    "image_url": "http://bibliophilia.com/images/some_image.jpg"
  }
]
```

- Status: `200 OK` if successful
- Status: `4xx` or `5xx` if an error occurs

---

### Get Book Details

GET /books/{id}/

Fetches details of a book by its `id`.

#### Response

```json
{
  "id": 1,
  "title": "Book Title",
  "author": "Book Author",
  "description": "Book Description",
  "image_url": "http://bibliophilia.com/images/some_image.jpg",
  "links": "Some Link"
}
```

- Status: `200 OK` if successful
- Status: `404 Not Found` if the book with specified ID doesn't exist
- Status: `4xx` or `5xx` if an error occurs

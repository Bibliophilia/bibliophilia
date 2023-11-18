# API Documentation

## Books

### Add a Book

POST /books/add/

Adds a new book to the library.

#### Request

```json
{
  "title": "Book Title",
  "author": "Book Author",
  "description": "Book Description"
}
```

#### Response

- Status: `201 Created` if successful
- Status: `4xx` or `5xx` if an error occurs

---

### Search Books

GET /books/search/?q=query

Searches for books based on the `query`.

#### Request

Send a GET request with the `q` parameter containing the query text.

#### Response

```json
[
  {
    "id": 1,
    "title": "Book Title",
    "author": "Book Author",
    "description": "Book Description"
  },
  {
    "id": 2,
    "title": "Another Book",
    "author": "Another Author",
    "description": "Description of another book"
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
  "description": "Book Description"
}
```

- Status: `200 OK` if successful
- Status: `404 Not Found` if the book with specified ID doesn't exist
- Status: `4xx` or `5xx` if an error occurs

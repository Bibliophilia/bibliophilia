import os
from dotenv import load_dotenv

#load_dotenv()

#CLIENT_ID = os.environ.get('client-id', None)
#CLIENT_SECRET = os.environ.get('client-secret', None)

CLIENT_ID = "google client id ask me"
CLIENT_SECRET = 'google client secret also ask me'


URL = "http://localhost:3000"
BOOKS_IN_PAGE = 10
FILES_PATH = "/app/private/files"
IMAGES_PATH = "/app/public/images"
IMAGE_EXTENSION = "jpg"

MEDIA_TYPES = {"pdf": "application/pdf",
               "txt": "text/plain",
               "epub": "application/epub+zip",
               "doc": "application/msword"}
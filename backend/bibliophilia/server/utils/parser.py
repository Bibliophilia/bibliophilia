import asyncio

import numpy
from fastapi import UploadFile

from bibliophilia.server.domain.models.input.books import BookCreate
from bibliophilia.server.domain.models.basic.books import FileFormat
import spacy
from docx import Document
import PyPDF2
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
from collections import Counter


class Parser:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def book_to_tokens(self, book: BookCreate):
        text = None
        file_extensions = [file.filename.split('.')[1] for file in book.files]
        if FileFormat.TXT.value in file_extensions:
            book_file = next(
                book_file for book_file in book.files if book_file.filename.split('.')[1] == FileFormat.TXT.value)
            text = self._file_TXT_to_text(book_file)
        # elif FileFormat.DOC.value in book.formats:
        #    book_file = next(book_file for book_file in book.files if book_file.filename.split('.')[1] == FileFormat.DOC.value)
        #    text = self._file_DOC_to_text(book_file)
        elif FileFormat.PDF.value in book.formats:
            book_file = next(
                book_file for book_file in book.files if book_file.filename.split('.')[1] == FileFormat.PDF.value)
            text = self._file_PDF_to_text(book_file)
        elif FileFormat.EPUB.value in book.formats:
            book_file = next(
                book_file for book_file in book.files if book_file.filename.split('.')[1] == FileFormat.EPUB.value)
            text = self._file_EPUB_to_text(book_file)
        else:
            raise Exception("The book doesn't have the right format!")

        return self.text_to_tokens(text)

    def text_to_tokens(self, text) -> numpy.ndarray:
        doc = self.nlp(text)
        # tokens = [entity.label_ for entity in doc.ents]
        # counter = Counter(tokens)
        # top_tokens = [item[0] for item in counter.most_common(10)]
        vector = doc.vector
        return vector.tolist()

    def _file_TXT_to_text(self, book_file: UploadFile):
        text = asyncio.run(book_file.read())
        return text

    # TODO: read DOCX file
    def _file_DOC_to_text(self, book_file: UploadFile):
        path = book_file.file_path
        doc = Document(path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text

        return text

    def _file_PDF_to_text(self, book_file: UploadFile):
        text = asyncio.run(book_file.read())
        pdf_reader = PyPDF2.PdfFileReader(text)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        return text

    def _file_EPUB_to_text(self, book_file: UploadFile):
        text = asyncio.run(book_file.read())
        book = epub.read_epub(text)
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content()
            soup = BeautifulSoup(content)
            text += soup.get_text()
        return text

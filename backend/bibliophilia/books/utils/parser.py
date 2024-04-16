import asyncio
import io
import logging

import numpy
from fastapi import UploadFile

from bibliophilia.books.domain.models.input import BookCreate
from bibliophilia.books.domain.models.basic import FileFormat
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
        book_files = {}
        for file in book.files:
            file_format = FileFormat.get_by_name(file.filename.split('.')[-1])
            book_files[file_format] = file
        if FileFormat.TXT in book_files.keys():
            text = self._file_TXT_to_text(book_files[FileFormat.TXT])
        # elif FileFormat.DOC.value in book.formats:
        #    book_file = next(book_file for book_file in book.files if book_file.filename.split('.')[1] == FileFormat.DOC.value)
        #    text = self._file_DOC_to_text(book_file)
        elif FileFormat.PDF in book_files.keys():
            text = self._file_PDF_to_text(book_files[FileFormat.PDF])
        elif FileFormat.EPUB.value in book_files.keys():
            text = self._file_EPUB_to_text(book_files[FileFormat.EPUB])
        else:
            raise Exception("The book doesn't have the right format!")

        return self.text_to_tokens(text)

    def text_to_tokens(self, text) -> list[float]:
        doc = self.nlp(text)
        # tokens = [entity.label_ for entity in doc.ents]
        # counter = Counter(tokens)
        # top_tokens = [item[0] for item in counter.most_common(10)]
        vector = doc.vector
        return vector.tolist()

    def _file_TXT_to_text(self, book_file: UploadFile) -> str:
        text = asyncio.run(book_file.read())
        logging.info(f"Text: {text}")
        return text.decode('utf-8')

    # TODO: read DOCX file
#    def _file_DOC_to_text(self, book_file: UploadFile):
#        path = book_file.file_path
#        doc = Document(path)
#        text = ""
#        for paragraph in doc.paragraphs:
#            text += paragraph.text
#
#        return text

    def _file_PDF_to_text(self, book_file: UploadFile) -> str:
        text_bytes = asyncio.run(book_file.read())
        text = ""

        with io.BytesIO(text_bytes) as file_buffer:
            pdf_reader = PyPDF2.PdfReader(file_buffer)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        return text

    def _file_EPUB_to_text(self, book_file: UploadFile) -> str:
        text = asyncio.run(book_file.read())
        book = epub.read_epub(text)
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content()
            soup = BeautifulSoup(content)
            text += soup.get_text()
        return text

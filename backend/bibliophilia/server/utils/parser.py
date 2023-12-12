from backend.bibliophilia.server.db.tables import Book, FileFormat, BookFile
import spacy
from docx import Document
import PyPDF2
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup


class BookParser:

    def book_to_tokens(self, book: Book):
        text = None
        if FileFormat.TXT.name in book.formats:
            book_file = next(book_file for book_file in book.files if book_file.file_format == FileFormat.TXT.name)
            text = self._file_TXT_to_text(book_file)
        elif FileFormat.DOC.name in book.formats:
            book_file = next(book_file for book_file in book.files if book_file.file_format == FileFormat.DOC.name)
            text = self._file_DOC_to_text(book_file)
        elif FileFormat.PDF.name in book.formats:
            book_file = next(book_file for book_file in book.files if book_file.file_format == FileFormat.PDF.name)
            text = self._file_PDF_to_text(book_file)
        elif FileFormat.EPUB.name in book.formats:
            book_file = next(book_file for book_file in book.files if book_file.file_format == FileFormat.EPUB.name)
            text = self._file_EPUB_to_text(book_file)
        else:
            raise Exception("The book doesn't have the right format!")

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        tokens = [entity.label_ for entity in doc.ents]
        return list(tokens)

    def _file_TXT_to_text(self, book_file: BookFile):
        path = book_file.file_path
        with open(path, 'r') as file:
            text = file.read()
        return text

    def _file_DOC_to_text(self, book_file: BookFile):
        path = book_file.file_path
        doc = Document(path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text

        return text

    def _file_PDF_to_text(self, book_file: BookFile):
        path = book_file.file_path
        text = ""
        with open(path, 'r') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
        return text

    def _file_EPUB_to_text(self, book_file: BookFile):
        path = book_file.file_path
        text = ""
        book = epub.read_epub(path)
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content()
            soup = BeautifulSoup(content)
            text += soup.get_text()
        return text

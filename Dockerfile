FROM python:3.11

COPY ./backend ./backend
RUN pip3 install -U spacy
RUN python -m spacy download en
RUN pip3 install python-docx
RUN pip3 install PyPDF2
RUN pip3 install EbookLib
RUN pip3 install beautifulsoup4
RUN pip3 install ./backend
CMD ["python3", "-m", "uvicorn", "bibliophilia.server.main:bibliophilia_app", "--host", "0.0.0.0"]
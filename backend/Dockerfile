FROM python:3.11

COPY . ./backend
RUN pip install -U pip setuptools wheel spacy
RUN pip install --upgrade urllib3 pip
RUN pip install schedule
RUN pip install ./backend/resources/en_core_web_sm-3.7.1-py3-none-any.whl
RUN pip install ./backend/resources/en_core_web_sm-3.7.1.tar.gz
RUN pip install -r ./backend/requirements.txt
RUN pip install ./backend
CMD ["python", "-m", "uvicorn", "backend.bibliophilia.api:bibliophilia_app", "--host", "0.0.0.0", "--port", "8000"]
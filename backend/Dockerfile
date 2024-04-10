FROM python:3.11

COPY . ./backend
RUN pip install -U pip setuptools wheel
RUN pip install -r ./backend/requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm
RUN pip install ./backend
CMD ["python3", "-m", "uvicorn", "bibliophilia.server.main:bibliophilia_app", "--host", "0.0.0.0"]
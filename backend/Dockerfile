FROM python:3.11

COPY . ./backend
RUN pip install -U pip setuptools wheel
RUN pip install --upgrade urllib3 pip
RUN pip install -U spacy
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
# RUN python -m spacy download en_core_web_sm
#RUN python -m spacy download ru_core_news_sm
RUN pip install -r ./backend/requirements.txt
RUN pip install ./backend
CMD ["python", "-m", "uvicorn", "bibliophilia.main:bibliophilia_app", "--host", "0.0.0.0"]
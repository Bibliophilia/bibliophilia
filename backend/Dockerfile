FROM python:3.11

RUN mkdir /app
COPY /. /app
COPY pyproject.toml /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 8000

CMD [ "poetry", "run", "wsgi:application", "--bind", "0:8000" ]
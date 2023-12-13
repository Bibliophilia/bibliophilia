FROM python:3.11

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY ./backend ./backend
WORKDIR /backend
RUN poetry install
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
# poetry run python manage.py runserver
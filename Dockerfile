FROM python:3.11

COPY ./backend ./backend
RUN pip3 install ./backend
CMD ["python3", "-m", "uvicorn", "bibliophilia.server.main:bibliophilia_app", "--host", "0.0.0.0"]

import threading
import time

import schedule
from sqlalchemy import func
from sqlmodel import Session, select

from backend.bibliophilia.books.domain.models.schemas import Book
from backend.bibliophilia.core.dependencies import engine
from backend.bibliophilia.users.domain.models.schemas import Review


def update_books_rating():
    with Session(engine) as session:
        list_book_idx_and_rating = session.query(
            Review.book_idx,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.book_idx).all()

        for book_idx_and_rating in list_book_idx_and_rating:
            book = session.exec(select(Book).where(Book.idx == book_idx_and_rating.book_idx)).first()
            book.avg_rating = book_idx_and_rating.avg_rating
            session.add(book)

        session.commit()


#schedule.every().day.at("00:00").do(update_books_rating)
schedule.every().minute.do(update_books_rating)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

from sqlmodel import select, Session

from backend.bibliophilia.books.domain.models.schemas import Book, UserBookRights, RightsEnum, GroupBookRights
from backend.bibliophilia.core.dependencies import es, engine
from backend.bibliophilia.users.domain.models.schemas import User, Group
from fastapi import HTTPException, status


def check_book_right(book_idx: int, user, criteria: str) -> bool:
    if user is None:
        return check_is_public(book_idx)
    else:
        email = user.get('email')
        with Session(engine) as session:
            is_publisher = check_is_publisher(book_idx, email)
            if is_publisher:
                return True

            is_public = check_is_public(book_idx)
            if is_public:
                return True

            user = session.exec(select(User).where(User.email == email)).one_or_none()
            if user is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No user with email \"{email}\"")

            is_user_right = check_is_user_right(book_idx, user.idx, criteria)
            if is_user_right:
                return True

            is_group_right = check_is_group_right(book_idx, user.idx, criteria)
            if is_group_right:
                return True
                    
            return False


def check_is_public(book_idx: int) -> bool:
    with Session(engine) as session:
        is_public = session.exec(select(Book).where(
            (Book.idx == book_idx) & (
                (Book.public == RightsEnum.SEARCH) | (Book.public == RightsEnum.SEARCH_READ) | (Book.public == RightsEnum.SEARCH_READ_DOWNLOAD)))
        ).one_or_none()
        if is_public:
            return True
        return False
    
    
def check_is_publisher(book_idx: int, email: str) -> bool:
    with Session(engine) as session:
        is_publisher = session.exec(select(Book).where((Book.idx == book_idx) & (Book.publisher == email))).one_or_none()
        if is_publisher:
            return True
        return False


def check_is_user_right(book_idx: int, user_idx: int, criteria: str) -> bool:
    with Session(engine) as session:
        if criteria == "search":
            user_right = session.exec(
                select(UserBookRights).where(
                    (UserBookRights.user_idx == user_idx)
                    & (UserBookRights.book_idx == book_idx)
                    & ((UserBookRights.rights == RightsEnum.SEARCH)
                         | (UserBookRights.rights == RightsEnum.SEARCH_READ)
                         | (UserBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD))
                )
            ).one_or_none()
            if user_right:
                return True
        elif criteria == "read":
            user_right = session.exec(
                select(UserBookRights).where(
                    (UserBookRights.user_idx == user_idx)
                    & (UserBookRights.book_idx == book_idx)
                    & ((UserBookRights.rights == RightsEnum.SEARCH_READ)
                         | (UserBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD))
                )
            ).one_or_none()
            if user_right:
                return True
        elif criteria == "download":
            user_right = session.exec(
                select(UserBookRights).where(
                    (UserBookRights.user_idx == user_idx)
                    & (UserBookRights.book_idx == book_idx)
                    & (UserBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD))
            ).one_or_none()
            if user_right:
                return True
        else:
            Exception(f"No such right criteria \"{criteria}\"")

        return False


def check_is_group_right(book_idx: int, user_idx: int, criteria: str) -> bool:
    with Session(engine) as session:
        if criteria == "search":
            group_rights = session.exec(
                select(GroupBookRights).where(
                    (GroupBookRights.book_idx == book_idx)
                    & ((GroupBookRights.rights == RightsEnum.SEARCH)
                         | (GroupBookRights.rights == RightsEnum.SEARCH_READ)
                         | (GroupBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD))
                )
            ).all()

        elif criteria == "read":
            group_rights = session.exec(
                select(GroupBookRights).where(
                    (GroupBookRights.book_idx == book_idx)
                    & ((GroupBookRights.rights == RightsEnum.SEARCH_READ)
                         | (GroupBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD))
                )
            ).all()

        elif criteria == "download":
            group_rights = session.exec(
                select(GroupBookRights).where(
                    (GroupBookRights.book_idx == book_idx)
                    & (GroupBookRights.rights == RightsEnum.SEARCH_READ_DOWNLOAD)
                )
            ).all()

        else:
            Exception(f"No such right criteria \"{criteria}\"")

        for group_right in group_rights:
            group = session.exec(select(Group).where(Group.idx == group_right.group_idx)).one_or_none()
            if group:
                for user_in_group in group.users:
                    if user_in_group.idx == user_idx:
                        return True

        return False
    

def check_is_creator(email: str, creator_idx: int) -> bool:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No user with email \"{email}\"")
        if user.idx == creator_idx:
            return True
        return False

            
            


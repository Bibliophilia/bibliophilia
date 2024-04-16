from bibliophilia.users.domain.models.basic import UserBase
from sqlmodel import Field


class User(UserBase, table=True):
    idx: int = Field(None, primary_key=True, sa_column_kwargs={"autoincrement": True})

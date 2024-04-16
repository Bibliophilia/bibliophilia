from backend.bibliophilia.core.models import BPModel


class UserBase(BPModel):
    email: str
    name: str

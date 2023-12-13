from typing import Optional

from fastapi import status, APIRouter
from sqlmodel import Session, select

router = APIRouter()
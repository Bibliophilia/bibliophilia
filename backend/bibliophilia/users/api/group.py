from typing import Optional

from fastapi import APIRouter, Response, HTTPException, status

from backend.bibliophilia.users.domain.models.input import GroupCreate

from backend.bibliophilia.users.domain.models.output import GroupInfo
from backend.bibliophilia.users import dependencies

router = APIRouter()


@router.post("/create", response_model=Optional[GroupInfo])
def handle_create_group(request: GroupCreate):
    response = dependencies.group_service.create(group=request)
    if response is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {request.group_name} already exists!")
    return response


@router.post("/edit/{group_name}", response_model=Optional[GroupInfo])
def handle_edit_group(old_group_name: str, request: GroupCreate):
    response = dependencies.group_service.edit(old_group_name, request)
    if response is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {request.group_name} already exists!")
    return response


@router.post("/delete/{group_name}")
def handle_delete_group(group_name: str, user_idx: int):
    dependencies.group_service.delete(group_name, user_idx)


@router.get("/", response_model=list[GroupInfo])
def handle_get_all_by_user_idx(user_idx: int):
    return dependencies.group_service.get_all_by_user_idx(user_idx)



from typing import Optional

from fastapi import APIRouter, Response, HTTPException, status
from starlette.requests import Request

from backend.bibliophilia.books.domain.utils.security import check_is_creator
from backend.bibliophilia.users.domain.models.input import GroupCreate

from backend.bibliophilia.users.domain.models.output import GroupInfo
from backend.bibliophilia.users import dependencies

router = APIRouter()


@router.post("/create", response_model=Optional[GroupInfo])
def handle_create_group(group_create: GroupCreate, request: Request):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to create group")
    if not check_is_creator(request.session.get('user').get('email'), group_create.creator_idx):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to create a group")
    group, users_email = dependencies.group_service.create(group=group_create)
    if group is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {group_create.group_name} already exists!")
    return GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=users_email)


@router.post("/edit/{group_name}", response_model=Optional[GroupInfo])
def handle_edit_group(old_group_name: str, group_create: GroupCreate, request: Request):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to edit group")
    if not check_is_creator(request.session.get('user').get('email'), group_create.creator_idx):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to edit a group")
    group, users_email = dependencies.group_service.edit(old_group_name, group_create)
    if group is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {group_create.group_name} already exists!")
    return GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=users_email)


@router.post("/delete/{group_name}")
def handle_delete_group(request: Request, group_name: str, user_idx: int):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to delete group")
    if not check_is_creator(request.session.get('user').get('email'), user_idx):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to delete a group")
    dependencies.group_service.delete(group_name, user_idx)


@router.get("/", response_model=list[GroupInfo])
def handle_get_all_by_user_idx(request: Request, user_idx: int):
    if request.session.get('user') is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to get all groups")
    if not check_is_creator(request.session.get('user').get('email'), user_idx):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have rights to get all groups")
    groups_and_emails = dependencies.group_service.get_all_by_user_idx(user_idx)
    groups_info = []
    for group, emails in groups_and_emails:
        groups_info.append(GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=emails))
    return groups_info



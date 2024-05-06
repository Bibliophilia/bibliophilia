from typing import Optional

from fastapi import APIRouter, Response, HTTPException, status

from backend.bibliophilia.users.domain.models.input import GroupCreate

from backend.bibliophilia.users.domain.models.output import GroupInfo
from backend.bibliophilia.users import dependencies

router = APIRouter()


@router.post("/create", response_model=Optional[GroupInfo])
def handle_create_group(request: GroupCreate):
    group = dependencies.group_service.create(group=request)
    if group is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {request.group_name} already exists!")
    users_email = []
    for user in group.users:
        users_email.append(user.email)
    return GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=users_email)


@router.post("/edit/{group_name}", response_model=Optional[GroupInfo])
def handle_edit_group(old_group_name: str, request: GroupCreate):
    group = dependencies.group_service.edit(old_group_name, request)
    if group is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Group with name {request.group_name} already exists!")
    users_email = []
    for user in group.users:
        users_email.append(user.email)
    return GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=users_email)


@router.post("/delete/{group_name}")
def handle_delete_group(group_name: str, user_idx: int):
    dependencies.group_service.delete(group_name, user_idx)


@router.get("/", response_model=list[GroupInfo])
def handle_get_all_by_user_idx(user_idx: int):
    groups = dependencies.group_service.get_all_by_user_idx(user_idx)
    groups_info = []
    for group in groups:
        users_email = []
        for user in group.users:
            users_email.append(user.email)
        groups_info.append(GroupInfo(creator_idx=group.creator_idx, group_name=group.group_name, users=users_email))

    return groups_info



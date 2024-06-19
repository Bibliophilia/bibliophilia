from fastapi import APIRouter, Depends
from backend.bibliophilia.core.dependencies import get_session

import backend.bibliophilia.users.api.session as session_api
import backend.bibliophilia.users.api.review as interaction_api
import backend.bibliophilia.users.api.group as group_api


router = APIRouter()

router.include_router(session_api.router,
                      prefix="/session",
                      tags=["session"],
                      dependencies=[Depends(get_session)])

router.include_router(interaction_api.router,
                      prefix="/review",
                      tags=["review"],
                      dependencies=[Depends(get_session)])

router.include_router(group_api.router,
                      prefix="/groups",
                      tags=["groups"],
                      dependencies=[Depends(get_session)])

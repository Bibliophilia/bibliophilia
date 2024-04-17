from fastapi import APIRouter, Depends
from bibliophilia.core.dependencies import get_session

import bibliophilia.users.api.session as session_api
import bibliophilia.users.api.review as interaction_api

router = APIRouter()

router.include_router(session_api.router,
                      prefix="/session",
                      tags=["session"],
                      dependencies=[Depends(get_session)])

router.include_router(interaction_api.router,
                      prefix="/review",
                      tags=["review"],
                      dependencies=[Depends(get_session)])

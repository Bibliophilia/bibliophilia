from authlib.integrations.base_client import OAuthError
from starlette.responses import RedirectResponse

from api import bibliophilia_app
from fastapi import Request, APIRouter

from backend.bibliophilia.server.view.api.routes.api import oauth
from api import bibliophilia_app

router = APIRouter()


@router.route('/login')
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@router.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')

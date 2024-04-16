import json
import os

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)


@router.get('/login')
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@router.get('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return "Error"
    user = access_token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/get-user')


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse(url='/auth')


@router.get('/get-user')
async def get_user(request: Request):
    user = request.session.get('user')
    if user is None:
        return RedirectResponse(url='/login')
    user_data = json.dumps(user, ensure_ascii=False)
    return {'user': user_data}
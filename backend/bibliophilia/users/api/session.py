import json
import logging
import os

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

from bibliophilia.config import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID
import bibliophilia.users.dependencies as dependencies
from bibliophilia.users.domain.models.input import UserCreate

load_dotenv()

router = APIRouter()


oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/users/session/auth'
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
    except OAuthError as e:
        return str(e)
    user = access_token.get('userinfo')
    print(f"username: {user.get('name')}")
    print(f"user email: {user.get('email')}")
    print(f"user: {dict(user)}")
    if user:
        request.session['user'] = dict(user)
    dependencies.user_service.create_book(
        UserCreate(
            email=user.get('email'),
            name=user.get('name')
        )
    )
    return RedirectResponse(url='/users/session/get-user')


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse(url='/users/session/login')


@router.get('/get-user')
async def get_user(request: Request):
    user = request.session.get('user')
    if user is None:
        return RedirectResponse(url='/users/session/login')
    user_data = json.dumps(user, ensure_ascii=False)
    return {'user': user_data}

from re import S
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from .. database.database import get_db
from sqlalchemy.orm import Session
from .. validators import val_auth
from .. models import mdl_user
from .. oauth2 import oauth2
from .. utils import utils
from loguru import logger

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=val_auth.Token)
@logger.catch()
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(mdl_user.Users).filter(
        mdl_user.Users.username == user_credentials.username).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

    if not utils.verify(user_credentials.password, user.password):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'invalid credentials'})

    access_token = oauth2.create_access_token(
        data={'id': user.id, 'name': user.name, 'permissions': user.permissions})

    return {'access_token': access_token, 'token_type': 'bearer'}

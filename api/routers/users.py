from fastapi import APIRouter
from .. validators import users

router = APIRouter(prefix='/user', tags=['Users'])


@router.get('')
def get_user():
    return {'detail': 'new user'}


@router.get('')
def get_user():
    return {'message': 'get_user'}

from fastapi import status, HTTPException, Depends, APIRouter
from .. validators import admin

router = APIRouter(prefix='/admin', tags=['Admin'])


@router.post('', response_model=admin.UserOut)
def user_create(user: admin.UserCreate):
    print(user)
    return user


@router.get('/{name}')
def get_user(name: str):
    return name

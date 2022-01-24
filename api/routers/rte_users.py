from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database.database import cursor, conn, get_db
from .. validators import val_user
from .. models import mdl_user
from .. utils import utils
from .. oauth2.oauth2 import get_current_user


router = APIRouter(prefix='/users', tags=['Users'])


# Validaton: api/validators/val_user.py
# Model: api/models/mdl_user.py


# Create New User
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_user.UserOut)
def create_user(user: val_user.UserCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    does_exist_name = db.query(mdl_user.Users).filter(
        mdl_user.Users.name == user.name).first()
    if does_exist_name:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'name: {user.name} already exists')

    does_exist_username = db.query(mdl_user.Users).filter(
        mdl_user.Users.username == user.username).first()
    if does_exist_username:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'username: {user.username} already exists')

    user.password = utils.hash(user.password)

    db_data = mdl_user.Users(created_by=current_user.id,
                             updated_by=current_user.id, **user.dict())

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


# Return List Of All Users
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_user.UserOut])
def get_users(db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_user.Users).order_by(mdl_user.Users.name).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='users do not exist')

    return db_data


# Return Single User By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_user.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_user.Users).filter(
        mdl_user.Users.id == id).first()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')

    return db_data


# Update User By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_user.UserOut)
def update_user(id: int, user: val_user.UserUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_user.Users).filter(mdl_user.Users.id == id)
    update = query.first()
    if not update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')

    does_exist_name = db.query(mdl_user.Users).filter(
        mdl_user.Users.name == user.name).first()

    if does_exist_name and does_exist_name.id != id:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'name: {user.name} already exists')

    new_dict = user.dict()
    new_dict['updated_by'] = current_user.id
    query.update(new_dict, synchronize_session=False)
    db.commit()

    return query.first()


# Delete User By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_user.Users).filter(mdl_user.Users.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# psycopg2 routes ###################################################################################
#
# @router.post('', status_code=status.HTTP_201_CREATED, response_model=val_user.UserOut)
# def user_create(user: val_user.UserCreate):
#     user.created_by = 1
#     user.updated_by = 1
#     cursor.execute("""
#         INSERT INTO users (name, is_active, role, email, brewery, permissions, password, updated_by)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         RETURNING *;
#     """, (user.name, user.is_active, user.role, user.email, user.brewery, user.permissions, user.password, user.updated_by))
#     new_user = cursor.fetchone()
#     conn.commit()
#     return new_user
#
# @router.get('', response_model=List[val_user.UserOut])
# def get_users():
#     cursor.execute("""
#         SELECT * FROM users;
#     """)
#     users = cursor.fetchall()
#     return users
#
# @router.get('/{id}', response_model=List[val_user.UserOut])
# def get_user(id: int):
#     cursor.execute("""
#         SELECT * FROM users
#         WHERE id = %s;
#     """, (str(id),))
#     user = cursor.fetchall()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'user with id: {id} does not exist')
#     return user

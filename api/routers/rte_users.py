from fastapi import status, Response, Depends, APIRouter
from .. database.database import cursor, conn, get_db
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. validators import val_user
from .. models import mdl_user
from .. utils import utils
from loguru import logger
from typing import List


router = APIRouter(prefix='/users', tags=['Users'])


# Validaton: api/validators/val_user.py
# Model: api/models/mdl_user.py


# Create New User
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_user.UserOut)
@logger.catch()
def create_user(user: val_user.UserCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        does_exist = db.query(mdl_user.Users).filter(
            mdl_user.Users.name == user.name).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({user.name}) violates unique contraint on column user.name'})

        does_exist_username = db.query(mdl_user.Users).filter(
            mdl_user.Users.username == user.username).first()
        if does_exist_username:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({user.username}) violates unique contraint on column user.username'})

        user.password = utils.hash(user.password)

        db_data = mdl_user.Users(created_by=current_user.id,
                                 updated_by=current_user.id, **user.dict())

        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Users
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_user.UserOut])
def get_users(active: str = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_user.Users).filter(
            mdl_user.Users.is_active == active).order_by(mdl_user.Users.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (name)=(all) are not present in table users'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single User By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_user.UserOut)
@logger.catch()
def get_user(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_user.Users).filter(
            mdl_user.Users.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table users'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update User By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_user.UserOut)
@logger.catch()
def update_user(id: int, user: val_user.UserUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_user.Users).filter(mdl_user.Users.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table users'})

        does_exist = db.query(mdl_user.Users).filter(
            mdl_user.Users.name == user.name).first()
        if does_exist and does_exist.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({user.name}) violates unique contraint on column user.name'})

        new_dict = user.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Delete User By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_user(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_user.Users).filter(mdl_user.Users.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table users'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Rest User Password By ID
@router.put('/password/reset', status_code=status.HTTP_200_OK)
@logger.catch()
def reset_user_password(user: val_user.UserPasswordReset, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_user.Users).filter(mdl_user.Users.id == user.id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table users'})

        user.password_reset = utils.hash(user.password_reset)

        new_dict = user.dict()
        new_dict['updated_by'] = current_user.id
        new_dict['password'] = '$2b$12$uxpquslSDnH4qR/zKdlSEe6Tk5NdAqxZby14H5zDOn86wX2/Z75k1'
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Change User Password By username
@router.put('/password/change', status_code=status.HTTP_200_OK, include_in_schema=False)
@logger.catch()
def change_user_password(user: val_user.UserPasswordChange, db: Session = Depends(get_db)):
    try:
        query = db.query(mdl_user.Users).filter(
            mdl_user.Users.username == user.username)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'invalid credentials'})

        user.password = utils.hash(user.password)

        new_dict = user.dict()
        new_dict['password_reset'] = 'Empty'
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

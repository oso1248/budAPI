from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. database.database import get_db
from sqlalchemy.orm import Session
from .. validators import val_auth
from .. models import mdl_user

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

JWT_SECRET_KEY = "SALDKJF90SD8FSDAPIFHAPSD978DSFSDFKLJH445KJH;DSF99780ASDFLH345KJH8DFASD87DFG8GF"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jet = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jet


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('id')
        if not id:
            raise credentials_exception
        token_data = val_auth.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized', headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exception)
    user = db.query(mdl_user.Users).filter(
        mdl_user.Users.id == token.id).first()

    return user

from jose import JWTError, jwt
from fastapi import Depends, Request, status, HTTPException
from . import schemas
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#openssl rand -hex 32
SECRET_KEY =f'{setting.secret_key}'
ALGORITHM = f"{setting.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.Token_data(id=id)
    except JWTError:
        raise credential_exception
    return token_data
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized",
                                          headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)
from jose import JWTError
import jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

#SECRET KEY
#ALGO
#EXP time for token

SECRET_KEY = "7b4098e572b24457266a603e82e67b1f64fb0d0015a17f9575d24bf0ddbdd2af"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def create_access_token(data: dict, exp_time: timedelta | None = None):  #TODO: to get more understanding about last variavble
    data_to_encode = data.copy()

    if exp_time:
        expire_t = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire_t = datetime.now(timezone.utc) + timedelta(minutes=30)

    data_to_encode.update({"exp": expire_t})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f'Could not validate the credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token=token, credentials_exception=credentials_exception)

#TODO: check the flow of get_current_user and verify acccess token fucntions - need more understanding
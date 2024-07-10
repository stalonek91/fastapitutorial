import jwt 
from datetime import datetime, timedelta, timezone


#SECRET KEY
#ALGO
#EXP time for token

SECRET_KEY = "7b4098e572b24457266a603e82e67b1f64fb0d0015a17f9575d24bf0ddbdd2af"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, exp_time: timedelta | None = None):  #TODO: to get more understanding about last variavble
    data_to_encode = data.copy()

    if exp_time:
        expire_t = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire_t = datetime.now() + timedelta(minutes=30)

    data_to_encode.update({"exp": expire_t})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

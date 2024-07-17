from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['authentication'], prefix='/auth')

@router.post("/login", response_model=schemas.Token)
def login(user_authentication: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_sql_db)):
          
          find_user = db.query(models.User).filter(models.User.email == user_authentication.username).first()
          

          if not find_user:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials are invalid")
          
          hashed_pass = find_user.password

          if not utils.verify_password(hashed_password=hashed_pass, user_password=user_authentication.password):
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='WRONG PASSWORD ZIOMEK')
                  
          access_token = oauth2.create_access_token(data={"user_id": find_user.id})
          return {"access_token": access_token, "token_type": "bearer"}
          


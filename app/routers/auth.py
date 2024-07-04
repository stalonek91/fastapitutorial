from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils

router = APIRouter(tags=['authentication'], prefix='/auth')

@router.post("/login")
def login(user_authentication: schemas.User_login, db: Session = Depends(database.get_sql_db)):
          print(user_authentication)
          find_user = db.query(models.User).filter(models.User.email == user_authentication.email).first()

          if not find_user:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credentials are invalid")
          
          hashed_pass = find_user.password

          if utils.verify_password(hashed_password=hashed_pass, user_password=user_authentication.password):
                  return {'kurwa dziala': 'kwik'}
          else:
                  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='WRONG PASSWORD ZIOMEK')
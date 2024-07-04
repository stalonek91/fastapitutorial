from .. import database, models, utils, tutorial_d1, schemas
from ..database import get_sql_db
from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=["users"])

@router.get("/{user_id}", response_model=schemas.User_return)
def users_login(user_id: int, db: Session = Depends(get_sql_db)):

    selected_user = db.query(models.User).filter(models.User.id == user_id)
    user = selected_user.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id} not found')


    return user


@router.get("/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def users(db: Session = Depends(get_sql_db)):
    users = db.query(models.User).all()
    return users


@router.post("/add", response_model=schemas.User_return, status_code=status.HTTP_201_CREATED)
def users_add(user: schemas.User_create, db: Session = Depends(get_sql_db)):

    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password

        new_user = models.User(
            **user.model_dump()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

    return new_user
from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, Request
from typing import Union, Optional, List, Dict
import random
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from . import models, database, schemas, utils
from .database import engine, get_sql_db
from sqlalchemy.orm import Session


models.base.metadata.create_all(bind=engine)



#TODO: youtube: 6:15:26

app = FastAPI()

@app.get("/users/{user_id}", response_model=schemas.User_return)
def users_login(user_id: int, db: Session = Depends(get_sql_db)):

    selected_user = db.query(models.User).filter(models.User.id == user_id)
    user = selected_user.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id} not found')


    return user


@app.get("/users", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def users(db: Session = Depends(get_sql_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users/add", response_model=schemas.User_return, status_code=status.HTTP_201_CREATED)
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

@app.get("/sqlpost", response_model=List[schemas.PostResponse])
def read_sql_posts(db: Session = Depends(get_sql_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/sqlpost/{post_id}", response_model=schemas.PostResponse)
def get_post_id(post_id: int, db: Session = Depends(get_sql_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f'Post with id:{post_id} not found!')

    return post


#post with pydantic not request
@app.post("/add_post_pydantic", status_code=status.HTTP_201_CREATED, response_model=schemas.PostUpdate)
def add_post_pydantic(post_data: schemas.PostBase, db: Session = Depends(get_sql_db)):
    new_post = models.Post(
        **post_data.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.post("/add_sql_post/", status_code=status.HTTP_201_CREATED)
async def add_sql_post(request: Request, db: Session = Depends(get_sql_db)):
    data = await request.json()
    title = data.get('title')
    content = data.get('content')
    published = data.get('published', True)

    if not title or not content:
        raise HTTPException(status_code=400, detail='Title and content must be provided')
    
    new_post = models.Posts(
        title=title,
        content=content,
        published=published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/delete_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_sql_db)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_to_delete)
    if not post_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')

    post_to_delete.delete(synchronize_session=False)
    db.commit()

#FIXME: kurwa nie dziala put
@app.put("/update_post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post_data: schemas.PostUpdate = Body(...), db: Session = Depends(get_sql_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')

    print(f'Post_data: {post_data.model_dump()}')
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()

    return post_query

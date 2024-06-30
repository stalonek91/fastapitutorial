from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, Request
from typing import Union, Optional, List, Dict
import random
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from . import models, database, schemas
from .database import engine, get_sql_db
from sqlalchemy.orm import Session

models.base.metadata.create_all(bind=engine)

#TODO: youtube: 5:26

app = FastAPI()


@app.get("/sqlpost", response_model=List[schemas.Post])
def read_sql_posts(db: Session = Depends(get_sql_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/sqlpost/{post_id}", response_model=schemas.Post)
def get_post_id(post_id: int, db: Session = Depends(get_sql_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f'Post with id:{post_id} not found!')

    return post


#post with pydantic not request
@app.post("/add_post_pydantic", status_code=status.HTTP_201_CREATED)
def add_post_pydantic(post: schemas.Post, db: Session = Depends(get_sql_db)):
    new_post = models.Post(
        **post.model_dump()
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

#TODO: add the option to update only provided by user values
@app.put("/update_post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post_data: schemas.Post = Body(...), db: Session = Depends(get_sql_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')

    print(f'Post_data: {post_data.model_dump()}')
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()

    return post_query













 





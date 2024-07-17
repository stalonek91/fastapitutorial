from .. import database, tutorial_d1, schemas, models, utils, oauth2
from fastapi import status, Depends, Body, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from ..database import get_sql_db
from typing import List

router = APIRouter(prefix='/sqlpost', tags=["posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def read_sql_posts(db: Session = Depends(get_sql_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post_id(post_id: int, db: Session = Depends(get_sql_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f'Post with id:{post_id} not found!')

    return post

#FIXME: kurwa nie dziala put
@router.put("/update_post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post_data: schemas.PostUpdate = Body(...), db: Session = Depends(get_sql_db), ):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')

    print(f'Post_data: {post_data.model_dump()}')
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()

    return post_query


#post with pydantic not request
@router.post("/add_post_pydantic", status_code=status.HTTP_201_CREATED, response_model=schemas.PostUpdate)
def add_post_pydantic(post_data: schemas.PostBase, db: Session = Depends(get_sql_db), user_id: int = Depends(oauth2.get_current_user)):
    print(f'USER ID is: {user_id}')
    new_post = models.Post(
        **post_data.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# @router.post("/add_sql_post/", status_code=status.HTTP_201_CREATED)
# async def add_sql_post(request: Request, db: Session = Depends(get_sql_db)):
#     data = await request.json()
#     title = data.get('title')
#     content = data.get('content')
#     published = data.get('published', True)

#     if not title or not content:
#         raise HTTPException(status_code=400, detail='Title and content must be provided')
    
#     new_post = models.Post(
#         title=title,
#         content=content,
#         published=published
#     )
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


@router.delete("/delete_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_sql_db), user_id: int = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_to_delete)
    if not post_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')

    post_to_delete.delete(synchronize_session=False)
    db.commit()
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Union, Optional
import random


app = FastAPI()

hello_dict = {"Hello": "Sylwek", "kwoka": "psiocha"}


my_posts = [{"title": "Lord of the rings", "content": "Content of LOTR", "id": 1},
            {"title": "Jack the Ripper", "content": "Content of J the Ripper", "id": 2}
            ]

class Post(BaseModel):
    title: str
    content: str
    id: int = Field(default_factory=lambda: random.randint(1,1000))
    is_published: bool = True
    is_bestseller: Optional[bool] = None


@app.get("/")
def index():
    dict_iter = iter(hello_dict.items())
    k,v = next(dict_iter)
    k,v = next(dict_iter)
    return {f"Key is: {k}, value is: {v}"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    my_posts.append(post.model_dump())
    return {"data": post}
 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_to_delete = find_index_post(id)
    if post_to_delete:
        my_posts.pop(post_to_delete)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The post ID has not been found")


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    returned_post = find_post(post_id)
    if returned_post:
        return {"returned post": returned_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {post_id} has not been found")


def find_post(post_id):
    for element in my_posts:
        if element.get("id") == post_id:
            print(element)
            return element
    return None

def find_index_post(post_id):
    for i, post in enumerate(my_posts):
        if post.get("id") == post_id:
            print(f'Returning element in my_post with index: {i} as id was: {post_id}')
            return i


#FIXME 
@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    returned_post_id = find_index_post(post_id)
    print(f'Found post index is: {returned_post_id}')

    if returned_post_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {post_id} has not been found")

    post_dict = post.model_dump()
    post_dict["id"] = post_id
    my_posts[returned_post_id] = post_dict
    return f"Post with id: {post_dict} updated"

    





## 1h 48min 17 sec 
## 2h 00min 47 sec
## 2h 06min 38 sec
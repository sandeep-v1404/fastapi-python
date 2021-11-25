from os import stat
from typing import Optional
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette.responses import Response

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts = [{
    "title": "FastAPI",
    "content": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
    "rating": 4,
    'id': 1,

}, {
    "title": "NestJs",
    "content": "NestJs is a backend framework built on top of Node.js",
    "rating": 4,
    'id': 2,
},
]


def find_post(id):
    for p in posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.post("/createpost")
def create_post(post: Post):
    post = post.dict()
    post["id"] = len(posts)+1
    posts.append(post)
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} not found')
    return {"post": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} not found')
    post_dict = post.dict()
    post_dict[id] = id
    posts[id] = post_dict
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int):
    index = find_index_post(id)
    if(index == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} not found')
    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

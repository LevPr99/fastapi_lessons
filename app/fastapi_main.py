from . import database
from time import sleep
from datetime import datetime

from random import randrange
from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel


# Create FastAPI object
app = FastAPI()


# Post model
class UserPost(BaseModel):
    id: int = randrange(2, 100000000)
    title: str = 'Blank title'
    content: str = 'Blank content'
    publish: bool = False
    created_at: datetime | None = None
    publish_at: datetime | None = None
    


# Connect to DB
conn_file = 'app/dblogin_data.json'
conn_evidence = database.get_connect_data(conn_file)

DB = database.connect_db(conn_evidence)

while DB is None:
    DB = database.connect_db(conn_evidence)
    sleep(5)


# CRUD app
# C - create
# R - read
# U - update
# D - delete
@app.get('/')
def root():
    return {'Hello': 'User'}

# C - create
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: UserPost):
    data = database.create_post(conn=DB, post=post)
    return {'msg': 'Post created succesfully!', 'post data': data}

# R - read
@app.get('/posts')
def get_all_posts():
    return {'msg': 'All posts from users', 'Posts': database.get_post(conn=DB)}

@app.get('/posts/{id}')
def get_post_by_id(id: int):
    data = database.get_post(conn=DB, id=id)
    return {'post': data}

# U - update
@app.patch('/posts/{id}')
def update_post(id: int, post: UserPost):
    updated_post = database.update_post(conn=DB, id=id, data=post)    
    return {'msg': 'post updated!', 'post': updated_post}

# D - delete
@app.delete('/posts/{id}', 
            status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    database.delete_post(conn=DB, id=id)
    return {'Delete': f'Post {id}'}
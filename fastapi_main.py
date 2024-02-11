from fastapi import FastAPI
from typing import Optional, Dict, List

from pydantic import BaseModel

app = FastAPI()

class UserPost(BaseModel):
    title: str
    content: str
    publishing: bool = False
    raiting: Optional[int] = None


my_posts: list[dict] = []



# CRUD app

# C - create
# R - read
# U - update
# D - delete


@app.get('/')
def root() -> Dict[str, str]:
    return {'Main page': '/'}

# C - create
@app.post('/posts')
def create_post(data: UserPost):
    data = data.model_dump()
    global my_posts
    my_posts.append(data)
    return {'msg': 'Post created succesfully!', 'post data': data}

# R - read
@app.get('/posts')
def get_all_posts():
    global my_posts
    return {'msg': 'All posts from users', 'Any information': my_posts}

@app.get('/posts/{_id}')
def get_post_by_id(_id: int):
    global my_posts
    if len(my_posts) >= _id and 0 <= _id - 1:
        return {'post': my_posts[_id - 1]}
    else:
        return {}

# U - update
@app.put('/posts/{_id}')
def update_post(_id: int, field_to_update: str, content_to_update: str | int):
    global my_posts
    if len(my_posts) >= _id and 0 <= _id - 1:
        my_posts[_id - 1][field_to_update] = content_to_update
    return my_posts[_id - 1]

# D - delete
@app.delete('/posts/{_id}')
def delete_post(_id: int):
    global my_posts
    if len(my_posts) >= _id and 0 <= _id - 1:
        del my_posts[_id - 1]
    return {'msg': f'Delete post #{_id} successfully!'}
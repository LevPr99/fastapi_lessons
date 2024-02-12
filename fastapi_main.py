from fastapi import FastAPI, HTTPException, status
from typing import Optional, Dict, List

from pydantic import BaseModel

app = FastAPI()

class UserPost(BaseModel):
    title: str
    content: str
    publishing: bool = False
    raiting: Optional[int] = None


my_posts: list[dict] = [{
    "title": "Post 1",
    "content": "This contents is reflection that Post model works!",
    "publishing": False
}]



# CRUD app

# C - create
# R - read
# U - update
# D - delete


@app.get('/')
def root() -> Dict[str, str]:
    return {'Main page': '/'}

# C - create
@app.post('/posts', status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},
                            ) 

# U - update
@app.put('/posts/{_id}')
def update_post(_id: int, field_to_update: str, content_to_update: str | int):
    global my_posts
    if len(my_posts) >= _id and 0 <= _id - 1:
        my_posts[_id - 1][field_to_update] = content_to_update
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Item {_id} not found", 
                            headers={"X-Error": "There goes my error"},
                            ) 
    return my_posts[_id - 1]

# D - delete
@app.delete('/posts/{_id}', 
            status_code=status.HTTP_204_NO_CONTENT)
def delete_post(_id: int):
    global my_posts
    if len(my_posts) >= _id and 0 <= _id - 1:
        del my_posts[_id - 1]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},
                            )
from fastapi import FastAPI, HTTPException, status
from typing import Optional, Dict, List
# from fastapi.encoders import jsonable_encoder
from random import randrange

from pydantic import BaseModel

app = FastAPI()

class UserPost(BaseModel):
    id: int = randrange(2, 100000000)
    title: str = 'Blank title'
    content: str = 'Blank content'
    publishing: bool = False
    raiting: int | None = None


my_posts: list[dict] = [{
    "id": 1,
    "title": "Post 1",
    "content": "This contents is reflection that Post model works!",
    "publishing": False,
    "raiting": 5,
}]

def find_post_index(id: int) -> int | None:
    if 0 <= (id - 1) < len(my_posts):
        return id - 1
    return None

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
    my_posts.append(data)
    print(data)
    return {'msg': 'Post created succesfully!', 'post data': data}

# R - read
@app.get('/posts')
def get_all_posts():
    return {'msg': 'All posts from users', 'Posts': my_posts}


@app.get('/posts/{id}')
def get_post_by_id(id: int):
    
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},) 
        
    return {'post': my_posts[index]}


# U - update
@app.patch('/posts/{id}')
def update_post(id: int, post: UserPost):
    
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},)
    
    stored_data = my_posts[index]
    stored_post_model = UserPost(**stored_data)
    new_data = post.model_dump(exclude_unset=True)
    # print(new_data)
    new_post = stored_post_model.model_copy(update=new_data)
    # print(new_post)
    my_posts[index] = new_post
    
    return {'msg': 'post updated!'}


# D - delete
@app.delete('/posts/{id}', 
            status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},) 
    return {'item deleted': my_posts.pop(index)}
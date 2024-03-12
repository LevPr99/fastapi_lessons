from fastapi import FastAPI, status, Depends
from . import models
from .database import delete_post_db, engine, get_db, get_post, create_post_db, UserPost
from sqlalchemy.orm import Session

models.Post.metadata.create_all(bind=engine)

# Create FastAPI object
app = FastAPI()


# CRUD app
# C - create
# R - read
# U - update
# D - delete
@app.get('/')
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post)
    print(posts)
    return {'data': posts.all()}

# C - create
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: UserPost, db: Session = Depends(get_db)):
    new_post = create_post_db(post, db)
    return {'msg': 'Post created succesfully!', 'post data': new_post}

# R - read
@app.get('/posts')
def get_all_posts(db: Session = Depends(get_db)):
    posts = get_post(db)
    return {'all_posts': posts}

@app.get('/posts/{id}')
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = get_post(db, id)
    return {'post': post}

# U - update
# @app.patch('/posts/{id}')
# def update_post(id: int, post: UserPost):
#     updated_post = database.update_post(conn=DB, id=id, data=post)    
#     return {'msg': 'post updated!', 'post': updated_post}

# D - delete
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post_db(db, id)
    # return {'Delete': f'Post {id}'}
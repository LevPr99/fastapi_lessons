from datetime import datetime
import json
from typing import Any
from pydantic import BaseModel
from sqlalchemy import URL
from os.path import exists
from fastapi import Depends, HTTPException, status
from . import models

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# Post model
class UserPost(BaseModel):
    title: str
    content: str
    publish: bool = False


def get_connect_data(file_json: str):
    if exists(file_json):
        conn_str = None
        with open(file_json, 'r') as file:
           conn_str = json.loads(file.read())
    return conn_str


# Create DB connection link
PG_DATABASE_URL = str(URL('postgresql+psycopg',
                          **get_connect_data('resources/dblogin_data.json')))
engine = create_engine(PG_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def error_raiser(content: Any | None, headers: str | None=None):
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Item not found", 
                        headers={"X-Error": headers} if headers is not None else headers,)

def get_post(db: Session, id: int | None = None, skip: int = 0, limit: int = 100):
    if id is not None:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    else:
        post = db.query(models.Post).offset(skip).limit(limit).all()
    error_raiser(post)
    return post
    
def create_post_db(post: UserPost, db: Session = Depends(get_db)):
    post = post.model_dump()
    new_post = models.Post(**post)
    if post['publish']:
        new_post.publish_at = datetime.now()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
# def update_post(conn: psycopg.Connection, id: int, data):
#     with conn.cursor() as cur:
#         cur.execute("UPDATE posts SET title = %s, content = %s, publish = %s, publish_at = %s WHERE id = %s RETURNING *;",
#                     (data.title, data.content, data.publish, 
#                      (datetime.now() if data.publish == True else None),
#                      id))
#         data = cur.fetchall()
#     conn.commit()
#     if data is None or len(data) < 1:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                         detail="Item not found", 
#                         headers={"X-Error": "There goes my error"},)
#     return data

def delete_post_db(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id)
    error_raiser(post.first())
    post.delete()
    db.commit()
    # return post
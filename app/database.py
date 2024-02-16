from os.path import exists
import json
from typing import Dict
import psycopg
from psycopg.rows import dict_row
from fastapi import HTTPException, status
from datetime import datetime



def get_connect_data(file_json: str):
    if exists(file_json):
        conn_str = None
        with open(file_json, 'r') as file:
           conn_str = json.loads(file.read())
    return conn_str

def connect_db(evidence: Dict[str, str]):
    try:
        con = psycopg.connect(row_factory=dict_row,**evidence)
        print('Connection to database sucessful!')
    except psycopg.Error as error:
        print('Connection to DB failed!')
        print(error)
        return None
    return con

def get_post(conn: psycopg.Connection, id: int | None=None):
    data = {}
    with conn.cursor() as cur:
        if id is not None:
            cur.execute(f"SELECT * FROM posts WHERE id = {id} ORDER BY id ASC;")
            data = cur.fetchone()
        else:
            cur.execute(f"SELECT * FROM posts ORDER BY id ASC;")
            data = cur.fetchall()
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"},) 
    return data
    
def create_post(conn: psycopg.Connection, post):
    with conn.cursor() as cur:
        if post.publish is True:
            cur.execute(
                """INSERT INTO posts (title, content, publish, publish_at) 
                VALUES (%s, %s, %s, %s) RETURNING * ;""", 
                (post.title, post.content, post.publish, datetime.now()))
        else:
            cur.execute(
                """INSERT INTO posts (title, content, publish) 
                VALUES (%s, %s, %s) RETURNING * ;""", 
                (post.title, post.content, post.publish))
        data = cur.fetchone()
    conn.commit()
    return data
    
def update_post(conn: psycopg.Connection, id: int, data):
    with conn.cursor() as cur:
        cur.execute("UPDATE posts SET title = %s, content = %s, publish = %s, publish_at = %s WHERE id = %s RETURNING *;",
                    (data.title, data.content, data.publish, 
                     (datetime.now() if data.publish == True else None),
                     id))
        data = cur.fetchall()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Item not found", 
                        headers={"X-Error": "There goes my error"},)
    conn.commit()
    return data

def delete_post(conn: psycopg.Connection, id: int):
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM posts WHERE id = {id};")
    conn.commit()
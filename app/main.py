from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='shreyes', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection success")
        break
    except Exception as e:
        print("DB conn failed", e)
        time.sleep(2)

my_posts = [ {"title": "title 1", "content": "content of 1", "id" : 1}, {"title": "title 2", "content": "content of 2", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


# root path
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_post(db: Session= Depends(get_db)):
    return {"status": "success"}



@app.get("/posts")
def get_posts():
    cursor.execute(""" select * from posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts} # the my_posts variable is already serialized here 



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning *  """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  #save the data to the database
    return {"data": new_post}



@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" select * from posts where id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Post with the id {id} was not found"}
    return {"post_details" : post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):

    cursor.execute(""" delete from posts where id =%s  returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """ , (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    return {"data": updated_post}




























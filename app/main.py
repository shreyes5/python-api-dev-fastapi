from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
import utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db)):
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts # the my_posts variable is already serialized here 



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning *  """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  #save the data to the database

    # **post.model_dump()
    # print(**post.model_dump())
    # new_post2 = models.Post(**post.model_dump())
    new_post = models.Post(
        **post.model_dump()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post



@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute(""" select * from posts where id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Post with the id {id} was not found"}
    return {"post_details" : post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db:Session = Depends(get_db)):

    # cursor.execute(""" delete from posts where id =%s  returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post =  db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db)):

    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """ , (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  post_query.first()


# User path operations


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):


    # hash the users password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **user.model_dump()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user

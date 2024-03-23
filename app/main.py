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
import app.utils as utils
from .routers import post,user

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




app.include_router(post.router)
app.include_router(user.router)



# root path
@app.get("/")
def root():
    return {"message": "Hello World"}


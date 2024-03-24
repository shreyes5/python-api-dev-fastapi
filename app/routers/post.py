from app import oauth2
from .. import models,schemas,utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()


    # Get logged in user's posts
    # posts = db.query(models.Post.owner_id).filter(models.Post.id == current_user.id).all()

    posts = db.query(models.Post).all()
    return posts # the my_posts variable is already serialized here 



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning *  """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  #save the data to the database

    # **post.model_dump()
    # print(**post.model_dump())
    # new_post2 = models.Post(**post.model_dump())

    print(current_user.id, "asdijhasikdhasihdj")
    new_post = models.Post(owner_id = current_user.id, 
        **post.model_dump()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" select * from posts where id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Post with the id {id} was not found"}
    return  post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" delete from posts where id =%s  returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query =  db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """ , (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  post_query.first()
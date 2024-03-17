from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None

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



@app.get("/posts")
def get_posts():
    return {"data": my_posts} # the my_posts variable is already serialized here 



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()   
    post_dict['id'] = randrange(0,123456)
    my_posts.append(post_dict)
    return {"data": post_dict}



@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Post with the id {id} was not found"}
    return {"post_details" : post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    # delete a post
    # find the index in the array specified by the id
    # my_posts.pop[index]
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} was not found")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
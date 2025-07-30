# fastapi dev main.py --reload
# uvicorn main:app --reload
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str  # required
    content: str  # required
    published: bool = True  # optional (default is True)
    rating: Optional[int] = None    # fully optional field
    

# database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='krishna', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('Connection to database failed.')
        print('Error: ', error)
        time.sleep(3)


my_posts = [{"id": 1, "title": "title of post 1", "content": "this is content of post 1"},{"id": 2, "title": "title of post 2", "content": "this is content of post 2"}]

@app.get("/")
def root():
    return {"message": "Welcome to python fast API!!!!!!"}


# @app.get("/posts")
# def get_posts():
#     return {"data": "This is your posts."}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}

# @app.post("/createposts")
# def create_posts(new_post: Post):
#     print(new_post)
#     print(type(new_post))
#     print(new_post.model_dump())    # print(new_post.dict())
#     print(new_post.title)
#     print(new_post.content)
#     print(new_post.published)
#     print(new_post.rating)
#     return {"data": new_post}

# --------------------------------------------create a post----------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    # print(post.model_dump())    # doesnt change the original post
    # print(post)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# --------------------------------------------get all posts----------------------

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# --------------------------------------------get latest post----------------------
@app.get("/posts/latest")       # important : order of routes matters here
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": [post]}

# --------------------------------------------get a post by id----------------------
@app.get("/posts/{id}")
def get_post(id: int):          # automatic validation and good error message if validation fails instead of showing crashing error messages
    print(id)
    print(type(id))
    # post = [post for post in my_posts if post["id"] == id]   # [expression for item in iterable if condition]
    post = next((post for post in my_posts if post["id"] == id), None)
    if not post:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    
    # or
    # filter(function, iterable)
    # list(filter(lambda post: post["id"] == 2, posts))
    # so
    # post = list(filter(lambda post: post["id"] == id, posts))
    
    return {"data": post}



# --------------------------------------------delete----------------------

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # # method one:
    # global my_posts
    # my_posts = [post for post in my_posts if post["id"]!= id]
    
    # method two:
    # find the index in the array that has required id
    # my_posts.pop(index)
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            del my_posts[i]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # # method 3
    # # from gpt
    # index = next((i for i, post in enumerate(my_posts) if post["id"] == id), None)
    # if index is None:
    #     raise HTTPException(status_code=404, detail="Post not found")
    # my_posts.pop(index)
    # return {"message": "Post deleted successfully"}
    
    
# --------------------------------------------create a post----------------------

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, new_post: Post):
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = id
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts[i] = new_post_dict
            return {"data": new_post_dict}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

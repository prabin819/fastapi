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
    return {"message": "Welcome to python fast API with postgres!!!!!!"}


# --------------------------------------------create a post----------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
    #above method will technically work but is vunerable to sql injection
    cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# --------------------------------------------get all posts----------------------

@app.get("/posts")
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

# --------------------------------------------get latest post----------------------
@app.get("/posts/latest")       # important : order of routes matters here
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": [post]}

# --------------------------------------------get a post by id----------------------
@app.get("/posts/{id}")
def get_post(id: int):          # automatic validation and good error message if validation fails instead of showing crashing error messages
    # print(id)
    # print(type(id))
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    return {"data": post}



# --------------------------------------------delete----------------------

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# --------------------------------------------create a post----------------------

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    print(post)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}

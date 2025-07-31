# fastapi dev main.py --reload
# uvicorn main:app --reload
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
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
    title: str  # required
    content: str  # required
    published: bool = True  # optional (default is True)    

# database connection (psycopg)
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
def create_posts(post: Post, db: Session = Depends(get_db)):
    # # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
    # #above method will technically work but is vunerable to sql injection
    # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # print(post.model_dump())
    # new_post = models.Tweet(title=post.title, content=post.content, published=post.published)
    new_post = models.Tweet(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# --------------------------------------------get all posts----------------------

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Tweet).all()
    print(posts)
    return {"data": posts}

# --------------------------------------------get latest post----------------------
@app.get("/posts/latest")       # important : order of routes matters here
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": [post]}

# --------------------------------------------get a post by id----------------------
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):          # automatic validation and good error message if validation fails instead of showing crashing error messages
    # # print(id)
    # # print(type(id))
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', (id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    # return {"data": post}
    
    post = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    return {"data": post}
    



# --------------------------------------------delete----------------------

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (id,))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# --------------------------------------------create a post----------------------

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, new_post: Post, db: Session = Depends(get_db)):
    # print(post)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # return {"data": updated_post}

    post_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    # post_query.update({'title':'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    return {'data': updated_post}

# --------------------------------------------test route for orm----------------------


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Tweet).all()
    print(posts)
    return {"data": posts}